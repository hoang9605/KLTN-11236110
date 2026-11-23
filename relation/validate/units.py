"""Step 1: split every synthetic sentence into the units that are checked.

  K1 collocation: a changed entity together with the word right before / after it, when that word is a content
     word (not a function word), and any two entities written next to each other with no gap. Example: the seed
     "nhức đầu" with "đầu" replaced by "tim" gives the K1 unit "nhức tim".
     Changed entity = the replaced entity (mention_replacement) or every filled slot (template, hard_negative).
  K2 relation: every positive pair (head text, relation, tail text). A pair whose two mentions are exactly the
     ones of a human-reviewed seed pair is marked seed_verified and needs no lookup.
  K3 context: the whole sentence (judged later, in English, from a literal translation).

Units are deduplicated: units.jsonl holds one line per distinct unit with the sentence ids using it.

Run: .venv\\Scripts\\python.exe -X utf8 -m relation.validate.units
"""
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
SYNTH = DATA / "synth"
OUT = SYNTH / "validate"
NEGATIVE = "NO_RELATION"

# Words that never form a medical term with a neighbouring entity.
FUNCTION_WORDS = set("""
bị là cái và của thì về trong cho ở có với nó này rất các nhiều hoặc đó hay như nữa lên chúng mà trên rồi để
người nè những một được khi sẽ đã đang thể ta mình họ không cũng nhé ạ ra vào đến từ tại sau trước bằng do vì nên
nhưng thế vậy đây kia ấy gì nào ai sao bao rằng thấy biết làm phải cần muốn nói chỉ còn lại đi qua theo vẫn hơn nhất
khi mỗi mọi cả hai ba bốn năm em anh chị ông bà bạn con bệnh chứng tình trạng nguy cơ loại dạng kiểu giống
xuống tới hết luôn thôi đều ngay thì là
""".split()) | set("""
chứ nhân hiện lần quá khoảng vâng đối đề mới việc dễ thậm lý liên bởi cậu ví xong tượng bên lẽ hoàn ph sĩ mặc cuốn
dậy chưa thêm giờ đấy đơn quả hiệu xem khó vùng thống bảo bác quý trung thiết giấy nếu thành giúp pháp trình cảnh
kiện nối dành sự dùng lúc mặt nguyên tạo tất thực chính trở khiến gồm âu nửa lớn nhỏ đình đồ kê sớm tuy bất thứ
động giác dụng phòng ngừa
""".split())
# The list above was read off the neighbour-frequency table of the pool (2026-11-21): discourse words and
# leftover syllables of the previous word ("nhân" of "bệnh nhân", "hiện" of "xuất hiện"). What remains are words
# that form a term with the entity: "nhức", "đau", "tê bì", "đột quỵ", "ung thư", "uống", "tiêm", "xét nghiệm"...


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def words_around(text, start, end):
    left = text[:start].split()
    right = text[end:].split()
    return (left[-1] if left else None), (right[0] if right else None)


def changed_ids(row):
    if row["method"] == "mention_replacement":
        return {row["replaced"]["entity"]}
    return {e["id"] for e in row["entities"]}


def seed_pairs(seed):
    """(head text, relation, tail text) of human-reviewed positive seed pairs."""
    out = set()
    for r in seed:
        ents = {e["id"]: e["text"].lower() for e in r["entities"]}
        for x in r["relations"]:
            if x["label"] not in (NEGATIVE, "CHUA_RO"):
                out.add((ents[x["head"]], x["label"], ents[x["tail"]]))
    return out


def main():
    pool = load(SYNTH / "pool.jsonl")
    verified = seed_pairs(load(DATA / "seed.jsonl"))
    units = {}
    per_sentence = {}

    def add(key, unit, sid):
        u = units.setdefault(key, {**unit, "sentence_ids": []})
        if sid not in u["sentence_ids"]:
            u["sentence_ids"].append(sid)
        return key

    for row in pool:
        sid, text = row["id"], row["text"]
        ents = sorted(row["entities"], key=lambda e: e["start"])
        changed = changed_ids(row)
        keys = []
        # K1a: changed entity + adjacent content word
        for e in ents:
            if e["id"] not in changed or e["label"] == "DOSAGE":   # drug + dose is checked as K2 has_dosage
                continue
            left, right = words_around(text, e["start"], e["end"])
            covered = {x["start"] for x in ents} | {x["end"] for x in ents}
            for side, w in (("left", left), ("right", right)):
                if not w or w.lower() in FUNCTION_WORDS:
                    continue
                # skip if the neighbour word belongs to another entity: handled by K1b
                pos = e["start"] - 1 if side == "left" else e["end"] + 1
                if any(x["start"] <= pos < x["end"] for x in ents if x is not e):
                    continue
                phrase = f"{w} {e['text']}" if side == "left" else f"{e['text']} {w}"
                keys.append(add(("K1", phrase.lower()), {"kind": "K1", "phrase_vi": phrase.lower(),
                                                         "entity_label": e["label"], "neighbour": w.lower(),
                                                         "side": side}, sid))
        # K1b: two entities written next to each other (one of them changed)
        for a, b in zip(ents, ents[1:]):
            gap = text[a["end"]:b["start"]]
            # Same-type neighbours are spoken enumerations ("đau đầu mỡ máu"), not compounds: left to K3.
            compound = a["label"] != b["label"] and "DOSAGE" not in (a["label"], b["label"])
            if compound and gap.strip() == "" and (a["id"] in changed or b["id"] in changed):
                phrase = f"{a['text']} {b['text']}".lower()
                keys.append(add(("K1", phrase), {"kind": "K1", "phrase_vi": phrase,
                                                 "entity_label": f"{a['label']}+{b['label']}",
                                                 "neighbour": None, "side": "entity_pair"}, sid))
        # K2: positive pairs
        by_id = {e["id"]: e for e in ents}
        for x in row["relations"]:
            if x["label"] == NEGATIVE:
                continue
            h, t = by_id[x["head"]]["text"].lower(), by_id[x["tail"]]["text"].lower()
            triple = (h, x["label"], t)
            keys.append(add(("K2",) + triple, {"kind": "K2", "head_vi": h, "relation": x["label"], "tail_vi": t,
                                               "head_label": by_id[x["head"]]["label"],
                                               "tail_label": by_id[x["tail"]]["label"],
                                               "seed_verified": triple in verified}, sid))
        # K3: whole sentence
        keys.append(add(("K3", sid), {"kind": "K3", "sentence_id": sid, "text_vi": text, "method": row["method"],
                                      "parent_text": row.get("parent_text"), "replaced": row.get("replaced")}, sid))
        per_sentence[sid] = keys

    OUT.mkdir(parents=True, exist_ok=True)
    ids = {}
    with open(OUT / "units.jsonl", "w", encoding="utf-8") as f:
        for i, (key, u) in enumerate(units.items(), 1):
            uid = f"{u['kind']}-{i:05d}"
            ids[key] = uid
            f.write(json.dumps({"unit_id": uid, **u}, ensure_ascii=False) + "\n")
    with open(OUT / "sentence_units.jsonl", "w", encoding="utf-8") as f:
        for sid, keys in per_sentence.items():
            f.write(json.dumps({"sentence_id": sid, "unit_ids": sorted({ids[k] for k in keys})}) + "\n")

    count = defaultdict(int)
    for u in units.values():
        count[u["kind"]] += 1
        if u["kind"] == "K2" and u["seed_verified"]:
            count["K2_seed_verified"] += 1
    print(json.dumps({"sentences": len(pool), "units": dict(count)}, indent=1))


if __name__ == "__main__":
    main()
