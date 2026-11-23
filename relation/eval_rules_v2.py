"""So sánh mô hình đã chọn với bộ quy tắc trên tập test gán lại theo tiêu chí chặt (test_v2).

Bổ sung cho evaluate.py: chấm thêm baseline rule-based (relation_extraction.rules) và cách kết hợp
mô hình hợp với rule-based, cùng khoảng tin cậy 95% bootstrap theo câu như evaluate.py.
Chỉ chấm trên test_v2 cho cấu hình đã chọn trên dev (evaluation.json["chosen"]), không chọn lại gì.

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.eval_rules_v2
Đầu ra: relation/outputs/evaluation_test_v2_rules.json
"""
import json

from relation_extraction.rules import predict_pair

from .ai_batches import load
from .evaluate import DATA, NEGATIVE, TRAIN, bootstrap, gold, predict, scores

OUT = TRAIN.parent / "evaluation_test_v2_rules.json"


def rule_preds(rows):
    out = {}
    for r in rows:
        ents = {e["id"]: e for e in r["entities"]}
        for x in r["relations"]:
            k = f"{r['id']}:{x['head']}:{x['tail']}:{x['allowed_relation']}"
            out[k] = predict_pair(r["text"], ents[x["head"]], ents[x["tail"]], x["allowed_relation"], r["entities"])
    return out


def main():
    chosen = json.loads((TRAIN.parent / "evaluation.json").read_text(encoding="utf-8"))["chosen"]
    rows = load(DATA / "test_v2.jsonl")
    g = gold(rows)
    model, _ = predict(json.loads((TRAIN / f"{chosen}.json").read_text(encoding="utf-8")), "test")
    model = {k: model[k] for k in g}
    rules = rule_preds(rows)
    union = {k: model[k] if model[k] != NEGATIVE else rules[k] for k in g}
    allpos = {k: k.rsplit(":", 1)[1] for k in g}
    preds = {"model": model, "rules": rules, "model+rules": union, "always_positive": allpos}
    sent_of = {k: k.split(":")[0] for k in g}
    # khoảng tin cậy của chênh lệch F1 (mô hình trừ rule-based) trên cùng các mẫu bootstrap theo câu
    import random
    from collections import defaultdict
    from .evaluate import prf
    by = defaultdict(list)
    for k, s in sent_of.items():
        by[s].append(k)
    sents, rng, diffs = sorted(by), random.Random(1), []
    for _ in range(2000):
        keys = [k for s in (rng.choice(sents) for _ in sents) for k in by[s]]
        diffs.append(prf(g, model, keys)["f1"] - prf(g, rules, keys)["f1"])
    diffs.sort()
    rep_diff = [round(diffs[50], 3), round(diffs[1949], 3)]
    rep = {"config": chosen, "ci95_diff_model_minus_rules": rep_diff, "test_set": "test_v2", "pairs": len(g), "positives": sum(v != NEGATIVE for v in g.values()),
           **{name: scores(g, p) for name, p in preds.items()},
           "ci95_micro_f1": bootstrap(g, preds, sent_of)}
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({n: rep[n]["micro"] for n in preds} | {"ci95": rep["ci95_micro_f1"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
