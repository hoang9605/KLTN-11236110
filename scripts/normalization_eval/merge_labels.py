r"""Merge a label TSV (id <TAB> codes|NIL <TAB> note) into the candidate JSONL -> gold JSONL.

The first code is the primary (most specific justified) code; the rest are also
accepted. NIL = no concept in the target ontology fits (generic word, drug class,
non-medical, NER fragment). Codes are validated against the ICD-10 catalog;
RxCUIs are not validated here (no network needed).

Usage:
    .venv\Scripts\python.exe -X utf8 scripts/normalization_eval/merge_labels.py ^
        --candidates data/norm_gold_v1/candidates_test.jsonl ^
        --labels data/norm_gold_v1/ai_labels_test.tsv --annotator "AI (Claude Opus 5.5)" ^
        --out data/norm_gold_v1/gold_test.jsonl
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--annotator", required=True)
    ap.add_argument("--human-verified", action="store_true",
                    help="đánh dấu nhãn đã được bác sĩ/người duyệt xác nhận")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    labels = {}
    for line in Path(a.labels).read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        labels[parts[0]] = (parts[1].strip(), parts[2].strip() if len(parts) > 2 else "")

    from normalization.icd10 import ICD10Normalizer
    code_map = ICD10Normalizer().code_map

    rows, errors = [], []
    for line in Path(a.candidates).read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["id"] not in labels:
            errors.append(f"{r['id']}: missing label")
            continue
        codes, note = labels.pop(r["id"])
        gold = [] if codes == "NIL" else [c.strip() for c in codes.split(",") if c.strip()]
        if r["label"] == "CONDITION":
            errors += [f"{r['id']}: {c} not in ICD-10 catalog" for c in gold if c not in code_map]
        r.update({"ontology": "ICD-10" if r["label"] == "CONDITION" else "RxNorm",
                  "gold_codes": gold, "nil": not gold, "note": note,
                  "annotator": a.annotator, "human_verified": a.human_verified})
        rows.append(r)
    errors += [f"{k}: label without candidate" for k in labels]
    if errors:
        sys.exit("\n".join(errors))
    with open(a.out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows -> {a.out}")


if __name__ == "__main__":
    main()
