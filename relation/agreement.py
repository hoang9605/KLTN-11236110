"""Độ đồng thuận giữa nhãn người (relation/data/test.jsonl, từ import_sheet.py) và nhãn AI độc lập
(relation/data/ai/test_b1_passA.jsonl) trên tập test.

Quy tắc định trước (docs/KE_HOACH_LAM_LAI_RE.md): kappa của bước B >= 0,6 thì nhãn AI được dùng cho seed.
Kappa bước B tính trên các cặp mà cả người và AI đều coi hai thực thể là VALID (dương/âm).

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.agreement
Đầu ra: relation/data/ai_agreement_test.json
"""
import json
from collections import Counter
from pathlib import Path

from sklearn.metrics import cohen_kappa_score

from .ai_batches import load

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
NEGATIVE = "NO_RELATION"
THRESHOLD = 0.6


def kappa(a, b):
    if not a:
        return None
    return 1.0 if len(set(a) | set(b)) < 2 else round(float(cohen_kappa_score(a, b)), 3)


def main():
    human = {r["id"]: r for r in load(DATA / "test.jsonl")}
    ai = {r["id"]: r for r in load(DATA / "ai" / "test_b1_passA.jsonl")}
    key = {r["id"]: r for r in load(DATA / "test_sheet_key.jsonl")}
    eh, ea, ph, pa = [], [], [], []
    by_rel, confusion, examples = {}, Counter(), []
    for sid, h in human.items():
        a = ai[sid]
        hv = {e["id"]: e["validity"] for e in h["entities"]}
        for eid, v in hv.items():
            eh.append(v); ea.append(a["entities"][eid])
        hl = {(r["head"], r["tail"]): r["label"] for r in h["relations"]}
        for p in key[sid]["pairs"]:
            x = hl.get((p["head"], p["tail"]))
            y = a["pairs"].get(p["pair_id"])
            confusion[(x or "SKIP", y or "SKIP")] += 1
            if x is None or y is None:
                continue
            ph.append(x != NEGATIVE); pa.append(y != NEGATIVE)
            v = by_rel.setdefault(p["allowed_relation"], ([], []))
            v[0].append(x != NEGATIVE); v[1].append(y != NEGATIVE)
            if x != y and len(examples) < 40:
                examples.append({"id": sid, "pair": p["pair_id"], "human": x, "ai": y, "text": h["text"]})
    k = kappa(ph, pa)
    report = {"sentences": len(human),
              "entity_kappa": kappa(eh, ea), "entity_agreement": round(sum(x == y for x, y in zip(eh, ea)) / len(eh), 3),
              "pairs_compared": len(ph), "pair_kappa": k,
              "pair_agreement": round(sum(x == y for x, y in zip(ph, pa)) / len(ph), 3) if ph else None,
              "pair_kappa_by_relation": {r: {"n": len(v[0]), "kappa": kappa(*v), "pos_human": sum(v[0]), "pos_ai": sum(v[1])}
                                         for r, v in sorted(by_rel.items())},
              "confusion_human_vs_ai": {f"{a}|{b}": n for (a, b), n in sorted(confusion.items())},
              "threshold": THRESHOLD, "ai_labels_usable_for_seed": k is not None and k >= THRESHOLD,
              "disagreement_examples": examples}
    (DATA / "ai_agreement_test.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k2: v for k2, v in report.items() if k2 != "disagreement_examples"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
