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
--save-model DIR trains the single model used by the pipeline and knowledge graph.

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
from transformers import AutoTokenizer, get_linear_schedule_with_warmup  # noqa: E402

from benchmark import folds, load_data  # noqa: E402
from relation_extraction.bert_model import (PairClassifier, add_markers, batches, encode,  # noqa: E402
                                            positive_probs, save_config, save_member)
from relation_extraction.data import NEGATIVE, RELATIONS  # noqa: E402


def train_predict(a, tok, start_ids, train, tests, seed, device, keep=False):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    model = PairClassifier.from_base(a.base, len(tok)).to(device)
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
    probs = [positive_probs(model, tok, start_ids, pairs, a.max_len, device) for pairs in tests]
    if keep:
        return probs, model
    del model
    torch.cuda.empty_cache()
    return probs


def save_deployed(a, tok, start_ids, both, tests, device):
    """The models the pipeline uses: the benchmark's final method (same data, hyper-parameters
    and seeds; mean probability over the seeds, threshold 0.5), saved so it can be loaded."""
    t0 = time.time()
    gl = list({p["uid"]: p for t in tests.values() for p in t}.values())
    acc = [0.0] * len(gl)
    per_seed = {}
    for seed in a.seeds:
        (pr,), model = train_predict(a, tok, start_ids, both, [gl], seed, device, keep=True)
        save_member(model, tok, a.save_model, seed)
        per_seed[str(seed)] = {p["uid"]: round(v, 6) for p, v in zip(gl, pr)}
        acc = [x + v / len(a.seeds) for x, v in zip(acc, pr)]
        del model
        torch.cuda.empty_cache()
        print(f"seed {seed} saved ({time.time() - t0:.0f}s)", flush=True)
    pr = acc
    pos = sorted({p["allowed_relation"] for p in both if p["label"] != NEGATIVE})
    cfg = {"base": a.base, "max_len": a.max_len, "threshold": 0.5, "seeds": a.seeds,
           "seed_aggregation": "mean probability, threshold 0.5", "epochs": a.epochs, "lr": a.lr,
           "batch": a.batch, "class_weight": "n_neg/n_pos", "pooling": "head/tail start markers",
           "supported_relations": pos, "all_relations": sorted(RELATIONS),
           "train_pairs": len(both), "train_positives": sum(p["label"] != NEGATIVE for p in both),
           "train_data": "RE gold v1 (người duyệt trên giấy, quy ước 05/11/2026) + RE v2 (nhãn AI)",
           "label_source": "gold_v1_reviewed+ai_v2", "human_verified": False,
           "torch": torch.__version__, "trained_on": torch.cuda.get_device_name(0) if device.type == "cuda" else platform.processor(),
           "seconds": round(time.time() - t0), "date": time.strftime("%Y-%m-%d")}
    save_config(a.save_model, cfg)
    preds = {p["uid"]: (p["allowed_relation"] if v >= 0.5 else NEGATIVE) for p, v in zip(gl, pr)}
    probs = {p["uid"]: round(v, 6) for p, v in zip(gl, pr)}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "bert_deployed_predictions.json").write_text(json.dumps(
        {"meta": {**cfg, "model_dir": str(a.save_model)}, "golden_test": preds, "prob": probs, "prob_per_seed": per_seed},
        ensure_ascii=False, indent=0), encoding="utf-8")
    print(json.dumps(cfg, ensure_ascii=False))


def run_augmented(a, tok, start_ids, both, tests, device):
    """Augmentation experiment: the deployed recipe (same hyper-parameters and seeds) trained on
    all VietMed pairs plus extra pairs (e.g. data/re_translated_en_v1, translated English data).
    Extra pairs are training-only. Nothing is saved except the test-set probabilities."""
    from relation_extraction.data import load_pairs
    from train_eval import attach_entities
    extra, audit = load_pairs(a.extra_train, allow_ai=True)
    attach_entities(extra, a.extra_train)
    extra = [p for p in extra if any(p["sample_id"].startswith(x) for x in a.extra_prefix)]
    for p in extra:
        p["source"] = "extra"
        p["uid"] = f"{p['sample_id']}:{p['head']['id']}:{p['tail']['id']}:{p['allowed_relation']}"
    train = both + extra
    t0 = time.time()
    gl = list({p["uid"]: p for t in tests.values() for p in t}.values())
    # Lưu xác suất sau từng seed để chạy tiếp được nếu tiến trình bị ngắt (máy ngủ, job bị dừng).
    # Seed đã có trong file partial và cùng file extra-train thì bỏ qua.
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    partial = out / f"bert_aug_{a.tag}_partial.json"
    per_seed = {}
    if partial.exists():
        saved = json.loads(partial.read_text(encoding="utf-8"))
        if saved.get("extra_train") == str(a.extra_train) and saved.get("extra_pairs") == len(extra):
            per_seed = {s: v for s, v in saved["prob_per_seed"].items() if int(s) in a.seeds}
            print(f"[{a.tag}] resume: seeds {sorted(per_seed)} already done", flush=True)
    for seed in a.seeds:
        if str(seed) in per_seed:
            continue
        pr = train_predict(a, tok, start_ids, train, [gl], seed, device)[0]
        per_seed[str(seed)] = {p["uid"]: round(v, 6) for p, v in zip(gl, pr)}
        partial.write_text(json.dumps({"extra_train": str(a.extra_train), "extra_pairs": len(extra),
                                       "prob_per_seed": per_seed}, ensure_ascii=False), encoding="utf-8")
        print(f"[{a.tag}] seed {seed} done ({time.time() - t0:.0f}s)", flush=True)
    acc = [sum(per_seed[str(s)][p["uid"]] for s in a.seeds) / len(a.seeds) for p in gl]
    from collections import Counter
    meta = {"tag": a.tag, "extra_train": str(a.extra_train), "extra_prefix": a.extra_prefix,
            "extra_pairs": len(extra), "extra_by_label": dict(Counter(f"{p['allowed_relation']}:{p['label']}" for p in extra)),
            "base_pairs": len(both), "base": a.base, "seeds": a.seeds, "epochs": a.epochs, "lr": a.lr, "batch": a.batch,
            "max_len": a.max_len, "seed_aggregation": "mean probability, threshold 0.5",
            "torch": torch.__version__, "device": torch.cuda.get_device_name(0) if device.type == "cuda" else platform.processor(),
            "seconds": round(time.time() - t0), "date": time.strftime("%Y-%m-%d")}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"bert_aug_{a.tag}_predictions.json").write_text(json.dumps(
        {"meta": meta, "prob": {p["uid"]: round(v, 6) for p, v in zip(gl, acc)}, "prob_per_seed": per_seed},
        ensure_ascii=False, indent=0), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False))


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
    ap.add_argument("--save-model", metavar="DIR",
                    help="train the final models (every seed) on all pairs, save them to DIR for the pipeline/KG and "
                         "write its test-set predictions to <out>/bert_deployed_predictions.json")
    ap.add_argument("--extra-train", metavar="JSONL", type=Path,
                    help="augmentation experiment: also train on these annotations (training only), write "
                         "<out>/bert_aug_<tag>_predictions.json; nothing is saved to the model directory")
    ap.add_argument("--extra-prefix", nargs="+", default=["TR-"], help="keep extra rows whose id starts with one of these")
    ap.add_argument("--tag", default="aug")
    a = ap.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(a.base)
    start_ids = add_markers(tok)
    both, tests = load_data()
    if a.extra_train:
        return run_augmented(a, tok, start_ids, both, tests, device)
    if a.save_model:
        return save_deployed(a, tok, start_ids, both, tests, device)
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
