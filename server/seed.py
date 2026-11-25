r"""Nạp kết quả đã chạy sẵn (results.jsonl của scripts/build_kg.py) vào CSDL, không cần chạy mô hình.

    python -m server.seed outputs/kg_test_2026-11-25/results.jsonl
    docker compose exec api python -m server.seed /app/seed/results.jsonl
"""
import argparse
import json
from pathlib import Path

from .config import get_settings
from .db import Database
from .engine import jsonable


def read_results(path):
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            result = row.get("result", row)  # build_kg.py bọc kết quả trong {"id", "result"}
            if "text" in result and "entities" in result:
                yield str(row.get("id", i)), jsonable(result)


def seed(db, path, batch=500):
    n, buf = 0, []
    for item in read_results(path):
        buf.append(item)
        if len(buf) >= batch:
            db.add_many(buf)
            n, buf = n + len(buf), []
    if buf:
        db.add_many(buf)
        n += len(buf)
    return n


def seed_if_empty(db, path):
    if not path or not Path(path).exists() or db.count() > 0:
        return 0
    return seed(db, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--force", action="store_true", help="nạp cả khi CSDL đã có dữ liệu")
    a = ap.parse_args()
    db = Database(get_settings().database_url)
    db.create_all()
    if db.count() and not a.force:
        raise SystemExit(f"CSDL đã có {db.count()} văn bản; dùng --force để nạp thêm.")
    print(f"Đã nạp {seed(db, a.path)} văn bản.")


if __name__ == "__main__":
    main()
