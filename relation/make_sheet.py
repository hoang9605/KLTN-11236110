"""Lập phiếu Excel gán nhãn mù cho một tập (mặc định: test).

Phiếu gán mù: không có nhãn AI, không có nhãn luật, không có điểm hay lý do chọn câu, không gợi ý
từ danh sách mention nhiễu. Mọi thực thể trong câu đều được đưa ra cho bước A, kể cả thực thể chung
chung hay thực thể nằm trong entity_blocklist.json. Các danh sách đó chỉ dùng để chọn câu.
Cặp ứng viên được tính lại trên toàn bộ thực thể của câu. Thứ tự câu được xáo trộn.

Phiếu gồm 3 sheet:
  README    - cách gán
  entities  - bước A: mỗi mention một dòng, cột label chọn VALID / INVALID
  pairs     - bước B: mỗi cặp một dòng, cột label chọn tên quan hệ hoặc NO_RELATION.
              Cột skip tự hiện SKIP khi một trong hai thực thể bị INVALID (khi đó để trống label).

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.make_sheet --split test
Đầu ra: relation/data/<split>_sheet.xlsx và relation/data/<split>_sheet_key.jsonl (khóa để nhập lại)
"""
import argparse
import json
import random
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from relation_extraction.data import candidates

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
NEGATIVE = "NO_RELATION"


def mark_entity(text, e):
    return text[:e["start"]] + "【" + text[e["start"]:e["end"]] + "】" + text[e["end"]:]


def mark_pair(text, h, t):
    spans = sorted([(h, "H"), (t, "T")], key=lambda x: -x[0]["start"])
    for e, tag in spans:
        text = text[:e["start"]] + f"[{tag}: " + text[e["start"]:e["end"]] + f" /{tag}]" + text[e["end"]:]
    return text


def all_pairs(row):
    ents = [{k: e[k] for k in ("id", "text", "label", "start", "end")} for e in row["entities"]]
    return [{"head": c["head"]["id"], "tail": c["tail"]["id"], "allowed_relation": c["allowed_relation"]}
            for c in candidates(row["text"], ents)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="test")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    rows = [json.loads(l) for l in (DATA / f"{a.split}_unlabeled.jsonl").read_text(encoding="utf-8").splitlines() if l]
    random.Random(a.seed).shuffle(rows)

    wb = Workbook()
    readme = wb.active
    readme.title = "README"
    for line in [
        "Phiếu gán nhãn RE, gán mù. Hướng dẫn: relation/guideline.md (đã khóa).",
        "",
        "Bước A, sheet entities: cột label chọn VALID hoặc INVALID cho từng mention 【...】.",
        "Bước B, sheet pairs: cột label chọn tên quan hệ (đúng bằng cột relation) hoặc NO_RELATION.",
        "  - Nếu cột skip hiện SKIP (một thực thể bị INVALID) thì để trống label.",
        "  - Mọi dòng không SKIP phải có label. Không có nhãn 'chưa rõ'.",
        "Cột note chỉ để ghi chú, không phải nhãn.",
        "Không sửa các cột khác, không xóa hay sắp xếp lại dòng.",
        "Làm theo từng câu: gán entities của câu đó trước, rồi đến pairs (cùng sentence_no).",
    ]:
        readme.append([line])
    readme.column_dimensions["A"].width = 110

    head_font = Font(bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", fgColor="305496")
    wrap = Alignment(wrap_text=True, vertical="top")

    ws_e = wb.create_sheet("entities")
    ws_e.append(["sentence_no", "sentence_id", "entity_id", "type", "mention", "sentence", "label", "note"])
    ws_p = wb.create_sheet("pairs")
    ws_p.append(["sentence_no", "sentence_id", "pair_id", "relation", "head", "tail", "sentence", "skip", "label", "note"])

    key = []
    n_ent = n_pair = 0
    for no, row in enumerate(rows, 1):
        for e in sorted(row["entities"], key=lambda e: e["start"]):
            ws_e.append([no, row["id"], e["id"], e["label"], e["text"], mark_entity(row["text"], e), "", ""])
            n_ent += 1
        ents = {e["id"]: e for e in row["entities"]}
        pairs = all_pairs(row)
        for k, p in enumerate(pairs, 1):
            pid = f"P{k}"
            r = ws_p.max_row + 1
            h, t = ents[p["head"]], ents[p["tail"]]
            skip = (f'=IF(OR(COUNTIFS(entities!$B:$B,$B{r},entities!$C:$C,"{h["id"]}",entities!$G:$G,"INVALID")>0,'
                    f'COUNTIFS(entities!$B:$B,$B{r},entities!$C:$C,"{t["id"]}",entities!$G:$G,"INVALID")>0),"SKIP","")')
            ws_p.append([no, row["id"], pid, p["allowed_relation"], f'{h["text"]} ({h["label"]})',
                         f'{t["text"]} ({t["label"]})', mark_pair(row["text"], h, t), skip, "", ""])
            n_pair += 1
        key.append({"sentence_no": no, "id": row["id"], "source_split": row["source_split"],
                    "source_row_index": row["source_row_index"], "text": row["text"],
                    "entities": [{k2: e[k2] for k2 in ("id", "text", "label", "start", "end")} for e in row["entities"]],
                    "pairs": [{"pair_id": f"P{k}", **p} for k, p in enumerate(pairs, 1)]})

    dv_e = DataValidation(type="list", formula1='"VALID,INVALID"', allow_blank=True)
    ws_e.add_data_validation(dv_e)
    dv_e.add(f"G2:G{ws_e.max_row}")
    rels = sorted({p["allowed_relation"] for k in key for p in k["pairs"]})
    dv_p = DataValidation(type="list", formula1='"' + ",".join(rels + [NEGATIVE]) + '"', allow_blank=True)
    ws_p.add_data_validation(dv_p)
    dv_p.add(f"I2:I{ws_p.max_row}")

    for ws, widths in ((ws_e, [6, 14, 8, 11, 22, 80, 10, 25]), (ws_p, [6, 14, 6, 20, 24, 24, 80, 7, 20, 25])):
        for c in ws[1]:
            c.font, c.fill = head_font, head_fill
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
        for r in ws.iter_rows(min_row=2):
            for c in r:
                c.alignment = wrap
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

    out = DATA / f"{a.split}_sheet.xlsx"
    wb.save(out)
    with open(DATA / f"{a.split}_sheet_key.jsonl", "w", encoding="utf-8") as f:
        for k in key:
            f.write(json.dumps(k, ensure_ascii=False) + "\n")
    print(f"{out}: {len(rows)} câu, {n_ent} mention, {n_pair} cặp")


if __name__ == "__main__":
    main()
