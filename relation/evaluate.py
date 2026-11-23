"""Chọn cấu hình trên dev, rồi chấm một lần trên test cho cấu hình đã chọn.

Quy tắc chọn định trước: macro F1 trên dev, tính trên các quan hệ dev có cặp dương; bằng nhau thì
chọn cấu hình ít dữ liệu sinh hơn. Test chỉ được chấm cho cấu hình đã chọn và cho các mốc so sánh
(bộ dự đoán luôn dương, bộ luật relation_extraction.rules nếu chạy được).
Xác suất trung bình qua các seed, ngưỡng 0,5. Khoảng tin cậy 95% bằng bootstrap theo câu (2.000 lần).

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.evaluate
Đầu ra: relation/outputs/evaluation.json
"""
import json
import random
from collections import defaultdict
from pathlib import Path

from .ai_batches import load

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
TRAIN = HERE / "outputs" / "train"
OUT = HERE / "outputs" / "evaluation.json"
NEGATIVE = "NO_RELATION"
REL = ["located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage"]
ORDER = ["x0", "x1", "v1", "vall", "x3"]  # theo số cặp sinh tăng dần (bằng điểm thì chọn cấu hình đứng trước)


def gold(rows):
    return {f"{r['id']}:{x['head']}:{x['tail']}:{x['allowed_relation']}": x["label"] for r in rows for x in r["relations"]}


def prf(g, p, keys):
    tp = sum(1 for k in keys if g[k] != NEGATIVE and p[k] == g[k])
    fp = sum(1 for k in keys if p[k] != NEGATIVE and p[k] != g[k])
    fn = sum(1 for k in keys if g[k] != NEGATIVE and p[k] != g[k])
    pr = tp / (tp + fp) if tp + fp else 0.0
    rc = tp / (tp + fn) if tp + fn else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": round(pr, 3), "recall": round(rc, 3),
            "f1": round(2 * pr * rc / (pr + rc), 3) if pr + rc else 0.0}


def scores(g, p, keys=None):
    keys = list(g) if keys is None else keys
    by = {r: [k for k in keys if k.endswith(":" + r)] for r in REL}
    per = {r: {**prf(g, p, ks), "pairs": len(ks), "positives": sum(g[k] != NEGATIVE for k in ks)} for r, ks in by.items() if ks}
    present = [r for r, v in per.items() if v["positives"]]
    return {"micro": prf(g, p, keys), "macro_f1": round(sum(per[r]["f1"] for r in present) / len(present), 3) if present else None,
            "macro_over": present, "per_relation": per, "pairs": len(keys)}


def predict(res, split):
    seeds = sorted(res[split])
    uids = res[split][seeds[0]]
    out = {}
    for u in uids:
        v = sum(res[split][s][u] for s in seeds) / len(seeds)
        out[u] = u.rsplit(":", 1)[1] if v >= 0.5 else NEGATIVE
    return out, seeds


def bootstrap(g, preds, sent_of, n=2000, seed=1):
    sents = sorted(set(sent_of.values()))
    by = defaultdict(list)
    for k, s in sent_of.items():
        by[s].append(k)
    rng = random.Random(seed)
    vals = {name: [] for name in preds}
    for _ in range(n):
        keys = [k for s in (rng.choice(sents) for _ in sents) for k in by[s]]
        for name, p in preds.items():
            vals[name].append(prf(g, p, keys)["f1"])
    return {name: [round(sorted(v)[int(0.025 * n)], 3), round(sorted(v)[int(0.975 * n)], 3)] for name, v in vals.items()}


def main():
    dev_g, test_g = gold(load(DATA / "dev.jsonl")), gold(load(DATA / "test.jsonl"))
    runs = {c: json.loads((TRAIN / f"{c}.json").read_text(encoding="utf-8")) for c in ORDER if (TRAIN / f"{c}.json").exists()}
    dev = {}
    for c, res in runs.items():
        p, seeds = predict(res, "dev")
        dev[c] = {**scores(dev_g, p), "seeds": seeds, "train_pairs": res["train_pairs"], "synthetic_pairs": res["synthetic_pairs"],
                  "complete": len(seeds) == len(res["seeds"])}
    complete = [c for c in ORDER if c in dev and dev[c]["complete"]]
    if not complete:
        raise SystemExit("chưa có cấu hình nào chạy đủ seed")
    best = max(complete, key=lambda c: (dev[c]["macro_f1"] or 0, -ORDER.index(c)))
    tp, _ = predict(runs[best], "test")
    allpos = {k: k.rsplit(":", 1)[1] for k in test_g}
    test_rows = load(DATA / "test.jsonl")
    sel = {r["id"]: r["selection_reason"] for r in load(DATA / "test_unlabeled.jsonl")}
    random_keys = [k for k in test_g if sel.get(k.split(":")[0]) == "random"]
    sent_of = {k: k.split(":")[0] for k in test_g}
    rep = {
        "selection_rule": "macro F1 trên dev, bằng nhau chọn ít dữ liệu sinh hơn", "dev": dev, "chosen": best,
        "configs_incomplete": [c for c in dev if c not in complete],
        "test": {"model": scores(test_g, tp), "always_positive": scores(test_g, allpos),
                 "model_random_sentences": scores(test_g, tp, random_keys) if random_keys else None,
                 "random_sentences": len({k.split(':')[0] for k in random_keys}),
                 "ci95_micro_f1": bootstrap(test_g, {"model": tp, "always_positive": allpos}, sent_of)},
        "test_sentences": len(test_rows),
    }
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"dev_macro_f1": {c: v["macro_f1"] for c, v in dev.items()}, "chosen": best,
                      "test_model_micro": rep["test"]["model"]["micro"], "test_model_macro": rep["test"]["model"]["macro_f1"],
                      "test_always_positive_micro": rep["test"]["always_positive"]["micro"],
                      "ci95": rep["test"]["ci95_micro_f1"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
