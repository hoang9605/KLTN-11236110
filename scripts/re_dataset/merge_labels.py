r"""Merge compact RE labels into annotation JSONL (the format relation_extraction.data.load_pairs reads).

Label file: one line per sentence, "<num> <l1> <l2> ... [# note]" with one label per
candidate pair in order: 1 = the pair's allowed relation, 0 = NO_RELATION, ? = CHUA_RO
(unclear; excluded from training and evaluation by load_pairs).

Checks: every sentence labelled exactly once, label count equals pair count.

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/merge_labels.py ^
        --candidates data/re_ai_v2/candidates.jsonl --labels data/re_ai_v2/labels_main.txt ^
        --candidates data/re_ai_v2/candidates_targeted.jsonl --labels data/re_ai_v2/labels_targeted.txt ^
        --out data/re_ai_v2/annotations_ai_v2.jsonl
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

CODE = {"0": "NO_RELATION", "?": "CHUA_RO"}


def parse_labels(path):
    out = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        body, _, note = line.partition("#")
        num, *labels = body.split()
        if num in out:
            raise ValueError(f"{path}: sentence {num} labelled twice")
        out[num] = (labels, note.strip())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", action="append", required=True)
    ap.add_argument("--labels", action="append", required=True)
    ap.add_argument("--annotator", default="AI (Claude Opus 5.5), 2 lượt + đối chiếu luật")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if len(a.candidates) != len(a.labels):
        ap.error("--candidates and --labels must be given in pairs")

    rows, counts, errors = [], Counter(), []
    for cand_path, lab_path in zip(a.candidates, a.labels):
        labels = parse_labels(lab_path)
        for line in Path(cand_path).read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            num = r["id"].split("-")[-1]
            if num not in labels:
                errors.append(f"{r['id']}: no labels"); continue
            labs, note = labels.pop(num)
            if len(labs) != len(r["pairs"]):
                errors.append(f"{r['id']}: {len(labs)} labels for {len(r['pairs'])} pairs"); continue
            rels = []
            for p, lab in zip(r["pairs"], labs):
                if lab not in ("0", "1", "?"):
                    errors.append(f"{r['id']} {p['id']}: bad label {lab!r}"); continue
                label = p["allowed_relation"] if lab == "1" else CODE[lab]
                counts[(p["allowed_relation"], label)] += 1
                rels.append({"head": p["head"], "tail": p["tail"], "allowed_relation": p["allowed_relation"],
                             "label": label})
            rows.append({"id": r["id"], "source": r["source"], "source_split": r["source_split"],
                         "source_row_index": r["source_row_index"], "selection": r.get("selection", "quota"),
                         "text": r["text"], "entities": r["entities"], "relations": rels,
                         "annotation_status": "AI_LABELED_TWO_PASS", "annotator": a.annotator,
                         "note": note or None, "human_verified": False, "training_eligible": False,
                         "review_flags": []})
        errors += [f"{lab_path}: label for unknown sentence {k}" for k in labels]
    if errors:
        sys.exit("\n".join(errors))
    with open(a.out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} sentences -> {a.out}")
    for (rel, lab), n in sorted(counts.items()):
        print(f"  {rel:22} {lab:22} {n}")


if __name__ == "__main__":
    main()
