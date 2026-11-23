r"""Chấm mô hình RE đã lưu (nạp lại từ thư mục Model/, như pipeline dùng) trên test_v2, ba cách chạy:
mô hình, bộ luật (relation_extraction.rules), mô hình ∪ luật (knowledge_graph.HybridRelationExtractor, union).

Kiểm tra thêm: xác suất của mô hình nạp lại so với xác suất lúc huấn luyện (relation/outputs/train/<config>_saved.json),
để chắc trọng số đã lưu đúng.

Chạy: .venv-gpu\Scripts\python.exe -X utf8 -m relation.eval_modes Model/vihealthbert-re-vietmed-validated
Đầu ra: relation/outputs/evaluation_test_v2_modes.json
"""
import json
import sys
from pathlib import Path

from relation_extraction.bert_model import load_extractor
from relation_extraction.rules import RuleRelationExtractor

from .ai_batches import load
from .evaluate import DATA, NEGATIVE, TRAIN, bootstrap, gold, scores
from .train import ROOT, pairs_of

OUT = TRAIN.parent / "evaluation_test_v2_modes.json"


def main():
    model_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "Model/vihealthbert-re-vietmed-validated")
    ex = load_extractor(ROOT / model_dir, device="cpu")
    cfg = ex.config
    rows = load(DATA / "test_v2.jsonl")
    g = gold(rows)
    pairs = pairs_of(rows)
    res = ex.predict_pairs(pairs)
    prob = {p["uid"]: r["score"] for p, r in zip(pairs, res)}
    model = {p["uid"]: r["label"] if r["status"] == "predicted" else NEGATIVE for p, r in zip(pairs, res)}

    # đối chiếu với xác suất lúc huấn luyện (test_v2 có cùng cặp với test, chỉ khác nhãn)
    saved = json.loads((TRAIN / f"{cfg['train_config']}_saved.json").read_text(encoding="utf-8"))["test"]
    seeds = sorted(saved)
    train_prob = {u: sum(saved[s][u] for s in seeds) / len(seeds) for u in saved[seeds[0]]}
    common = [u for u in prob if u in train_prob and prob[u] is not None]
    max_dev = max(abs(prob[u] - train_prob[u]) for u in common)
    flips = sum((prob[u] >= 0.5) != (train_prob[u] >= 0.5) for u in common)

    # luật chạy như trong pipeline: RuleRelationExtractor trên cả câu, lấy đúng các cặp cần chấm
    rx = RuleRelationExtractor()
    rules = {}
    for r in rows:
        by = {(p["head"], p["tail"], p["allowed_relation"]): p["label"] for p in rx.predict(r["text"], r["entities"])}
        for x in r["relations"]:
            lab = by.get((x["head"], x["tail"], x["allowed_relation"]))
            rules[f"{r['id']}:{x['head']}:{x['tail']}:{x['allowed_relation']}"] = lab if lab else NEGATIVE
    union = {k: model[k] if model[k] != NEGATIVE else rules[k] for k in g}
    allpos = {k: k.rsplit(":", 1)[1] for k in g}
    preds = {"model": model, "rules": rules, "union": union, "always_positive": allpos}
    rep = {"test_set": "test_v2", "model_dir": model_dir.as_posix(), "train_config": cfg["train_config"],
           "note": f"mô hình nạp từ {model_dir.as_posix()} trên CPU; luật relation_extraction.rules; "
                   "union như knowledge_graph.HybridRelationExtractor",
           "reload_check": {"pairs": len(common), "max_abs_prob_diff": round(max_dev, 6), "label_flips": flips},
           **{n: scores(g, p) for n, p in preds.items()},
           "ci95_micro_f1": bootstrap(g, preds, {k: k.split(":")[0] for k in g})}
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"reload_check": rep["reload_check"]} | {n: rep[n]["micro"] for n in preds}
                     | {"macro": {n: rep[n]["macro_f1"] for n in preds}, "ci95": rep["ci95_micro_f1"]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
