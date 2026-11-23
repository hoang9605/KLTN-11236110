"""Chia câu thành lô cho AI gán nhãn, và kiểm tra file nhãn AI trả về.

Lô đầu vào có cùng nội dung với phiếu của người: mọi thực thể của câu, và mọi cặp ứng viên tính trên
toàn bộ thực thể. Lô không có nhãn luật, không có điểm chọn câu, không có danh sách mention nhiễu.

  make:  .venv\\Scripts\\python.exe -X utf8 -m relation.ai_batches make --split seed --size 100
  check: .venv\\Scripts\\python.exe -X utf8 -m relation.ai_batches check relation/data/ai/seed_b1_passA.jsonl

Định dạng nhãn AI (mỗi câu một dòng):
  {"id": "...", "entities": {"E1": "VALID", "E2": "INVALID"},
   "pairs": {"P1": "located_at", "P2": "NO_RELATION", "P3": null}}   # null khi có thực thể INVALID
"""
import argparse
import json
import sys
from pathlib import Path

from .make_sheet import all_pairs

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
AI = DATA / "ai"
NEGATIVE = "NO_RELATION"


def marked(text, ents):
    for e in sorted(ents, key=lambda e: -e["start"]):
        text = text[:e["start"]] + f"[{e['id']}:{e['label']} " + text[e["start"]:e["end"]] + "]" + text[e["end"]:]
    return text


def item(row):
    ents = [{k: e[k] for k in ("id", "text", "label", "start", "end")} for e in row["entities"]]
    pairs = all_pairs(row)
    return {"id": row["id"], "text": row["text"], "marked_text": marked(row["text"], ents),
            "entities": [{k: e[k] for k in ("id", "text", "label")} for e in ents],
            "pairs": [{"pair_id": f"P{k}", "relation": p["allowed_relation"], "head": p["head"], "tail": p["tail"]}
                      for k, p in enumerate(pairs, 1)]}


def load(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def make(split, size):
    files = {"seed": ["seed_unlabeled.jsonl", "dev_unlabeled.jsonl"], "test": ["test_unlabeled.jsonl"]}[split]
    rows = [r for f in files for r in load(DATA / f)]
    AI.mkdir(parents=True, exist_ok=True)
    items = [item(r) for r in rows]
    out = []
    for b in range(0, len(items), size):
        p = AI / f"{split}_b{b // size + 1}_input.jsonl"
        with open(p, "w", encoding="utf-8") as f:
            for it in items[b:b + size]:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
        out.append((str(p), len(items[b:b + size]), sum(len(i["pairs"]) for i in items[b:b + size])))
    for o in out:
        print(*o)


def check(label_path, input_path=None):
    """Trả về danh sách lỗi; rỗng nghĩa là hợp lệ và đủ."""
    label_path = Path(label_path)
    if input_path is None:
        stem = label_path.name.split("_pass")[0]
        input_path = label_path.parent / f"{stem}_input.jsonl"
    inputs = {r["id"]: r for r in load(input_path)}
    errs, seen = [], set()
    for lab in load(label_path):
        sid = lab.get("id")
        if sid not in inputs:
            errs.append(f"{sid}: không có trong lô"); continue
        if sid in seen:
            errs.append(f"{sid}: trùng"); continue
        seen.add(sid)
        it = inputs[sid]
        ev = lab.get("entities", {})
        for e in it["entities"]:
            if ev.get(e["id"]) not in ("VALID", "INVALID"):
                errs.append(f"{sid} {e['id']}: '{ev.get(e['id'])}'")
        pv = lab.get("pairs", {})
        for p in it["pairs"]:
            ok = ev.get(p["head"]) == "VALID" and ev.get(p["tail"]) == "VALID"
            v = pv.get(p["pair_id"], "MISSING")
            if ok and v not in (p["relation"], NEGATIVE):
                errs.append(f"{sid} {p['pair_id']}: '{v}' phải là {p['relation']} hoặc {NEGATIVE}")
            if not ok and v not in (None, "MISSING"):
                errs.append(f"{sid} {p['pair_id']}: có thực thể INVALID nên phải là null")
    missing = set(inputs) - seen
    if missing:
        errs.append(f"thiếu {len(missing)} câu, ví dụ {sorted(missing)[:3]}")
    return errs


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make"); m.add_argument("--split", required=True); m.add_argument("--size", type=int, default=100)
    c = sub.add_parser("check"); c.add_argument("labels"); c.add_argument("--input")
    a = ap.parse_args()
    if a.cmd == "make":
        make(a.split, a.size)
    else:
        errs = check(a.labels, a.input)
        print("OK" if not errs else f"{len(errs)} lỗi:\n" + "\n".join(errs[:100]))
        sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
