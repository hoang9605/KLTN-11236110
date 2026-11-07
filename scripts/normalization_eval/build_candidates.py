r"""Build the normalization gold candidate set from VietMed-NER gold entities.

Unit = one unique normalized surface form per (label, split), with its mention
frequency and up to 3 context sentences. Gold NER spans are used (not model
output) so normalization is evaluated independently of NER errors.

Splits: `validation` -> dev (rules/synonyms may be tuned on it),
        `test`       -> held-out test (report only, never tune).
Forms that also occur in the other split are kept in both; the overlap is
reported in the manifest.

Usage:
    .venv\Scripts\python.exe -X utf8 scripts/normalization_eval/build_candidates.py
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "golden_test"))

from common import entities_from_bio, load_split  # noqa: E402
from normalization.icd10 import normalize_vietnamese_text  # noqa: E402

LABELS = ("CONDITION", "DRUG")
SPLITS = {"dev": "validation", "test": "test"}


def collect(split):
    rows, src = load_split(split)
    forms = defaultdict(lambda: {"freq": 0, "surfaces": defaultdict(int), "contexts": []})
    for idx, row in enumerate(rows):
        if len(row["words"]) != len(row["labels"]):
            continue
        text, ents = entities_from_bio(row["words"], row["labels"])
        for e in ents:
            if e["label"] not in LABELS:
                continue
            key = (e["label"], normalize_vietnamese_text(e["text"]))
            if not key[1]:
                continue
            f = forms[key]
            f["freq"] += 1
            f["surfaces"][e["text"]] += 1
            if len(f["contexts"]) < 3:
                f["contexts"].append({"row": idx, "text": text, "start": e["start"], "end": e["end"]})
    return forms, src


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "data" / "norm_gold_v1"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"source": "leduckhai/VietMed-NER", "unit": "unique normalized surface form per label",
                "splits": {}}
    all_forms = {}
    for name, split in SPLITS.items():
        forms, src = collect(split)
        all_forms[name] = forms
        items = sorted(forms.items(), key=lambda kv: (kv[0][0], -kv[1]["freq"], kv[0][1]))
        with open(out / f"candidates_{name}.jsonl", "w", encoding="utf-8") as fh:
            for i, ((label, form), f) in enumerate(items, 1):
                surface = max(f["surfaces"].items(), key=lambda kv: kv[1])[0]
                fh.write(json.dumps({
                    "id": f"N{name[0].upper()}-{i:04d}", "split": name, "label": label,
                    "form": form, "surface": surface, "freq": f["freq"],
                    "contexts": f["contexts"]}, ensure_ascii=False) + "\n")
        manifest["splits"][name] = {
            "hf_split": split, "source": src,
            **{lab: {"unique_forms": sum(1 for k in forms if k[0] == lab),
                     "mentions": sum(v["freq"] for k, v in forms.items() if k[0] == lab)}
               for lab in LABELS}}
    overlap = set(all_forms["dev"]) & set(all_forms["test"])
    manifest["dev_test_form_overlap"] = {lab: sum(1 for k in overlap if k[0] == lab) for lab in LABELS}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
