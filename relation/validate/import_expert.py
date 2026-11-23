"""Step 7: read the filled expert sheet, build the validated pool and the x1 / x3 training sets.

Final pool:
  - sentences on the sheet: KEEP -> kept, FIX_LABEL -> kept with fixed_pairs applied, DROP -> removed;
  - sentences not on the sheet: kept if the system verdict is VALID, removed if INVALID.
Then the positive rate is brought back into the seed range and x1 / x3 are sampled as in relation/synth.py.
It also reports the precision of the automatic verdicts on the sampled rows (expert decision as reference).

Run: .venv\\Scripts\\python.exe -X utf8 -m relation.validate.import_expert [path/to/expert_review.xlsx]
Outputs: relation/data/synth/validated/{pool,x1,x3}.jsonl, manifest.json
"""
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

from re_v3.synth_pattern import balance

from .units import DATA, OUT, SYNTH, load

DEST = SYNTH / "validated"
SEED = 20261121
RELATIONS = {"located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage", "NO_RELATION"}


def parse_fix(text):
    out = {}
    for part in filter(None, (p.strip() for p in re.split(r"[;\n]", text or ""))):
        m = re.fullmatch(r"(E\d+)\s*-\s*(E\d+)\s*=\s*(\w+)", part)
        if not m or m.group(3) not in RELATIONS:
            raise ValueError(f"bad fixed_pairs item: {part!r}")
        out[m.group(1), m.group(2)] = m.group(3)
    return out


def npairs(rows):
    return sum(len(r["relations"]) for r in rows)


def main():
    simple = OUT / "phieu_duyet_chuyen_gia.xlsx"
    sheet = Path(sys.argv[1]) if len(sys.argv) > 1 else simple if simple.exists() else OUT / "expert_review.xlsx"
    pool = {r["id"]: r for r in load(SYNTH / "pool.jsonl")}
    verdict = {v["sentence_id"]: v for v in load(OUT / "verdicts.jsonl")}
    key = {k["sentence_id"]: k["selected_as"] for k in json.loads((OUT / "expert_review_key.json").read_text())}

    wb = load_workbook(sheet, read_only=True)
    decisions, errors = {}, []
    if "duyet" in wb.sheetnames:
        # simple sheet (simple_sheet.py): kept only if both answers are Valid
        rows = wb["duyet"].iter_rows(min_row=2, values_only=True)
        for sid, stt, _, _, ok_sent, ok_rel, _note in rows:
            if not sid:
                continue
            # 1 = Valid, 2 = Invalid (the words are accepted too)
            code = {"1": "Valid", "1.0": "Valid", "valid": "Valid", "2": "Invalid", "2.0": "Invalid", "invalid": "Invalid"}
            a, b = (code.get(str(x if x is not None else "").strip().lower(), "") for x in (ok_sent, ok_rel))
            if not a or not b:
                errors.append(f"STT {stt}: answer missing or not 1/2 ({ok_sent!r}, {ok_rel!r})")
                continue
            decisions[sid] = ("KEEP" if a == b == "Valid" else "DROP", {})
        rows = []
    else:
        ws = wb["review"]
        header = [c.value for c in next(ws.iter_rows(max_row=1))]
        col = {h: i for i, h in enumerate(header)}
        rows = ws.iter_rows(min_row=2, values_only=True)
    for row in rows:
        sid, dec = row[col["sentence_id"]], (row[col["expert_decision"]] or "").strip().upper()
        if not sid:
            continue
        if dec not in ("KEEP", "FIX_LABEL", "DROP"):
            errors.append(f"{sid}: expert_decision empty or invalid ({dec!r})"); continue
        try:
            fix = parse_fix(row[col["fixed_pairs"]]) if dec == "FIX_LABEL" else {}
        except ValueError as e:
            errors.append(f"{sid}: {e}"); continue
        if dec == "FIX_LABEL" and not fix:
            errors.append(f"{sid}: FIX_LABEL without fixed_pairs"); continue
        decisions[sid] = (dec, fix)
    missing = set(key) - set(decisions)
    if errors or missing:
        print("\n".join(errors[:30]))
        print(f"{len(errors)} errors, {len(missing)} rows without a decision; nothing written.")
        sys.exit(1)

    kept = []
    for sid, r in pool.items():
        r = json.loads(json.dumps(r))
        if sid in decisions:
            dec, fix = decisions[sid]
            if dec == "DROP":
                continue
            for x in r["relations"]:
                if (x["head"], x["tail"]) in fix:
                    x["label"] = fix[x["head"], x["tail"]]
            r["annotation_status"] = "SYNTHETIC_EXPERT_CHECKED"
            r["human_verified"] = True
        elif verdict[sid]["verdict"] == "VALID":
            r["annotation_status"] = "SYNTHETIC_AUTO_VALIDATED"
        else:
            continue
        kept.append(r)

    # precision of the automatic verdict on the sampled rows
    prec = {}
    for group, ok in (("sample_valid", {"KEEP", "FIX_LABEL"}), ("sample_wrong", {"DROP"}), ("all_not_found", {"DROP"})):
        rows = [sid for sid, g in key.items() if g == group]
        if rows:
            prec[group] = {"rows": len(rows), "expert_agrees_with_system": sum(decisions[s][0] in ok for s in rows),
                           "rate": round(sum(decisions[s][0] in ok for s in rows) / len(rows), 3)}

    rng = random.Random(SEED)
    seed = load(DATA / "seed.jsonl")
    seed_pos = sum(x["label"] != "NO_RELATION" for r in seed for x in r["relations"]) / npairs(seed)
    target = (round(seed_pos - 0.05, 2), round(seed_pos + 0.05, 2))
    balanced = balance(kept, rng, target)

    DEST.mkdir(parents=True, exist_ok=True)

    def write(name, rs):
        with open(DEST / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for r in rs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    def stats(rs):
        c = Counter(f"{x['allowed_relation']}:{'neg' if x['label'] == 'NO_RELATION' else 'pos'}"
                    for r in rs for x in r["relations"])
        return {"records": len(rs), "pairs": npairs(rs), "by_method": dict(Counter(r["method"] for r in rs)),
                "by_status": dict(Counter(r["annotation_status"] for r in rs)), "pairs_by_label": dict(sorted(c.items()))}

    write("pool", balanced)
    manifest = {"expert_decisions": dict(Counter(d for d, _ in decisions.values())),
                "verdict_precision": prec, "kept_before_balance": len(kept),
                "dropped_by_balance": len(kept) - len(balanced), "pool": stats(balanced)}
    order = balanced[:]
    rng.shuffle(order)
    for name, k in (("x1", 1), ("x3", 3)):
        want, pick, got = k * npairs(seed), [], 0
        for r in order:
            if got >= want:
                break
            pick.append(r); got += len(r["relations"])
        write(name, pick)
        manifest[name] = {**stats(pick), "requested_pairs": want, "short_of_request": got < want}
    (DEST / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
