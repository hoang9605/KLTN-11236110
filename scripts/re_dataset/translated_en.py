r"""English RE data translated to Vietnamese, for a training-data augmentation experiment.

Sources (downloaded to data/external_en_raw/, not redistributed in the report):
  * BioText disease-treatment sentences (Rosario & Hearst, ACL 2004),
    https://biotext.berkeley.edu/data/dis_treat_data.html
  * ADE corpus v2, drug-dosage relation (Gurulingappa et al., 2012),
    https://huggingface.co/datasets/ade-benchmark-corpus/ade_corpus_v2

Steps:
  download -> data/external_en_raw/ (the two public files; gitignored, not redistributed)
  sample  -> data/re_translated_en_v1/source_en.jsonl
             English sentences with entity markers [D]..[/D], [T]..[/T] (BioText) or
             [R]..[/R], [Q]..[/Q] (ADE drug / dosage). Selection is fixed before any
             training or test result is seen (seed 42, rules below).
  build   -> data/re_translated_en_v1/annotations.jsonl
             reads translations_vi.jsonl (same ids, Vietnamese text keeping the markers,
             plus the treatment type DRUG/PROCEDURE), converts markers to offsets and
             writes rows in the RE annotation format. Every row is human_verified: false.

Label mapping (project conventions in docs/HUONG_DAN_HE_THONG.md section 5.2):
  BioText TREAT_FOR_DIS -> treated_by / treated_by_procedure (positive)
  BioText PREVENT       -> NO_RELATION (prevention is not treatment)
  BioText SIDE_EFF      -> NO_RELATION (adverse effect is a cause, not a treatment)
  VAGUE, TREAT_NO_FOR_DIS, TO_SEE, single-role sentences -> not used
  ADE drug-dosage pair  -> has_dosage; other drug/dosage pairs in the same sentence -> NO_RELATION

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/translated_en.py download
    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/translated_en.py sample
    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/translated_en.py build
"""
import argparse
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from relation_extraction.data import validate_entities  # noqa: E402

RAW = ROOT / "data/external_en_raw"
OUT = ROOT / "data/re_translated_en_v1"
SEED = 42
N_TREAT = 100   # positives sampled from TREAT_FOR_DIS
N_ADE = 60      # ADE sentences
MAX_WORDS = 45
BIOTEXT_LABELS = {"TREAT_FOR_DIS": None, "PREVENT": "NO_RELATION", "SIDE_EFF": "NO_RELATION"}
TAG = re.compile(r"<\s*(/?)([A-Z_]+?)\s*>")


def biotext_rows():
    path = RAW / "biotext/sentences_with_roles_and_relations"
    for i, line in enumerate(path.read_text(encoding="latin-1").splitlines()):
        if "||" not in line:
            continue
        sent, label = line.rsplit("||", 1)
        label = label.strip()
        if label not in BIOTEXT_LABELS:
            continue
        opened = [m.group(2) for m in TAG.finditer(sent) if not m.group(1)]
        dis = [t for t in opened if t.startswith("DIS")]
        treat = [t for t in opened if t.startswith("TREAT")]
        if len(dis) != 1 or len(treat) != 1 or any(t.endswith("ONLY") or t == "TO_SEE" for t in opened):
            continue
        marked = TAG.sub(lambda m: "[/" + m.group(2)[0] + "]" if m.group(1) else "[" + m.group(2)[0] + "]", sent)
        marked = " ".join(marked.replace("[D] ", "[D]").replace(" [/D]", "[/D]")
                          .replace("[T] ", "[T]").replace(" [/T]", "[/T]").split())
        marked = re.sub(r"^(OBJECTIVES?|BACKGROUND|CONCLUSIONS?|RESULTS?|METHODS?|PURPOSE|INTERPRETATION|FINDINGS)\s*:\s*",
                        "", marked)
        if len(marked.split()) > MAX_WORDS:
            continue
        yield {"id": f"BT-{i:04d}", "source": "BioText (Rosario & Hearst 2004)", "source_line": i,
               "source_label": label, "en": marked,
               "pairs": [{"head": "D", "tail": "T", "label": "POSITIVE_TREAT" if label == "TREAT_FOR_DIS" else "NO_RELATION"}]}


def ade_rows():
    import pandas as pd
    df = pd.read_parquet(RAW / "ade/drug_dosage.parquet")
    by_text = {}
    for r in df.to_dict("records"):
        by_text.setdefault(r["text"], []).append(r)
    out = []
    for k, (text, rows) in enumerate(sorted(by_text.items())):
        spans = {}
        rows = [r for r in rows if len(r["indexes"]["drug"]["start_char"]) and len(r["indexes"]["dosage"]["start_char"])]
        if not rows:
            continue
        for r in rows:  # first mention of each drug / dosage string
            for key, tag in (("drug", "R"), ("dosage", "Q")):
                s, e = int(r["indexes"][key]["start_char"][0]), int(r["indexes"][key]["end_char"][0])
                spans.setdefault((tag, r[key]), (s, e))
        ordered = sorted(spans.items(), key=lambda x: x[1][0])
        if any(a[1][1] > b[1][0] for a, b in zip(ordered, ordered[1:])) or len(text.split()) > MAX_WORDS:
            continue
        names, marked, pos = {}, "", 0
        counts = Counter()
        for (tag, surface), (s, e) in ordered:
            counts[tag] += 1
            name = f"{tag}{counts[tag]}"
            names[(tag, surface)] = name
            marked += text[pos:s] + f"[{name}]" + text[s:e] + f"[/{name}]"
            pos = e
        marked += text[pos:]
        positive = {(names[("R", r["drug"])], names[("Q", r["dosage"])]) for r in rows}
        pairs = [{"head": d, "tail": q, "label": "has_dosage" if (d, q) in positive else "NO_RELATION"}
                 for d in sorted(n for (t, _), n in names.items() if t == "R")
                 for q in sorted(n for (t, _), n in names.items() if t == "Q")]
        out.append({"id": f"ADE-{k:03d}", "source": "ADE corpus v2 (Gurulingappa et al. 2012)",
                    "source_label": "drug_dosage", "en": marked, "pairs": pairs})
    return out


def sample():
    rng = random.Random(SEED)
    bt = list(biotext_rows())
    pos = [r for r in bt if r["source_label"] == "TREAT_FOR_DIS"]
    neg = [r for r in bt if r["source_label"] != "TREAT_FOR_DIS"]
    rng.shuffle(pos)
    ade = ade_rows()
    rng.shuffle(ade)
    rows = sorted(pos[:N_TREAT], key=lambda r: r["id"]) + sorted(neg, key=lambda r: r["id"]) \
        + sorted(ade[:N_ADE], key=lambda r: r["id"])
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "source_en.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print({"biotext_candidates_positive": len(pos), "biotext_candidates_negative": len(neg),
           "ade_candidates": len(ade), "written": len(rows),
           "by_label": Counter(r["source_label"] for r in rows)})


SOURCES = {
    "biotext/sentences_with_roles_and_relations":
        "https://biotext.berkeley.edu/data/dis_treat_data/sentences_with_roles_and_relations",
    "ade/drug_dosage.parquet": "https://huggingface.co/api/datasets/ade-benchmark-corpus/ade_corpus_v2/parquet/"
                               "Ade_corpus_v2_drug_dosage_relation/train/0.parquet",
}


def download():
    import urllib.request
    for rel, url in SOURCES.items():
        dest = RAW / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            urllib.request.urlretrieve(url, dest)
        print(dest, dest.stat().st_size, "bytes")


MARK = re.compile(r"\[(/?)([A-Z]\d*)\]")


def parse_marked(text):
    """'[D]ung thư[/D] được điều trị bằng [T]hóa trị[/T]' -> (plain text, {name: (start, end)})."""
    plain, spans, open_at, pos = "", {}, {}, 0
    for m in MARK.finditer(text):
        plain += text[pos:m.start()]
        pos = m.end()
        name = m.group(2)
        if m.group(1):
            if name not in open_at:
                raise ValueError(f"closing marker without opening: {name}")
            s = open_at.pop(name)
            if name in spans:
                raise ValueError(f"marker used twice: {name}")
            spans[name] = (s, len(plain))
        else:
            open_at[name] = len(plain)
    plain += text[pos:]
    if open_at:
        raise ValueError(f"unclosed marker: {sorted(open_at)}")
    return plain, spans


def strip_span(plain, s, e):
    while s < e and plain[s] == " ":
        s += 1
    while e > s and plain[e - 1] == " ":
        e -= 1
    return s, e


def build():
    src = {json.loads(line)["id"]: json.loads(line) for line in
           (OUT / "source_en.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()}
    tr = [json.loads(line) for line in (OUT / "translations_vi.jsonl").read_text(encoding="utf-8").splitlines()
          if line.strip()]
    seen, rows, audit, skipped = set(), [], Counter(), []
    for t in tr:
        sid = t["id"]
        if sid in seen or sid not in src:
            raise ValueError(f"{sid}: duplicate or unknown id")
        seen.add(sid)
        s = src[sid]
        if t.get("skip"):
            skipped.append({"id": sid, "reason": "; ".join(t.get("flags", []))})
            continue
        plain, spans = parse_marked(t["vi"])
        plain = " ".join(plain.split()) if plain == " ".join(plain.split()) else plain
        names = sorted({p[k] for p in s["pairs"] for k in ("head", "tail")})
        if sorted(spans) != names:
            raise ValueError(f"{sid}: markers {sorted(spans)} != {names}")
        ttype = t.get("treat_type")
        labels = {"D": "CONDITION", "T": ttype}
        ents, eid = [], {}
        for i, name in enumerate(sorted(spans, key=lambda n: spans[n][0]), 1):
            a, b = strip_span(plain, *spans[name])
            label = labels.get(name) or ("DRUG" if name.startswith("R") else "DOSAGE")
            if label not in ("CONDITION", "DRUG", "PROCEDURE", "DOSAGE"):
                raise ValueError(f"{sid}: bad type {label}")
            eid[name] = f"E{i}"
            ents.append({"id": f"E{i}", "text": plain[a:b], "label": label, "start": a, "end": b})
        validate_entities(plain, ents)
        rels = []
        for p in s["pairs"]:
            label = p["label"]
            if label == "POSITIVE_TREAT":
                label = "treated_by" if ttype == "DRUG" else "treated_by_procedure"
            allowed = {("CONDITION", "DRUG"): "treated_by", ("CONDITION", "PROCEDURE"): "treated_by_procedure",
                       ("DRUG", "DOSAGE"): "has_dosage"}[(labels.get(p["head"], "DRUG") if p["head"] != "D" else "CONDITION",
                                                         labels.get(p["tail"]) or "DOSAGE")]
            rels.append({"head": eid[p["head"]], "tail": eid[p["tail"]], "allowed_relation": allowed, "label": label})
            audit[f"{allowed}:{label}"] += 1
        rows.append({"id": f"TR-{sid}", "source": s["source"], "source_id": sid, "source_label": s["source_label"],
                     "english": s["en"], "text": plain, "entities": ents, "relations": rels,
                     "annotation_status": "TRANSLATED_AI",
                     "annotator": "Nhãn quan hệ từ bộ tiếng Anh gốc; dịch và gán loại DRUG/PROCEDURE bởi AI (Claude Opus 5.5)",
                     "human_verified": False, "training_eligible": False, "review_flags": t.get("flags", [])})
    missing = sorted(set(src) - seen)
    if missing:
        raise ValueError(f"untranslated ids: {missing[:5]} ... ({len(missing)})")
    with open(OUT / "annotations.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest = {"name": "re_translated_en_v1", "rows": len(rows), "pairs": dict(audit),
                "source_sentences": len(src), "skipped": skipped,
                "sources": sorted({r["source"] for r in rows}), "seed": SEED,
                "selection": f"BioText: {N_TREAT} TREAT_FOR_DIS + all PREVENT/SIDE_EFF with one DIS and one TREAT, "
                             f"<= {MAX_WORDS} words; ADE: {N_ADE} drug-dosage sentences, <= {MAX_WORDS} words",
                "style": "lowercase, no punctuation, numbers in words (like VietMed-NER transcripts)",
                "use": "training augmentation only; never used as test data",
                "human_verified": False}
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(manifest)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["download", "sample", "build"])
    {"download": download, "sample": sample, "build": build}[ap.parse_args().step]()
