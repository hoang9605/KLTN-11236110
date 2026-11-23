"""Tiện ích dùng chung: đọc/ghi jsonl, parse câu có thẻ, kiểm tra bản ghi sinh ra."""
import json
import re
import unicodedata
from pathlib import Path

from relation_extraction.data import RELATIONS, NEGATIVE, validate_entities

from . import config


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8-sig").splitlines()
            if line.strip()]


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def norm(text):
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def words(text):
    return re.findall(r"\w+", norm(text))


# Thẻ dạng [E1:CONDITION]đau đầu[/E1] — dùng cho (B) và (C).
TAG = re.compile(r"\[(/?)(E\d+)(?::([A-Z_]+))?\]")


def parse_tagged(tagged):
    """'[E1:CONDITION]đau[/E1] ở [E2:BODY_PART]bụng[/E2]' -> (text, entities)."""
    plain, pos, open_at, entities = "", 0, {}, []
    for m in TAG.finditer(tagged):
        plain += tagged[pos:m.start()]
        pos = m.end()
        closing, eid, label = m.group(1), m.group(2), m.group(3)
        if not closing:
            if eid in open_at or not label:
                raise ValueError(f"thẻ mở lỗi: {m.group(0)}")
            open_at[eid] = (len(plain), label)
        else:
            if eid not in open_at:
                raise ValueError(f"thẻ đóng không có thẻ mở: {eid}")
            start, label = open_at.pop(eid)
            entities.append({"id": eid, "label": label, "start": start, "end": len(plain),
                             "text": plain[start:len(plain)]})
    plain += tagged[pos:]
    if open_at:
        raise ValueError(f"thẻ chưa đóng: {sorted(open_at)}")
    validate_entities(plain, entities)
    return plain, sorted(entities, key=lambda e: e["start"])


def check_record(row):
    """Kiểm tra một bản ghi sinh ra theo đúng định dạng annotation của repo."""
    if row.get("annotation_status") not in config.ANNOTATION_STATUSES:
        raise ValueError(f"{row.get('id')}: annotation_status không hợp lệ")
    if row.get("human_verified") is not False:
        raise ValueError(f"{row.get('id')}: dữ liệu sinh phải có human_verified=false")
    validate_entities(row["text"], row["entities"])
    ents = {e["id"]: e for e in row["entities"]}
    for rel in row["relations"]:
        head, tail = ents[rel["head"]], ents[rel["tail"]]
        types = RELATIONS[rel["allowed_relation"]]
        if (head["label"], tail["label"]) != types:
            raise ValueError(f"{row['id']}: sai kiểu thực thể cho {rel['allowed_relation']}")
        if rel["label"] not in (rel["allowed_relation"], NEGATIVE):
            raise ValueError(f"{row['id']}: nhãn {rel['label']} không hợp lệ")
