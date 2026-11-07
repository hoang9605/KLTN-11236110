r"""Agreement between label versions of the 600-passage RE set.

Versions: AI draft -> AI second review (2026-10-15) -> gold v1 (human paper review,
2026-11-05). A pair is matched across versions by (passage id, head span, tail span,
allowed relation), so pairs whose entities were deleted or re-cut count as "dropped".

Reported for each AI version against gold v1, on pairs present in both and labelled
(no CHUA_RO) in both:
- observed agreement, Cohen's kappa over the label set (relations + NO_RELATION),
- the 2x2 table positive / NO_RELATION and precision/recall of AI positives.

Caveat (stated in the output): the human reviewer saw the AI labels, so agreement is
an upper bound on what an independent annotator would give.

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/agreement.py --out outputs/re_ai_v2/agreement.json
"""
import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSIONS = {
    "ai_draft": ROOT / "outputs/vietmed_600_RE_review/annotations_draft.jsonl",
    "ai_review": ROOT / "outputs/vietmed_600_RE_review/review_2026_10_15/annotations_reviewed_600.jsonl",
    "gold_v1": ROOT / "data/re_gold_v1/annotations_gold_v1.jsonl",
}
NEG, UNK = "NO_RELATION", "CHUA_RO"


def pairs(path):
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        ents = {e["id"]: e for e in r["entities"]}
        for rel in r["relations"]:
            h, t = ents.get(rel["head"]), ents.get(rel["tail"])
            if h is None or t is None:
                continue
            key = (r["id"], h["start"], h["end"], t["start"], t["end"], rel["allowed_relation"])
            out[key] = rel["label"]
    return out


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return po, (po - pe) / (1 - pe) if pe < 1 else 1.0


def compare(ai, gold):
    common = [k for k in ai if k in gold and ai[k] != UNK and gold[k] != UNK]
    a = [ai[k] for k in common]
    g = [gold[k] for k in common]
    po, k = kappa(a, g)
    pa = [x != NEG for x in a]
    pg = [x != NEG for x in g]
    tp = sum(x and y for x, y in zip(pa, pg))
    fp = sum(x and not y for x, y in zip(pa, pg))
    fn = sum(y and not x for x, y in zip(pa, pg))
    tn = len(common) - tp - fp - fn
    binary_po, binary_k = kappa(pa, pg)
    flips = Counter(f"{x} -> {y}" for x, y in zip(a, g) if x != y)
    return {
        "ai_pairs": len(ai), "gold_pairs": len(gold),
        "dropped_from_ai": sum(k not in gold for k in ai),
        "new_in_gold": sum(k not in ai for k in gold),
        "compared": len(common),
        "observed_agreement": round(po, 4), "cohen_kappa": round(k, 4),
        "binary": {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
                   "observed_agreement": round(binary_po, 4), "cohen_kappa": round(binary_k, 4),
                   "ai_positive_precision": round(tp / (tp + fp), 4) if tp + fp else None,
                   "ai_positive_recall": round(tp / (tp + fn), 4) if tp + fn else None},
        "label_changes": dict(flips.most_common()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    v = {k: pairs(p) for k, p in VERSIONS.items()}
    res = {"versions": {k: str(p.relative_to(ROOT)) for k, p in VERSIONS.items()},
           "caveat": "Người duyệt gold v1 thấy nhãn AI khi duyệt, nên độ đồng thuận là cận trên so với một người gán độc lập.",
           "ai_draft_vs_gold_v1": compare(v["ai_draft"], v["gold_v1"]),
           "ai_review_vs_gold_v1": compare(v["ai_review"], v["gold_v1"]),
           "ai_draft_vs_ai_review": compare(v["ai_draft"], v["ai_review"])}
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for k in ("ai_draft_vs_gold_v1", "ai_review_vs_gold_v1", "ai_draft_vs_ai_review"):
        r = res[k]
        print(f"{k}: compared {r['compared']}, agreement {r['observed_agreement']}, kappa {r['cohen_kappa']}, "
              f"binary kappa {r['binary']['cohen_kappa']}, dropped {r['dropped_from_ai']}, changes {r['label_changes']}")


if __name__ == "__main__":
    main()
