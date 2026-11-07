r"""Natural-distribution RE test set from the VietMed-NER *test* split.

The golden test (data/golden_test/v1) was sampled with per-relation quotas, so a third
of its pairs are positive and trivial baselines ("every type-compatible pair is
positive") score well on it. This set samples sentences uniformly instead:

- source: test split; drop sentences whose normalized text is in the golden test or in
  train, and duplicates; drop generic entities (relation_extraction.data.is_generic);
- keep sentences with at least one type-compatible pair (no cap on pairs);
- draw N sentences uniformly at random (seed 20261108) - no relation quota.

Output format = data/re_ai_v2/candidates.jsonl, so merge_labels.py can build the
annotation file. Labels follow the same guideline and conventions as RE v2.

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/build_random_test.py --n 200
"""
import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "golden_test"))

from common import entities_from_bio, load_split, text_group  # noqa: E402
from relation_extraction.data import candidates, is_generic  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20261108)
    ap.add_argument("--out", default=str(ROOT / "data/re_test_random_v1/candidates.jsonl"))
    a = ap.parse_args()
    test, src = load_split("test")
    train, _ = load_split("train")
    train_g = {text_group(" ".join(r["words"])) for r in train}
    gt_g = {text_group(json.loads(l)["text"])
            for l in (ROOT / "data/golden_test/v1/candidates.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
    pool, seen, audit = [], set(), Counter()
    for idx, row in enumerate(test):
        if len(row["words"]) != len(row["labels"]):
            audit["skip_bad_alignment"] += 1; continue
        text, ents = entities_from_bio(row["words"], row["labels"])
        g = text_group(text)
        if g in gt_g:
            audit["skip_in_golden_test"] += 1; continue
        if g in train_g:
            audit["skip_also_in_train"] += 1; continue
        if g in seen:
            audit["skip_duplicate"] += 1; continue
        seen.add(g)
        ents = [e for e in ents if not is_generic(e)]
        for i, e in enumerate(ents, 1):
            e["id"] = f"E{i}"
        pairs = candidates(text, ents)
        if not pairs:
            audit["no_candidate_pair"] += 1; continue
        pool.append({"row": idx, "text": text, "entities": ents,
                     "pairs": [{"head": p["head"]["id"], "tail": p["tail"]["id"], "allowed_relation": p["allowed_relation"]}
                               for p in pairs]})
    rng = random.Random(a.seed)
    chosen = sorted(rng.sample(pool, min(a.n, len(pool))), key=lambda s: s["row"])
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        for i, s in enumerate(chosen, 1):
            for j, p in enumerate(s["pairs"], 1):
                p["id"] = f"R{j}"
            fh.write(json.dumps({"id": f"RT-{i:03d}", "source": "leduckhai/VietMed-NER", "source_split": "test",
                                 "source_row_index": s["row"], "selection": "uniform_random", "text": s["text"],
                                 "entities": s["entities"], "pairs": s["pairs"]}, ensure_ascii=False) + "\n")
    types = Counter(p["allowed_relation"] for s in chosen for p in s["pairs"])
    manifest = {"source": src, "seed": a.seed, "pool_sentences_with_pairs": len(pool),
                "pool_pairs": sum(len(s["pairs"]) for s in pool), "chosen_sentences": len(chosen),
                "chosen_pairs": sum(len(s["pairs"]) for s in chosen), "pairs_by_type": dict(types),
                "pool_pairs_by_type": dict(Counter(p["allowed_relation"] for s in pool for p in s["pairs"])),
                "audit": dict(audit)}
    (out.parent / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
