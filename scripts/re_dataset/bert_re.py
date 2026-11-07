r"""ViHealthBERT relation classifier with typed entity markers (run in .venv-gpu).

Input: the marked sentence from relation_extraction.data.mark_pair, e.g.
  "[HEAD_CONDITION]đau[/HEAD] ở [TAIL_BODY_PART]vùng bụng[/TAIL] ..."
The marker strings are added to the tokenizer as special tokens. The pair
representation is [h_HEAD_START ; h_TAIL_START] (hidden states at the two opening
markers, as in Baldini Soares et al. 2019 / Zhong & Chen 2021) -> dropout -> linear
-> {NO_RELATION, positive}. Each pair has one type-allowed relation, so "positive"
means that relation; the marker types tell the model which one.

Hyper-parameters are fixed in advance (no tuning on any test data): 10 epochs,
lr 3e-5, batch 16, warmup 10%, weight decay 0.01, class weight n_neg/n_pos for the
positive class, max length 192, fp16. Three seeds per model; probabilities are
averaged over seeds and the threshold is 0.5.

Protocol is identical to benchmark.py: the same 5 grouped CV folds over gold v1 + RE v2,
and a final model trained on all pairs scored on both golden test versions.
Output: <out>/bert_predictions.json  (uid -> label), merged by benchmark.py.

    .venv-gpu\Scripts\python.exe -X utf8 scripts/re_dataset/bert_re.py --out outputs/re_benchmark_2026-11-08
"""
import argparse
import json
import math
import os
import platform
import random
import sys
import time
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import torch  # noqa: E402
from torch import nn  # noqa: E402
from transformers import AutoModel, AutoTokenizer, get_linear_schedule_with_warmup  # noqa: E402

from benchmark import folds, load_data  # noqa: E402
from relation_extraction.data import NEGATIVE, SCHEMA  # noqa: E402

TYPES = SCHEMA["entity_types"]
MARKERS = [f"[HEAD_{t}]" for t in TYPES] + [f"[TAIL_{t}]" for t in TYPES] + ["[/HEAD]", "[/TAIL]"]


class PairClassifier(nn.Module):
    def __init__(self, base, n_tokens):
        super().__init__()
        self.enc = AutoModel.from_pretrained(base)
        self.enc.resize_token_embeddings(n_tokens)
        h = self.enc.config.hidden_size
        self.drop = nn.Dropout(0.1)
        self.out = nn.Linear(2 * h, 2)

    def forward(self, ids, att, hpos, tpos):
        hs = self.enc(input_ids=ids, attention_mask=att).last_hidden_state
        r = torch.arange(hs.size(0), device=hs.device)
        return self.out(self.drop(torch.cat([hs[r, hpos], hs[r, tpos]], -1)))


def encode(tok, pairs, max_len, start_ids):
    items = []
    for p in pairs:
        ids = tok(p["features"], truncation=True, max_length=max_len)["input_ids"]
        hpos = next((i for i, x in enumerate(ids) if x in start_ids["HEAD"]), 0)
        tpos = next((i for i, x in enumerate(ids) if x in start_ids["TAIL"]), 0)
        items.append((ids, hpos, tpos, int(p["label"] != NEGATIVE)))
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


def train_predict(a, tok, start_ids, train, tests, seed, device):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    model = PairClassifier(a.base, len(tok)).to(device)
    tr = encode(tok, train, a.max_len, start_ids)
    npos = sum(x[3] for x in tr)
    w = torch.tensor([1.0, (len(tr) - npos) / max(npos, 1)], device=device)
    lossf = nn.CrossEntropyLoss(weight=w)
    steps = math.ceil(len(tr) / a.batch) * a.epochs
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=0.01)
    sch = get_linear_schedule_with_warmup(opt, int(0.1 * steps), steps)
    scaler = torch.amp.GradScaler("cuda", enabled=device.type == "cuda")
    rng = random.Random(seed)
    pad = tok.pad_token_id
    for _ in range(a.epochs):
        model.train()
        for ids, att, hp, tp, y, _ in batches(tr, a.batch, pad, rng):
            with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=device.type == "cuda"):
                logits = model(ids.to(device), att.to(device), hp.to(device), tp.to(device))
            loss = lossf(logits.float(), y.to(device))
            opt.zero_grad()
            scaler.scale(loss).backward()
            scaler.unscale_(opt)
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(opt)
            scaler.update()
            sch.step()
    model.eval()
    probs = []
    with torch.no_grad():
        for pairs in tests:
            te = encode(tok, pairs, a.max_len, start_ids)
            pr = [0.0] * len(te)
            for ids, att, hp, tp, _, idx in batches(te, 64, pad):
                with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=device.type == "cuda"):
                    logits = model(ids.to(device), att.to(device), hp.to(device), tp.to(device))
                for j, v in zip(idx, torch.softmax(logits.float(), -1)[:, 1].cpu().tolist()):
                    pr[j] = v
            probs.append(pr)
    del model
    torch.cuda.empty_cache()
    return probs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="demdecuong/vihealthbert-base-syllable")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--lr", type=float, default=3e-5)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--max-len", type=int, default=192)
    ap.add_argument("--final-only", action="store_true",
                    help="keep the CV predictions in <out>/bert_predictions.json; retrain the final models and "
                         "predict every current test set (e.g. after adding data/re_test_random_v1)")
    a = ap.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(a.base)
    tok.add_tokens(MARKERS, special_tokens=True)
    start_ids = {"HEAD": set(tok.convert_tokens_to_ids([f"[HEAD_{t}]" for t in TYPES])),
                 "TAIL": set(tok.convert_tokens_to_ids([f"[TAIL_{t}]" for t in TYPES]))}
    both, tests = load_data()
    fl = folds(both)
    t0 = time.time()
    cv = {}
    per_seed_cv = {s: {} for s in a.seeds}
    prev = Path(a.out) / "bert_predictions.json"
    if a.final_only:
        old = json.loads(prev.read_text(encoding="utf-8"))
        cv = old["cv"]
        per_seed_cv = {int(s): v for s, v in old.get("cv_per_seed", {}).items()}
    for k in ([] if a.final_only else range(5)):
        tr = [p for p, f in zip(both, fl) if f != k]
        te = [p for p, f in zip(both, fl) if f == k]
        acc = [0.0] * len(te)
        for s in a.seeds:
            pr = train_predict(a, tok, start_ids, tr, [te], s, device)[0]
            for p, v in zip(te, pr):
                per_seed_cv[s][p["uid"]] = p["allowed_relation"] if v >= 0.5 else NEGATIVE
            acc = [x + v / len(a.seeds) for x, v in zip(acc, pr)]
        for p, v in zip(te, acc):
            cv[p["uid"]] = p["allowed_relation"] if v >= 0.5 else NEGATIVE
        print(f"fold {k} done ({time.time() - t0:.0f}s)", flush=True)
    gt_pairs = {}
    for t in tests.values():
        for p in t:
            gt_pairs[p["uid"]] = p
    gl = list(gt_pairs.values())
    acc = [0.0] * len(gl)
    for s in a.seeds:
        pr = train_predict(a, tok, start_ids, both, [gl], s, device)[0]
        acc = [x + v / len(a.seeds) for x, v in zip(acc, pr)]
    gt = {p["uid"]: (p["allowed_relation"] if v >= 0.5 else NEGATIVE) for p, v in zip(gl, acc)}
    meta = {"base": a.base, "pooling": "head/tail start markers", "epochs": a.epochs, "lr": a.lr, "batch": a.batch,
            "max_len": a.max_len, "seeds": a.seeds, "seed_aggregation": "mean probability, threshold 0.5",
            "class_weight": "n_neg/n_pos", "device": torch.cuda.get_device_name(0) if device.type == "cuda" else platform.processor(),
            "torch": torch.__version__, "seconds": round(time.time() - t0)}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "bert_predictions.json").write_text(json.dumps(
        {"meta": meta, "cv": cv, "golden_test": gt, "cv_per_seed": {str(s): v for s, v in per_seed_cv.items()}},
        ensure_ascii=False, indent=0), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
