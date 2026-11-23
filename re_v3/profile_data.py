"""Hồ sơ dữ liệu RE: mọi tập đang dùng (train, test) và kho VietMed-NER chưa gán nhãn RE.

Chạy: .venv\\Scripts\\python.exe -X utf8 -m re_v3.profile_data
Đầu ra: re_v3/outputs/data_profile.json (số liệu) và in bảng tóm tắt.
"""
import json
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

from relation_extraction.data import NEGATIVE, RELATIONS, candidates, is_generic
from relation_extraction.rules import RuleRelationExtractor

from . import config

sys.path.insert(0, str(config.ROOT / "scripts" / "re_dataset"))
sys.path.insert(0, str(config.ROOT / "scripts" / "golden_test"))
from benchmark import load_data  # noqa: E402


def gap_words(p):
    a, b = sorted([p["head"], p["tail"]], key=lambda e: e["start"])
    return len(p["text"][a["end"]:b["start"]].split())


def describe(pairs):
    rel = defaultdict(Counter)
    for p in pairs:
        rel[p["allowed_relation"]]["pos" if p["label"] != NEGATIVE else "neg"] += 1
    gaps = defaultdict(list)
    for p in pairs:
        gaps["pos" if p["label"] != NEGATIVE else "neg"].append(gap_words(p))
    sents = {p["group"] for p in pairs}
    pos_sents = {p["group"] for p in pairs if p["label"] != NEGATIVE}
    per_sent = Counter(p["group"] for p in pairs)
    return {
        "sentences": len(sents), "sentences_with_positive": len(pos_sents), "pairs": len(pairs),
        "positives": sum(p["label"] != NEGATIVE for p in pairs),
        "by_relation": {r: dict(rel[r]) for r in RELATIONS},
        "gap_words_median": {k: st.median(v) for k, v in gaps.items() if v},
        "gap_words_mean": {k: round(st.mean(v), 1) for k, v in gaps.items() if v},
        "pairs_per_sentence_max": max(per_sent.values()) if per_sent else 0,
        "sentence_words_median": st.median(len(p["text"].split()) for p in pairs) if pairs else 0,
    }


def mentions(pairs, top=12):
    by_type = defaultdict(Counter)
    pos_type = defaultdict(Counter)
    for p in pairs:
        for e in (p["head"], p["tail"]):
            by_type[e["label"]][e["text"].lower()] += 1
            if p["label"] != NEGATIVE:
                pos_type[e["label"]][e["text"].lower()] += 1
    return {t: {"distinct": len(c), "top": c.most_common(top),
                "top_in_positive": pos_type[t].most_common(8)} for t, c in by_type.items()}


def rule_quality(pairs, rules):
    pred = [r["label"] for r in rules.predict_pairs(pairs)]
    out = {}
    for r in RELATIONS:
        tp = sum(1 for p, y in zip(pairs, pred) if p["allowed_relation"] == r and y == r and p["label"] == r)
        fp = sum(1 for p, y in zip(pairs, pred) if p["allowed_relation"] == r and y == r and p["label"] != r)
        fn = sum(1 for p, y in zip(pairs, pred) if p["allowed_relation"] == r and y != r and p["label"] == r)
        out[r] = {"tp": tp, "fp": fp, "fn": fn}
    return out


def corpus_pool():
    """Câu VietMed-NER (nhãn NER gốc đã map) có ít nhất một cặp ứng viên RE, theo split."""
    from common import entities_from_bio, load_split
    res = {}
    for split in ("train", "validation", "test"):
        rows, _ = load_split(split)
        n_with, n_pairs, by_rel = 0, 0, Counter()
        for r in rows:
            text, ents = entities_from_bio(r["words"], r["labels"])
            ents = [e for e in ents if not is_generic(e)]
            try:
                c = candidates(text, ents)
            except ValueError:
                continue
            if c:
                n_with += 1
                n_pairs += len(c)
                by_rel.update(x["allowed_relation"] for x in c)
        res[split] = {"sentences": len(rows), "sentences_with_candidate_pair": n_with,
                      "candidate_pairs": n_pairs, "by_relation": dict(by_rel)}
    return res


def main():
    train, tests = load_data()
    sets = {"train_gold_v1": [p for p in train if p["source"] == "v1"],
            "train_ai_v2": [p for p in train if p["source"] == "v2"],
            "test_golden_v1_1": tests["v1_1"], "test_random_v1": tests.get("random_v1", [])}
    rules = RuleRelationExtractor()
    groups = {k: {p["group"] for p in v} for k, v in sets.items()}
    overlap = {f"{a}&{b}": len(groups[a] & groups[b]) for a in groups for b in groups if a < b}
    prof = {"sets": {k: describe(v) for k, v in sets.items()},
            "mentions_train": mentions(sets["train_gold_v1"] + sets["train_ai_v2"]),
            "rules_on": {k: rule_quality(v, rules) for k, v in sets.items()},
            "sentence_overlap": overlap}
    try:
        prof["vietmed_pool"] = corpus_pool()
    except Exception as e:  # cache HF có thể không có
        prof["vietmed_pool"] = {"error": repr(e)}
    out = config.OUTPUTS_DIR / "data_profile.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(prof, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(prof, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
