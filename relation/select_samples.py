"""Chọn câu để gán nhãn RE: 600 câu seed (train + validation VietMed) và 100 câu test (test VietMed).

Chọn chủ động, ưu tiên câu có khả năng chứa quan hệ dương. Chưa có nhãn, nên dùng điểm heuristic:
  - bỏ thực thể chung chung (relation_extraction.data.GENERIC_ENTITIES) và mention trong entity_blocklist.json
  - mỗi cặp ứng viên: +3 nếu luật đoán dương, +1 nếu hai thực thể cách nhau <= 4 từ, +1 nếu có từ gợi ý
  - điểm của câu cho một quan hệ = điểm cặp cao nhất của quan hệ đó

Thứ tự chọn (mỗi kho):
  1. Quan hệ hiếm (has_dosage, diagnosed_by): lấy hết câu có ứng viên hợp lệ, tới hạn mức.
  2. Các quan hệ còn lại: lấy theo điểm giảm dần, tới hạn mức.
  3. Câu ngẫu nhiên trong số câu có ứng viên, để giữ phân bố tự nhiên.
  4. Lấp đầy bằng điểm tổng cao nhất.
Seed: tách DEV_SIZE câu làm dev (ngẫu nhiên, phân tầng theo lý do chọn).
Chống rò rỉ: loại câu seed có chung 8-gram từ với câu test đã chọn.

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.select_samples
Đầu ra: relation/data/{seed,dev,test}_unlabeled.jsonl, relation/data/selection.json
"""
import json
import random
import re as regex
import sys
from collections import Counter, defaultdict
from pathlib import Path

from relation_extraction.data import RELATIONS, candidates, is_generic, text_group
from relation_extraction.rules import CUES, predict_pair

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts" / "golden_test"))
from common import entities_from_bio, load_split  # noqa: E402

DATA = HERE / "data"
SEED = 20261119
NEAR = 4
LEAK_N = 8
DEV_SIZE = 60
PLAN = {
    "seed": {"splits": ["train", "validation"], "size": 600, "random": 60,
             "quota": {"has_dosage": 150, "diagnosed_by": 150, "treated_by": 150,
                       "treated_by_procedure": 150, "located_at": 150}},
    "test": {"splits": ["test"], "size": 100, "random": 15,
             "quota": {"has_dosage": 12, "diagnosed_by": 12, "treated_by": 15,
                       "treated_by_procedure": 15, "located_at": 20}},
}
ORDER = ["has_dosage", "diagnosed_by", "treated_by", "treated_by_procedure", "located_at"]


def words(s):
    return regex.findall(r"\w+", s.lower())


def ngrams(text, n=LEAK_N):
    w = words(text)
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def load_blocklist():
    raw = json.loads((HERE / "entity_blocklist.json").read_text(encoding="utf-8"))
    return {k: set(v) for k, v in raw.items() if not k.startswith("_")}


def build(splits, block):
    out = []
    for split in splits:
        data, meta = load_split(split)
        for i, r in enumerate(data):
            text, ents = entities_from_bio(r["words"], r["labels"])
            for e in ents:
                e["generic"] = is_generic(e)
                e["blocklisted"] = " ".join(e["text"].lower().split()) in block.get(e["label"], ())
            valid = [e for e in ents if not e["generic"] and not e["blocklisted"]]
            try:
                cands = candidates(text, valid)
            except ValueError:
                continue
            if not cands:
                continue
            score = defaultdict(int)
            pairs = []
            for c in cands:
                rel, h, t = c["allowed_relation"], c["head"], c["tail"]
                a, b = sorted((h, t), key=lambda e: e["start"])
                between = " " + " ".join(words(text[a["end"]:b["start"]])) + " "
                gap = len(between.split())
                s = (3 if predict_pair(text, h, t, rel, valid) == rel else 0) + (gap <= NEAR) \
                    + any(f" {cue} " in between for cue in CUES.get(rel, []))
                score[rel] = max(score[rel], s)
                pairs.append({"head": h["id"], "tail": t["id"], "allowed_relation": rel, "gap": gap, "score": s})
            out.append({"id": f"VM-{split[:2].upper()}-{i:05d}", "source_split": split, "source_row_index": i,
                        "text": text, "entities": ents, "candidate_pairs": pairs, "score": dict(score),
                        "total_score": sum(p["score"] for p in pairs)})
    return out


def choose(pool, plan, rng, exclude_grams=None):
    if exclude_grams:
        pool = [s for s in pool if not ngrams(s["text"]) & exclude_grams]
    chosen, reason, seen = [], {}, set()

    def take(s, why):
        g = text_group(s["text"])
        if s["id"] in reason or g in seen or len(chosen) >= plan["size"]:
            return False
        chosen.append(s); reason[s["id"]] = why; seen.add(g)
        return True

    for rel in ORDER:
        have = sum(1 for s in chosen if rel in s["score"])
        ranked = sorted((s for s in pool if rel in s["score"]),
                        key=lambda s: (-s["score"][rel], -s["total_score"], rng.random()))
        for s in ranked:
            if have >= plan["quota"][rel]:
                break
            have += take(s, f"quota:{rel}")
    rest = [s for s in pool if s["id"] not in reason]
    rng.shuffle(rest)
    n = 0
    for s in rest:
        if n >= plan["random"]:
            break
        n += take(s, "random")
    for s in sorted(pool, key=lambda s: (-s["total_score"], rng.random())):
        take(s, "fill")
    for s in chosen:
        s["selection_reason"] = reason[s["id"]]
    return chosen


def summary(rows):
    rel_sent, rel_pairs, strong = Counter(), Counter(), Counter()
    for s in rows:
        for rel in s["score"]:
            rel_sent[rel] += 1
        for p in s["candidate_pairs"]:
            rel_pairs[p["allowed_relation"]] += 1
            strong[p["allowed_relation"]] += p["score"] >= 2
    return {"sentences": len(rows), "candidate_pairs": sum(rel_pairs.values()),
            "reasons": dict(Counter(s["selection_reason"] for s in rows)),
            "sentences_by_relation": {r: rel_sent[r] for r in RELATIONS},
            "pairs_by_relation": {r: rel_pairs[r] for r in RELATIONS},
            "strong_pairs_by_relation (score>=2)": {r: strong[r] for r in RELATIONS},
            "entities_blocklisted": sum(e["blocklisted"] for s in rows for e in s["entities"])}


def write(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    rng = random.Random(SEED)
    block = load_blocklist()
    pools = {k: build(v["splits"], block) for k, v in PLAN.items()}
    test = choose(pools["test"], PLAN["test"], rng)
    test_grams = set().union(*(ngrams(s["text"]) for s in test))
    seed_all = choose(pools["seed"], PLAN["seed"], rng, exclude_grams=test_grams)
    leak_dropped = sum(1 for s in pools["seed"] if ngrams(s["text"]) & test_grams)
    by_reason = defaultdict(list)
    for s in seed_all:
        by_reason[s["selection_reason"]].append(s)
    dev_ids = set()
    for why, lst in sorted(by_reason.items()):
        k = round(DEV_SIZE * len(lst) / len(seed_all))
        dev_ids |= {s["id"] for s in rng.sample(lst, min(k, len(lst)))}
    dev = [s for s in seed_all if s["id"] in dev_ids]
    seed = [s for s in seed_all if s["id"] not in dev_ids]
    DATA.mkdir(parents=True, exist_ok=True)
    write(DATA / "seed_unlabeled.jsonl", seed)
    write(DATA / "dev_unlabeled.jsonl", dev)
    write(DATA / "test_unlabeled.jsonl", test)
    report = {"seed": SEED, "plan": PLAN, "near_words": NEAR, "leak_ngram": LEAK_N,
              "pool_sentences_with_valid_candidate": {k: len(v) for k, v in pools.items()},
              "seed_pool_sentences_sharing_8gram_with_test": leak_dropped,
              "seed": summary(seed), "dev": summary(dev), "test": summary(test)}
    (DATA / "selection.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
