r"""Select VietMed-NER sentences for the AI-labelled RE dataset v2 (train split only).

Excludes sentences already in RE gold v1 (VM600) and any sentence whose normalized text
also occurs in the test split. Entities are the gold NER spans mapped to the 6 target
types; generic entities (relation_extraction.data.is_generic) are dropped, like the
inference pipeline does. Sentences are sampled per pair type to cover the rare
relations (treated_by, has_dosage, diagnosed_by, treated_by_procedure).

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/build_candidates.py
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

import re

# Second, targeted batch: has_dosage pairs whose DOSAGE looks like a real dose, and
# treated_by pairs with a treatment cue between the two entities. Quota sampling found
# almost none of either (VietMed is spoken podcast text; most DOSAGE spans are 'cao').
DOSE_RE = re.compile(r"\d|mg|ml|\bg\b|gam|viên|lần|giọt|ống|liều|%|phần trăm|mcg|iu", re.I)
CUE_RE = re.compile(r"điều trị|chữa|uống|dùng|kê|tiêm|bôi|sử dụng|cho thuốc|thuốc")

QUOTA = {"treated_by": 60, "has_dosage": 45, "diagnosed_by": 50, "treated_by_procedure": 45, "located_at": 30}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "data/re_ai_v2/candidates.jsonl"))
    ap.add_argument("--max-pairs", type=int, default=6)
    ap.add_argument("--seed", type=int, default=20261107)
    ap.add_argument("--targeted-out", default=str(ROOT / "data/re_ai_v2/candidates_targeted.jsonl"))
    a = ap.parse_args()
    rng = random.Random(a.seed)

    train, _ = load_split("train")
    test, _ = load_split("test")
    test_groups = {text_group(" ".join(r["words"])) for r in test}
    v1 = [json.loads(l) for l in (ROOT / "data/re_gold_v1/annotations_gold_v1.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    v1_groups = {text_group(r["text"]) for r in v1}

    pool, audit, seen = [], Counter(), set()
    for idx, row in enumerate(train):
        if len(row["words"]) != len(row["labels"]):
            audit["skip_bad_alignment"] += 1; continue
        text, ents = entities_from_bio(row["words"], row["labels"])
        g = text_group(text)
        if g in test_groups:
            audit["skip_also_in_test"] += 1; continue
        if g in v1_groups:
            audit["skip_in_re_gold_v1"] += 1; continue
        if g in seen:
            audit["skip_duplicate"] += 1; continue
        seen.add(g)
        ents = [e for e in ents if not is_generic(e)]
        for i, e in enumerate(ents, 1):
            e["id"] = f"E{i}"
        pairs = candidates(text, ents)
        if not pairs:
            continue
        if len(pairs) > a.max_pairs:
            audit["skip_too_many_pairs"] += 1; continue
        pool.append({"row": idx, "text": text, "entities": ents,
                     "types": sorted({p["allowed_relation"] for p in pairs}),
                     "pairs": [{"head": p["head"]["id"], "tail": p["tail"]["id"],
                                "allowed_relation": p["allowed_relation"]} for p in pairs]})
    rng.shuffle(pool)
    chosen, have = [], Counter()
    for rel in sorted(QUOTA, key=lambda r: sum(r in s["types"] for s in pool)):  # rarest first
        for s in pool:
            if have[rel] >= QUOTA[rel]:
                break
            if rel in s["types"] and s not in chosen:
                chosen.append(s)
                have.update(s["types"])
    with open(a.out, "w", encoding="utf-8") as fh:
        for i, s in enumerate(sorted(chosen, key=lambda s: s["row"]), 1):
            for j, p in enumerate(s["pairs"], 1):
                p["id"] = f"R{j}"
            fh.write(json.dumps({"id": f"RV2-{i:03d}", "source": "leduckhai/VietMed-NER", "source_split": "train",
                                 "source_row_index": s["row"], "text": s["text"], "entities": s["entities"],
                                 "pairs": s["pairs"]}, ensure_ascii=False) + "\n")
    def targeted(s):
        ents = {e["id"]: e for e in s["entities"]}
        for p in s["pairs"]:
            h, t = ents[p["head"]], ents[p["tail"]]
            if p["allowed_relation"] == "has_dosage" and DOSE_RE.search(t["text"]):
                return True
            if p["allowed_relation"] == "treated_by" and CUE_RE.search(
                    s["text"][min(h["end"], t["end"]):max(h["start"], t["start"])]):
                return True
        return False
    extra = [s for s in pool if s not in chosen and targeted(s)]
    with open(a.targeted_out, "w", encoding="utf-8") as fh:
        for i, s in enumerate(sorted(extra, key=lambda s: s["row"]), 1):
            for j, p in enumerate(s["pairs"], 1):
                p["id"] = f"R{j}"
            fh.write(json.dumps({"id": f"RV2T-{i:03d}", "source": "leduckhai/VietMed-NER", "source_split": "train",
                                 "source_row_index": s["row"], "selection": "targeted", "text": s["text"],
                                 "entities": s["entities"], "pairs": s["pairs"]}, ensure_ascii=False) + "\n")
    print("targeted", len(extra), "pairs", sum(len(s["pairs"]) for s in extra))
    print("pool", len(pool), "chosen", len(chosen), "pairs", sum(len(s["pairs"]) for s in chosen))
    print("sentences per pair type", dict(have)); print("audit", dict(audit))
    print("available per type", {r: sum(r in s["types"] for s in pool) for r in QUOTA})


if __name__ == "__main__":
    main()
