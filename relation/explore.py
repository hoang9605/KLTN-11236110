"""Khảo sát kho VietMed-NER cho RE làm lại: thực thể, cặp ứng viên, cặp dương tiềm năng.

Không đọc nhãn RE cũ nào. Chỉ dùng văn bản và nhãn NER gốc của VietMed-NER.
Kho seed = train + validation; kho test = test.

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.explore
Đầu ra: relation/data/explore.json
"""
import json
import random
import re as regex
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

from relation_extraction.data import RELATIONS, candidates, is_generic
from relation_extraction.rules import CUES, predict_pair

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "golden_test"))
from common import entities_from_bio, load_split  # noqa: E402

OUT = Path(__file__).resolve().parent / "data"
NEAR = 4   # cặp "gần": cách nhau không quá NEAR từ


def gap(text, a, b):
    x, y = sorted((a, b), key=lambda e: e["start"])
    return len(regex.findall(r"\w+", text[x["end"]:y["start"]]))


def has_cue(text, a, b, rel):
    x, y = sorted((a, b), key=lambda e: e["start"])
    between = " " + " ".join(regex.findall(r"\w+", text[x["end"]:y["start"]].lower())) + " "
    return any(f" {c} " in between for c in CUES.get(rel, []))


def load_pool(splits):
    rows = []
    raw_tags = Counter()
    for split in splits:
        data, _ = load_split(split)
        for i, r in enumerate(data):
            raw_tags.update(t.split("-", 1)[1] for t in map(str, r["labels"]) if t.startswith("B-"))
            text, ents = entities_from_bio(r["words"], r["labels"])
            rows.append({"split": split, "idx": i, "text": text, "entities": ents})
    return rows, raw_tags


def profile(rows, rng):
    ent_count, mentions = Counter(), defaultdict(Counter)
    generic = Counter()
    rel = {r: Counter() for r in RELATIONS}
    rel_sent = {r: defaultdict(set) for r in RELATIONS}
    gaps = defaultdict(list)
    examples = defaultdict(list)
    sent_any, sent_strong = 0, 0
    lengths = []
    for s in rows:
        lengths.append(len(s["text"].split()))
        for e in s["entities"]:
            ent_count[e["label"]] += 1
            mentions[e["label"]][e["text"].lower()] += 1
            if is_generic(e):
                generic[e["label"]] += 1
        ents = [e for e in s["entities"] if not is_generic(e)]
        try:
            cands = candidates(s["text"], ents)
        except ValueError:
            continue
        if cands:
            sent_any += 1
        strong_here = False
        for c in cands:
            r, h, t = c["allowed_relation"], c["head"], c["tail"]
            g = gap(s["text"], h, t)
            near, cue = g <= NEAR, has_cue(s["text"], h, t, r)
            rule = predict_pair(s["text"], h, t, r, ents) == r
            rel[r]["pairs"] += 1
            rel[r]["near"] += near
            rel[r]["cue"] += cue
            rel[r]["rule_positive"] += rule
            strong = rule or (near and cue)
            rel[r]["strong"] += strong
            gaps[r].append(g)
            key = (s["split"], s["idx"])
            rel_sent[r]["any"].add(key)
            if strong:
                rel_sent[r]["strong"].add(key)
                strong_here = True
                if len(examples[r]) < 200:
                    examples[r].append(f"{h['text']} → {t['text']} | {s['text']}")
        sent_strong += strong_here
    return {
        "sentences": len(rows),
        "sentence_words_median": st.median(lengths),
        "sentences_with_candidate": sent_any,
        "sentences_with_strong_candidate": sent_strong,
        "entities": dict(ent_count),
        "generic_entities_removed": dict(generic),
        "mentions_distinct": {k: len(v) for k, v in mentions.items()},
        "mentions_top": {k: v.most_common(30) for k, v in mentions.items()},
        "relations": {r: {**dict(rel[r]),
                          "sentences": len(rel_sent[r]["any"]),
                          "sentences_strong": len(rel_sent[r]["strong"]),
                          "gap_median": st.median(gaps[r]) if gaps[r] else None,
                          "gap_le_4_share": round(sum(g <= NEAR for g in gaps[r]) / len(gaps[r]), 2) if gaps[r] else None}
                      for r in RELATIONS},
        "strong_examples": {r: rng.sample(v, min(8, len(v))) for r, v in examples.items()},
    }


def main():
    rng = random.Random(42)
    seed_rows, seed_tags = load_pool(["train", "validation"])
    test_rows, test_tags = load_pool(["test"])
    out = {"raw_vietmed_entity_tags": dict((seed_tags + test_tags).most_common()),
           "seed_pool": profile(seed_rows, rng), "test_pool": profile(test_rows, rng)}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "explore.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
