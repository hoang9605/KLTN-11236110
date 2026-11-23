"""Nhập phiếu Excel đã gán (make_sheet.py) thành jsonl, kèm kiểm tra.

Kiểm tra:
  - mọi mention có label VALID hoặc INVALID
  - mọi cặp có hai thực thể VALID có label là đúng quan hệ của cặp hoặc NO_RELATION
  - cặp có thực thể INVALID phải để trống label
  - id câu, id thực thể, id cặp khớp với file khóa (không ai sửa hay xóa dòng)
Có lỗi thì in ra từng lỗi kèm sentence_no và dừng, không ghi file. Dùng --partial để nhập phần đã gán xong.

Định dạng đầu ra, mỗi câu một dòng:
  {id, source_split, source_row_index, text,
   entities: [{id, text, label, start, end, validity}],
   relations: [{head, tail, allowed_relation, label}],   # chỉ cặp có hai thực thể VALID
   annotator, annotation_source, note}

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.import_sheet --split test --annotator human
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import load_workbook

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
NEGATIVE = "NO_RELATION"


def cells(ws):
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    return [dict(zip(head, r)) for r in rows[1:] if any(v is not None for v in r)]


def clean(v):
    return str(v).strip() if v is not None else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="test")
    ap.add_argument("--sheet", type=Path, help="mặc định relation/data/<split>_sheet.xlsx")
    ap.add_argument("--annotator", required=True, help="ví dụ: human, ai")
    ap.add_argument("--out", type=Path, help="mặc định relation/data/<split>.jsonl")
    ap.add_argument("--partial", action="store_true", help="bỏ qua câu chưa gán xong thay vì báo lỗi")
    a = ap.parse_args()
    key = [json.loads(l) for l in (DATA / f"{a.split}_sheet_key.jsonl").read_text(encoding="utf-8").splitlines() if l]
    wb = load_workbook(a.sheet or DATA / f"{a.split}_sheet.xlsx", data_only=True)
    ent_rows, pair_rows = cells(wb["entities"]), cells(wb["pairs"])

    ent_lab, ent_note = {}, defaultdict(list)
    for r in ent_rows:
        k = (clean(r["sentence_id"]), clean(r["entity_id"]))
        ent_lab[k] = clean(r["label"]).upper()
        if clean(r["note"]):
            ent_note[k[0]].append(f'{k[1]}: {clean(r["note"])}')
    pair_lab = {}
    pair_note = defaultdict(list)
    for r in pair_rows:
        k = (clean(r["sentence_id"]), clean(r["pair_id"]))
        pair_lab[k] = clean(r["label"])
        if clean(r["note"]):
            pair_note[k[0]].append(f'{k[1]}: {clean(r["note"])}')

    errors, out, skipped = [], [], 0
    stats = Counter()
    for s in key:
        sid, errs = s["id"], []
        validity = {}
        for e in s["entities"]:
            v = ent_lab.get((sid, e["id"]))
            if v is None:
                errs.append(f"thiếu dòng entity {e['id']}")
            elif v not in ("VALID", "INVALID"):
                errs.append(f"entity {e['id']} ({e['text']}): label '{v}' không hợp lệ")
            validity[e["id"]] = v
        rels = []
        for p in s["pairs"]:
            lab = pair_lab.get((sid, p["pair_id"]))
            ok = validity.get(p["head"]) == "VALID" and validity.get(p["tail"]) == "VALID"
            if lab is None:
                errs.append(f"thiếu dòng cặp {p['pair_id']}")
            elif ok and lab not in (p["allowed_relation"], NEGATIVE):
                errs.append(f"cặp {p['pair_id']}: label '{lab}' phải là {p['allowed_relation']} hoặc {NEGATIVE}")
            elif not ok and lab and all(validity.get(x) in ("VALID", "INVALID") for x in (p["head"], p["tail"])):
                errs.append(f"cặp {p['pair_id']}: có thực thể INVALID nên phải để trống, đang là '{lab}'")
            elif ok:
                rels.append({"head": p["head"], "tail": p["tail"], "allowed_relation": p["allowed_relation"], "label": lab})
        if errs:
            if a.partial:
                skipped += 1
                continue
            errors += [f"câu {s['sentence_no']} ({sid}): {m}" for m in errs]
            continue
        for e in s["entities"]:
            stats[f"entity_{validity[e['id']]}"] += 1
        for r in rels:
            stats[f"{r['allowed_relation']}:{'pos' if r['label'] != NEGATIVE else 'neg'}"] += 1
        out.append({"id": sid, "source_split": s["source_split"], "source_row_index": s["source_row_index"],
                    "text": s["text"],
                    "entities": [{**e, "validity": validity[e["id"]]} for e in s["entities"]],
                    "relations": rels, "annotator": a.annotator, "annotation_source": str(a.sheet or f"{a.split}_sheet.xlsx"),
                    "note": "; ".join(ent_note[sid] + pair_note[sid]) or None})
    if errors:
        print(f"{len(errors)} lỗi, chưa ghi file:")
        print("\n".join(errors[:200]))
        raise SystemExit(1)
    dest = a.out or DATA / f"{a.split}.jsonl"
    with open(dest, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps({"written": str(dest), "sentences": len(out), "skipped_incomplete": skipped,
                      "counts": dict(sorted(stats.items()))}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
