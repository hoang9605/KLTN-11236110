r"""Re-split all of VietMed-NER (train + validation + test) into 8:1:1 for RE labeling.

- pool: every row of the three original splits; rows whose normalized text was already
  seen are dropped (first occurrence kept), rows with misaligned words/labels are dropped;
- entities: BIO -> target types, generic entities removed (relation_extraction.data.is_generic);
- pairs: type-compatible candidate pairs (relation_extraction.data.candidates);
- stratum: the rarest relation type among a sentence's pairs, or "no_pair";
- each stratum is shuffled (seed) and cut 80/10/10, so every relation keeps the same share
  in train/dev/test.

Sentences with no pair stay in the files (label NO_RELATION by construction, no API call).

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/build_split_811.py
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "golden_test"))

from common import entities_from_bio, load_split, text_group  # noqa: E402
from relation_extraction.data import candidates, is_generic  # noqa: E402

# rarest first (pair counts over the whole corpus)
RARITY = ["diagnosed_by", "has_dosage", "treated_by", "treated_by_procedure", "located_at"]
SPLITS = ("train", "dev", "test")

# existing labeled RE sets, only used to report where their sentences land
EXISTING = {
    "golden_test_v1": "data/golden_test/v1/candidates.jsonl",
    "re_test_random_v1": "data/re_test_random_v1/candidates.jsonl",
    "re_gold_v1": "data/re_gold_v1/annotations_gold_v1.jsonl",
    "re_ai_v2": "data/re_ai_v2/candidates.jsonl",
}


def stratum(pairs):
    if not pairs:
        return "no_pair"
    present = {p["allowed_relation"] for p in pairs}
    return next(r for r in RARITY if r in present)


def cut(n, ratios):
    n_dev = round(n * ratios[1])
    n_test = round(n * ratios[2])
    return n - n_dev - n_test, n_dev, n_test


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261124)
    ap.add_argument("--out", default=str(ROOT / "data/re_vietmed_811_v1"))
    a = ap.parse_args()
    ratios = (0.8, 0.1, 0.1)

    pool, seen, audit, sources = [], set(), Counter(), {}
    for orig in ("train", "validation", "test"):
        rows, src = load_split(orig)
        sources[orig] = src
        for idx, row in enumerate(rows):
            audit[f"rows_{orig}"] += 1
            if len(row["words"]) != len(row["labels"]):
                audit["skip_bad_alignment"] += 1
                continue
            text, ents = entities_from_bio(row["words"], row["labels"])
            g = text_group(text)
            if g in seen:
                audit["skip_duplicate"] += 1
                continue
            seen.add(g)
            ents = [e for e in ents if not is_generic(e)]
            for i, e in enumerate(ents, 1):
                e["id"] = f"E{i}"
            pairs = [{"id": f"R{j}", "head": p["head"]["id"], "tail": p["tail"]["id"],
                      "allowed_relation": p["allowed_relation"]}
                     for j, p in enumerate(candidates(text, ents), 1)]
            pool.append({"source_split": orig, "source_row_index": idx, "group": g, "text": text,
                         "words": row["words"], "entities": ents, "pairs": pairs, "stratum": stratum(pairs)})

    by_stratum = defaultdict(list)
    for s in pool:
        by_stratum[s["stratum"]].append(s)
    rng = random.Random(a.seed)
    assigned = {k: [] for k in SPLITS}
    for key in sorted(by_stratum):
        items = sorted(by_stratum[key], key=lambda s: (s["source_split"], s["source_row_index"]))
        rng.shuffle(items)
        n_tr, n_dev, _ = cut(len(items), ratios)
        assigned["train"] += items[:n_tr]
        assigned["dev"] += items[n_tr:n_tr + n_dev]
        assigned["test"] += items[n_tr + n_dev:]

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    where = {}
    stats = {}
    prefix = {"train": "VMR-TR", "dev": "VMR-DV", "test": "VMR-TE"}
    for split in SPLITS:
        items = sorted(assigned[split], key=lambda s: (s["source_split"], s["source_row_index"]))
        with open(out / f"{split}.jsonl", "w", encoding="utf-8") as fh:
            for i, s in enumerate(items, 1):
                where[s["group"]] = split
                rec = {"id": f"{prefix[split]}-{i:05d}", "source": "leduckhai/VietMed-NER",
                       "source_split": s["source_split"], "source_row_index": s["source_row_index"],
                       "split": split, "stratum": s["stratum"], "text": s["text"], "words": s["words"],
                       "entities": s["entities"], "pairs": s["pairs"]}
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        stats[split] = {
            "sentences": len(items),
            "sentences_with_pairs": sum(1 for s in items if s["pairs"]),
            "sentences_no_pair": sum(1 for s in items if not s["pairs"]),
            "pairs": sum(len(s["pairs"]) for s in items),
            "pairs_by_type": dict(Counter(p["allowed_relation"] for s in items for p in s["pairs"])),
            "from_original_split": dict(Counter(s["source_split"] for s in items)),
        }

    overlap = {}
    for name, rel in EXISTING.items():
        path = ROOT / rel
        if not path.exists():
            continue
        c = Counter()
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                c[where.get(text_group(json.loads(line)["text"]), "not_found")] += 1
        overlap[name] = dict(c)

    manifest = {"sources": sources, "seed": a.seed, "ratios": dict(zip(SPLITS, ratios)),
                "stratify_by": "rarest relation type among candidate pairs, else no_pair",
                "rarity_order": RARITY, "audit": dict(audit), "splits": stats,
                "existing_sets_by_new_split": overlap}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"audit": dict(audit), "splits": stats, "existing": overlap}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
