r"""Fine-tune a BERT-style encoder for VietMed-NER token classification (37 BIO tags).

Protocol (fixes audit item A15 for the self-trained model):
- train on `train`, evaluate raw micro-F1 on `validation` after every epoch,
  keep the best epoch (early stopping, patience 3), score `test` once at the end;
- every run records per-epoch validation F1, the chosen epoch, max length,
  seed, hardware and wall time in run.json.

Labels go on the first sub-token of each word (others = -100), the same decoding as
ner/predictor.py and eval/evaluate_tier1.py. The inherited checkpoint can be scored
with the same code (--score-checkpoint) for a like-for-like comparison.

    .venv-gpu\Scripts\python.exe -X utf8 scripts/ner_experiments/finetune_bert.py ^
        --base demdecuong/vihealthbert-base-syllable --seeds 42 43 44 ^
        --out eval/ner_selftrained_2026-11-08 --save-dir Model/vihealthbert-ner-selftrained
"""
import argparse
import json
import math
import os
import platform
import random
import statistics
import time
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import numpy as np  # noqa: E402
import torch  # noqa: E402
from transformers import AutoModelForTokenClassification, AutoTokenizer, get_linear_schedule_with_warmup  # noqa: E402

from common_ner import ROOT, label_list, load, save, score, score_both  # noqa: E402


def set_seed(s):
    random.seed(s)
    np.random.seed(s)
    torch.manual_seed(s)
    torch.cuda.manual_seed_all(s)


def encode(tok, words, tags, l2i, max_len):
    ids, labs, first = [tok.bos_token_id], [-100], []
    for i, w in enumerate(words):
        pieces = tok.tokenize(w) or [tok.unk_token]
        pid = tok.convert_tokens_to_ids(pieces)
        if len(ids) + len(pid) >= max_len - 1:
            break
        first.append(len(ids))
        ids.extend(pid)
        labs.extend([l2i.get(tags[i], 0) if tags is not None else 0] + [-100] * (len(pid) - 1))
    ids.append(tok.eos_token_id)
    labs.append(-100)
    return ids, labs, first


def batches(items, bs, shuffle, rng):
    order = list(range(len(items)))
    if shuffle:
        rng.shuffle(order)
    for i in range(0, len(order), bs):
        chunk = [items[j] for j in order[i:i + bs]]
        n = max(len(c[0]) for c in chunk)
        ids = torch.full((len(chunk), n), 1, dtype=torch.long)  # pad id 1 (PhoBERT/RoBERTa)
        att = torch.zeros((len(chunk), n), dtype=torch.long)
        lab = torch.full((len(chunk), n), -100, dtype=torch.long)
        for k, (a, b, _) in enumerate(chunk):
            ids[k, :len(a)] = torch.tensor(a)
            att[k, :len(a)] = 1
            lab[k, :len(b)] = torch.tensor(b)
        yield ids, att, lab, [c[2] for c in chunk], order[i:i + bs]


@torch.no_grad()
def predict(model, tok, data, i2l, max_len, device, bs=32):
    model.eval()
    items = [encode(tok, w, None, {}, max_len) for w, _ in data]
    out = [None] * len(data)
    pad = tok.pad_token_id if tok.pad_token_id is not None else 1
    for ids, att, _, firsts, idx in batches(items, bs, False, None):
        ids[att == 0] = pad
        with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=device.type == "cuda"):
            logits = model(input_ids=ids.to(device), attention_mask=att.to(device)).logits
        pred = logits.argmax(-1).cpu().tolist()
        for k, j in enumerate(idx):
            n = len(data[j][0])
            tags = [i2l[pred[k][p]] for p in firsts[k]]
            out[j] = tags + ["O"] * (n - len(tags))  # words cut by max_len -> O
    return out


def train_one(a, seed, train, val, labels, device):
    set_seed(seed)
    l2i = {l: i for i, l in enumerate(labels)}
    i2l = dict(enumerate(labels))
    tok = AutoTokenizer.from_pretrained(a.base)
    model = AutoModelForTokenClassification.from_pretrained(
        a.base, num_labels=len(labels), id2label=i2l, label2id=l2i).to(device)
    items = [encode(tok, w, t, l2i, a.max_len) for w, t in train]
    truncated = sum(len(f) < len(w) for (w, _), (_, _, f) in zip(train, items))
    steps = math.ceil(len(items) / a.batch) * a.epochs
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=0.01)
    sch = get_linear_schedule_with_warmup(opt, int(0.1 * steps), steps)
    scaler = torch.amp.GradScaler("cuda", enabled=device.type == "cuda")
    rng = random.Random(seed)
    hist, best, bad = [], None, 0
    tmp = Path(a.save_dir) / f"_seed{seed}"
    t0 = time.time()
    for ep in range(1, a.epochs + 1):
        model.train()
        tot = 0.0
        for ids, att, lab, _, _ in batches(items, a.batch, True, rng):
            ids[att == 0] = tok.pad_token_id
            with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=device.type == "cuda"):
                loss = model(input_ids=ids.to(device), attention_mask=att.to(device), labels=lab.to(device)).loss
            opt.zero_grad()
            scaler.scale(loss).backward()
            scaler.unscale_(opt)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(opt)
            scaler.update()
            sch.step()
            tot += loss.item()
        vf = score([t for _, t in val], predict(model, tok, val, i2l, a.max_len, device), with_ci=False)["micro"]["f1"]
        hist.append({"epoch": ep, "train_loss": round(tot, 3), "validation_micro_f1": round(vf, 4),
                     "elapsed_s": round(time.time() - t0)})
        print(f"  seed {seed} epoch {ep}: loss {tot:.1f}, val F1 {vf:.4f} ({time.time() - t0:.0f}s)", flush=True)
        if best is None or vf > best:
            best, bad = vf, 0
            model.save_pretrained(tmp)
            tok.save_pretrained(tmp)
        else:
            bad += 1
            if bad >= a.patience:
                break
    best_ep = max(hist, key=lambda h: h["validation_micro_f1"])["epoch"]
    return tmp, {"seed": seed, "history": hist, "best_epoch": best_ep, "best_validation_micro_f1": best,
                 "train_seconds": round(time.time() - t0), "train_sentences_truncated": truncated}


def score_dir(path, data_by_split, device, max_len):
    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModelForTokenClassification.from_pretrained(path).to(device)
    i2l = {int(k): v for k, v in model.config.id2label.items()}
    i2l = {k: ("O" if v in ("0", "O") else v) for k, v in i2l.items()}
    res = {}
    for split, data in data_by_split.items():
        pred = predict(model, tok, data, i2l, max_len, device)
        res[split] = score_both([t for _, t in data], pred)
    del model
    torch.cuda.empty_cache()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="demdecuong/vihealthbert-base-syllable")
    ap.add_argument("--seeds", type=int, nargs="+", default=[42])
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--patience", type=int, default=3)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--max-len", type=int, default=256)
    ap.add_argument("--out", required=True)
    ap.add_argument("--save-dir", required=True, help="best model of the best seed is kept here")
    ap.add_argument("--score-checkpoint", help="also score this existing checkpoint on validation and test")
    a = ap.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train, val, test = load("train"), load("validation"), load("test")
    labels = label_list(train + val + test)  # label inventory only; no statistics used
    meta = {"base": a.base, "device": torch.cuda.get_device_name(0) if device.type == "cuda" else platform.processor(),
            "torch": torch.__version__, "python": platform.python_version(),
            "hyper": {"epochs_max": a.epochs, "patience": a.patience, "batch": a.batch, "lr": a.lr,
                      "weight_decay": 0.01, "warmup": "10% linear", "max_len": a.max_len, "fp16": device.type == "cuda"},
            "selection": "best epoch by validation raw micro-F1; test scored once after training",
            "data": {"train": len(train), "validation": len(val), "test": len(test)}, "labels": len(labels)}
    print(json.dumps(meta, ensure_ascii=False))
    runs = []
    for seed in a.seeds:
        tmp, info = train_one(a, seed, train, val, labels, device)
        info["scores"] = score_dir(tmp, {"validation": val, "test": test}, device, a.max_len)
        info["model_dir"] = str(tmp)
        print(f"  seed {seed}: best epoch {info['best_epoch']}, test raw F1 {info['scores']['test']['raw']['micro']['f1']:.4f}, "
              f"target F1 {info['scores']['test']['target']['micro']['f1']:.4f}", flush=True)
        runs.append(info)
    # keep the seed with the best VALIDATION score (never test)
    pick = max(runs, key=lambda r: r["best_validation_micro_f1"])
    dest = Path(a.save_dir)
    for f in dest.glob("*"):
        if f.is_file():
            f.unlink()
    for f in Path(pick["model_dir"]).iterdir():
        (dest / f.name).write_bytes(f.read_bytes())
    meta["kept_seed"] = pick["seed"]
    meta["kept_model_dir"] = str(dest)

    def agg(level):
        xs = [r["scores"]["test"][level]["micro"]["f1"] for r in runs]
        return {"mean": statistics.mean(xs), "sd": statistics.stdev(xs) if len(xs) > 1 else 0.0, "values": xs}
    out = {"meta": meta, "runs": runs, "test_micro_f1_over_seeds": {"raw": agg("raw"), "target": agg("target")}}
    if a.score_checkpoint:
        out["inherited_checkpoint"] = {"path": a.score_checkpoint,
                                       "scores": score_dir(a.score_checkpoint, {"validation": val, "test": test}, device, a.max_len)}
        c = out["inherited_checkpoint"]["scores"]["test"]
        print(f"inherited checkpoint: test raw F1 {c['raw']['micro']['f1']:.4f}, target F1 {c['target']['micro']['f1']:.4f}")
    save(out, Path(a.out) / f"run_{Path(a.base).name}.json")
    (Path(a.save_dir) / "selftrained_run.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
