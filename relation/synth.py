"""Sinh dữ liệu huấn luyện từ seed đã duyệt (relation/data/seed.jsonl). Chỉ dùng để huấn luyện.

Hai cách sinh, dùng lại hàm của re_v3/synth_pattern.py và từ điển re_v3/lexicon.json:
  - mention_replacement: lấy câu seed, thay một thực thể bằng thực thể cùng kiểu, cùng nhóm chuyên khoa
    với mọi đối tác dương của nó; giữ nguyên nhãn. Không thay DOSAGE.
  - template: điền cặp thực thể cùng nhóm vào mẫu câu viết tay, gồm mẫu dương và mẫu âm khó
    (phòng bệnh, tác dụng phụ, phủ định, thực thể gây nhiễu). Không dùng mẫu khai thác từ nhãn RE cũ.
Lọc: loại câu trùng với seed, dev, test hoặc trùng nhau; loại câu có chung 8-gram với dev hoặc test;
mỗi khung câu giữ tối đa 3 câu; tỉ lệ dương đưa về khoảng tỉ lệ dương của seed.
Rồi lấy mẫu thành hai mức theo số cặp: x1 bằng số cặp seed, x3 bằng ba lần.

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.synth
Đầu ra: relation/data/synth/{pool,x1,x3}.jsonl, relation/data/synth/manifest.json
"""
import json
import random
import re
from collections import Counter
from pathlib import Path

from relation_extraction.data import NEGATIVE, text_group
from re_v3.synth_pattern import Lexicon, balance, mention_replacement, templates

from .ai_batches import load

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
OUT = DATA / "synth"
SEED = 20261120
NGRAM = 8
MAX_PER_SKELETON = 3


def ngrams(text, n=NGRAM):
    w = text.lower().split()
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def skeleton(text, entities):
    for e in sorted(entities, key=lambda e: -e["start"]):
        text = text[:e["start"]] + f"[{e['label']}]" + text[e["end"]:]
    return re.sub(r"\s+", " ", text.lower()).strip()


def npairs(rows):
    return sum(len(r["relations"]) for r in rows)


def main():
    rng = random.Random(SEED)
    lex = Lexicon()
    seed = load(DATA / "seed.jsonl")
    held = load(DATA / "dev.jsonl") + load(DATA / "test.jsonl")
    seed_rows = [{"id": r["id"], "text": r["text"],
                  "entities": [{k: e[k] for k in ("id", "label", "start", "end", "text")} for e in r["entities"]],
                  "relations": [{k: x[k] for k in ("head", "tail", "allowed_relation", "label")} for x in r["relations"]]}
                 for r in seed]
    seed_text = {r["id"]: r["text"] for r in seed}
    raw = mention_replacement(seed_rows, lex, rng, per_sentence=5)
    mr_pos = Counter(x["allowed_relation"] for *_, rels, _ in raw for x in rels if x["label"] != NEGATIVE)
    raw += templates([], lex, rng, positives_per_relation=250, hard_negative_ratio=2.0, existing_pos=mr_pos)

    leak = set().union(*(ngrams(r["text"]) for r in held))
    seen = {text_group(r["text"]) for r in seed + held}
    skel = Counter()
    rows, audit = [], Counter()
    for method, text, entities, relations, meta in raw:
        if not relations:
            continue
        g = text_group(text)
        if g in seen:
            audit["drop_duplicate"] += 1; continue
        if ngrams(text) & leak:
            audit["drop_leak_dev_test"] += 1; continue
        sk = skeleton(text, entities)
        if skel[sk] >= MAX_PER_SKELETON:
            audit["drop_skeleton_cap"] += 1; continue
        skel[sk] += 1
        seen.add(g)
        rows.append({"id": f"SY-{len(rows) + 1:05d}", "method": method, "text": text, "entities": entities,
                     "relations": relations, "annotation_status": "SYNTHETIC_PATTERN", "human_verified": False,
                     "parent_id": meta.get("parent_id"), "template": meta.get("template"),
                     "group": meta.get("group"), "replaced": meta.get("replaced"),
                     "parent_text": seed_text.get(meta.get("parent_id"))})
    seed_pos = sum(x["label"] != NEGATIVE for r in seed for x in r["relations"]) / npairs(seed)
    target = (round(seed_pos - 0.05, 2), round(seed_pos + 0.05, 2))
    before = len(rows)
    rows = balance(rows, rng, target)
    audit["drop_positive_ratio"] = before - len(rows)

    OUT.mkdir(parents=True, exist_ok=True)

    def write(name, rs):
        with open(OUT / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for r in rs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    def stats(rs):
        c = Counter(f"{x['allowed_relation']}:{'neg' if x['label'] == NEGATIVE else 'pos'}" for r in rs for x in r["relations"])
        return {"records": len(rs), "pairs": npairs(rs), "by_method": dict(Counter(r["method"] for r in rs)),
                "pairs_by_label": dict(sorted(c.items()))}

    write("pool", rows)
    order = rows[:]
    rng.shuffle(order)
    manifest = {"seed_pairs": npairs(seed), "seed_positive_rate": round(seed_pos, 3), "target_positive_rate": target,
                "audit": dict(audit), "pool": stats(rows)}
    for name, k in (("x1", 1), ("x3", 3)):
        want, pick, got = k * npairs(seed), [], 0
        for r in order:
            if got >= want:
                break
            pick.append(r); got += len(r["relations"])
        write(name, pick)
        manifest[name] = {**stats(pick), "requested_pairs": want, "short_of_request": got < want}
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
