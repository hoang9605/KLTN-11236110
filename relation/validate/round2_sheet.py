"""Round 2 of the expert review: blind sheets for synthetic sentences no expert has seen yet.

Round 1 (expert_review_key.json, 521 rows) was a sample. Every other sentence of the pool is put here, split into
packets of PACKET rows so several reviewers can work in parallel and stop at any packet. Packets are ordered by
priority, and each packet holds one group only, so a finished packet is a random sample of its group:

  1. auto_in_pool               VALID, in the training pool but checked only automatically (most important)
  2. valid_dropped_balance      VALID, left out of the pool by the positive-rate balancing
  3. invalid_implausible_context INVALID because the LLM judged the context implausible (round 1: the expert kept
                                 about four in five of these, so this group can add training data)
  4. invalid_contradicted       INVALID because a source contradicted a positive triple

Sheet format = simple_sheet.py (same two 1/2 columns, nothing from the system is shown).
Existing round 2 files are never overwritten, because they may hold answers.

Run: .venv\\Scripts\\python.exe -X utf8 -m relation.validate.round2_sheet
Output: relation/data/synth/validate/dot2/goi_NN.xlsx, dot2/key.json (group of each packet, not shown to reviewers)
"""
import json
import random
import sys

from .simple_sheet import write_sheet
from .units import OUT, SYNTH, load

DEST = OUT / "dot2"
PACKET = 150
SEED = 20261124
GROUPS = ["auto_in_pool", "valid_dropped_balance", "invalid_implausible_context", "invalid_contradicted"]


def group_of(verdict, reviewed, in_pool):
    sid = verdict["sentence_id"]
    if sid in reviewed:
        return None
    if sid in in_pool:
        return "auto_in_pool"
    if verdict["verdict"] == "VALID":
        return "valid_dropped_balance"
    return f"invalid_{verdict['reason']}"


def main():
    if DEST.exists() and any(DEST.iterdir()):
        sys.exit(f"{DEST} already has files (they may hold answers); move them away first.")
    pool = {r["id"]: r for r in load(SYNTH / "pool.jsonl")}
    reviewed = {k["sentence_id"] for k in json.loads((OUT / "expert_review_key.json").read_text())}
    in_pool = {r["id"] for r in load(SYNTH / "validated" / "pool.jsonl")
               if r["annotation_status"] == "SYNTHETIC_AUTO_VALIDATED"}
    by_group = {g: [] for g in GROUPS}
    for v in load(OUT / "verdicts.jsonl"):
        g = group_of(v, reviewed, in_pool)
        if g is None:
            continue
        if g not in by_group:
            sys.exit(f"unexpected group {g} for {v['sentence_id']}")
        by_group[g].append(v["sentence_id"])

    rng = random.Random(SEED)
    DEST.mkdir(parents=True, exist_ok=True)
    key, n = [], 0
    for g in GROUPS:
        ids = sorted(by_group[g])
        rng.shuffle(ids)
        for start in range(0, len(ids), PACKET):
            n += 1
            chunk = ids[start:start + PACKET]
            name = f"goi_{n:02d}.xlsx"  # neutral name: the reviewer must not see the group
            write_sheet(DEST / name, [pool[s] for s in chunk])
            key += [{"sentence_id": s, "group": g, "packet": name} for s in chunk]
    (DEST / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    print({g: len(v) for g, v in by_group.items()}, f"{n} packets, {len(key)} rows")


if __name__ == "__main__":
    main()
