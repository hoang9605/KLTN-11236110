"""ViHealthBERT relation classifier with typed entity markers, for training and inference.

The marked sentence comes from relation_extraction.data.mark_pair, e.g.
  "[HEAD_CONDITION]đau[/HEAD] ở [TAIL_BODY_PART]vùng bụng[/TAIL] ..."
The marker strings are added to the tokenizer as special tokens. The pair representation
is [h_HEAD_START ; h_TAIL_START] (hidden states at the two opening markers, Baldini Soares
et al. 2019 / Zhong & Chen 2021) -> dropout -> linear -> {NO_RELATION, positive}. Each
pair has exactly one type-allowed relation, so "positive" means that relation.

Training: scripts/re_dataset/bert_re.py (GPU). A saved model directory holds
  config.json, tokenizer files   (committed)
  model_seed<N>.safetensors      (fp16 weights, one per seed; not in git: see the directory README)
  re_config.json                 (max_len, threshold, seeds, supported relations, provenance)
The extractor averages the positive probability over the seeds and thresholds at 0.5,
exactly as the benchmark scored the method (outputs/re_benchmark_2026-11-08).

BertRelationExtractor has the same interface as RelationExtractor (predict, predict_pairs,
supported_relations, metadata), so HybridRelationExtractor can combine it with the rules.
"""
import json
from pathlib import Path

import torch
from torch import nn

from .data import NEGATIVE, SCHEMA, candidates

TYPES = SCHEMA["entity_types"]
MARKERS = [f"[HEAD_{t}]" for t in TYPES] + [f"[TAIL_{t}]" for t in TYPES] + ["[/HEAD]", "[/TAIL]"]


class PairClassifier(nn.Module):
    def __init__(self, encoder):
        super().__init__()
        self.enc = encoder
        h = encoder.config.hidden_size
        self.drop = nn.Dropout(0.1)
        self.out = nn.Linear(2 * h, 2)

    @classmethod
    def from_base(cls, base, n_tokens):
        from transformers import AutoModel
        enc = AutoModel.from_pretrained(base)
        enc.resize_token_embeddings(n_tokens)
        return cls(enc)

    def forward(self, ids, att, hpos, tpos):
        hs = self.enc(input_ids=ids, attention_mask=att).last_hidden_state
        r = torch.arange(hs.size(0), device=hs.device)
        return self.out(self.drop(torch.cat([hs[r, hpos], hs[r, tpos]], -1)))


def add_markers(tok):
    tok.add_tokens(MARKERS, special_tokens=True)
    return {"HEAD": set(tok.convert_tokens_to_ids([f"[HEAD_{t}]" for t in TYPES])),
            "TAIL": set(tok.convert_tokens_to_ids([f"[TAIL_{t}]" for t in TYPES]))}


def encode(tok, pairs, max_len, start_ids):
    """(input_ids, head_marker_pos, tail_marker_pos, is_positive) per pair."""
    items = []
    for p in pairs:
        ids = tok(p["features"], truncation=True, max_length=max_len)["input_ids"]
        hpos = next((i for i, x in enumerate(ids) if x in start_ids["HEAD"]), 0)
        tpos = next((i for i, x in enumerate(ids) if x in start_ids["TAIL"]), 0)
        items.append((ids, hpos, tpos, int(p.get("label", NEGATIVE) != NEGATIVE)))
    return items


def batches(items, bs, pad, rng=None):
    order = list(range(len(items)))
    if rng:
        rng.shuffle(order)
    for i in range(0, len(order), bs):
        ch = [items[j] for j in order[i:i + bs]]
        n = max(len(c[0]) for c in ch)
        ids = torch.full((len(ch), n), pad, dtype=torch.long)
        att = torch.zeros((len(ch), n), dtype=torch.long)
        for k, c in enumerate(ch):
            ids[k, :len(c[0])] = torch.tensor(c[0])
            att[k, :len(c[0])] = 1
        yield (ids, att, torch.tensor([c[1] for c in ch]), torch.tensor([c[2] for c in ch]),
               torch.tensor([c[3] for c in ch]), order[i:i + bs])


def positive_probs(model, tok, start_ids, pairs, max_len, device, bs=64):
    model.eval()
    items = encode(tok, pairs, max_len, start_ids)
    out = [0.0] * len(items)
    amp = device.type == "cuda"
    with torch.no_grad():
        for ids, att, hp, tp, _, idx in batches(items, bs, tok.pad_token_id):
            with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=amp):
                logits = model(ids.to(device), att.to(device), hp.to(device), tp.to(device))
            for j, v in zip(idx, torch.softmax(logits.float(), -1)[:, 1].cpu().tolist()):
                out[j] = v
    return out


def weights_name(seed):
    return f"model_seed{seed}.safetensors"


def save_member(model, tok, directory, seed):
    """Weights of one seed; the encoder config and tokenizer are shared by all seeds."""
    from safetensors.torch import save_file
    d = Path(directory)
    d.mkdir(parents=True, exist_ok=True)
    model.enc.config.save_pretrained(d)
    tok.save_pretrained(d)
    save_file({k: v.detach().to("cpu", torch.float16).contiguous().clone() for k, v in model.state_dict().items()},
              str(d / weights_name(seed)))


def save_config(directory, re_config):
    (Path(directory) / "re_config.json").write_text(json.dumps(re_config, ensure_ascii=False, indent=2), encoding="utf-8")


class BertRelationExtractor:
    def __init__(self, models, tok, start_ids, config, device):
        """models: the PairClassifier of each seed; probabilities are averaged over them."""
        self.models, self.tok, self.start_ids, self.config, self.device = models, tok, start_ids, config, device
        self.max_len = config["max_len"]
        self.threshold = config.get("threshold", 0.5)
        self.supported_relations = sorted(config["supported_relations"])
        self.metadata = {"label_source": config.get("label_source", "unknown"), "model": "vihealthbert-entity-marker",
                         "seeds": config.get("seeds"),
                         "human_verified": config.get("human_verified", False), "directory": config.get("directory")}

    @classmethod
    def load(cls, directory, device=None):
        from safetensors.torch import load_file
        from transformers import AutoConfig, AutoModel, AutoTokenizer
        d = Path(directory)
        config = json.loads((d / "re_config.json").read_text(encoding="utf-8"))
        files = [d / weights_name(s) for s in config["seeds"]]
        missing = [f.name for f in files if not f.exists()]
        if missing:
            raise FileNotFoundError(f"thiếu {', '.join(missing)} trong {d} (trọng số không có trong git; xem {d / 'README.md'})")
        config["directory"] = str(d)
        tok = AutoTokenizer.from_pretrained(d)
        start_ids = add_markers(tok)  # no-op if already present; returns the marker ids
        enc_cfg = AutoConfig.from_pretrained(d)
        device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        models = []
        for f in files:
            model = PairClassifier(AutoModel.from_config(enc_cfg))
            model.load_state_dict({k: v.float() for k, v in load_file(str(f)).items()})
            models.append(model.to(device).eval())
        return cls(models, tok, start_ids, config, device)

    def predict_pairs(self, pairs):
        if not pairs:
            return []
        idx = [i for i, p in enumerate(pairs) if p["allowed_relation"] in self.supported_relations]
        sub = [pairs[i] for i in idx]
        probs = [0.0] * len(sub)
        for m in self.models:
            probs = [a + b / len(self.models) for a, b in
                     zip(probs, positive_probs(m, self.tok, self.start_ids, sub, self.max_len, self.device))]
        out = [{"label": None, "score": None, "status": "unsupported"} for _ in pairs]
        for i, v in zip(idx, probs):
            out[i] = {"label": pairs[i]["allowed_relation"] if v >= self.threshold else NEGATIVE,
                      "score": float(v), "status": "predicted"}
        return out

    def predict(self, text, entities):
        pairs = candidates(text, entities)
        return [{"head": p["head"]["id"], "tail": p["tail"]["id"],
                 "allowed_relation": p["allowed_relation"], **result}
                for p, result in zip(pairs, self.predict_pairs(pairs))]


def load_extractor(path, device=None):
    """A saved BERT directory (has re_config.json) or a RelationExtractor .joblib file."""
    p = Path(path)
    if p.is_dir():
        return BertRelationExtractor.load(p, device=device)
    from .model import RelationExtractor
    return RelationExtractor.load(p)
