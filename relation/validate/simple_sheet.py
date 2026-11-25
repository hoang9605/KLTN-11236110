"""A simple, blind review sheet for the medical expert (same rows as expert_review.xlsx).

One row per sentence, five visible columns:
  STT | Câu (entities in bold) | Quan hệ trong câu | Câu hợp lý? | Quan hệ đúng? | Ghi chú
The expert answers two questions with Valid / Invalid from a drop-down. The system's own verdict, evidence and
translation are NOT shown, so the expert is not influenced by them (needed to measure the system's precision).
A row is kept for training only if both answers are Valid.

Run: .venv\\Scripts\\python.exe -X utf8 -m relation.validate.simple_sheet
Output: relation/data/synth/validate/phieu_duyet_chuyen_gia.xlsx
"""
import json

from openpyxl import Workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

from .units import OUT, SYNTH, load

SHEET = OUT / "phieu_duyet_chuyen_gia.xlsx"
TAB = "duyet"
ANSWERS = ("1", "2")  # 1 = Valid, 2 = Invalid
REL_VI = {"located_at": "ở vị trí", "treated_by": "điều trị bằng thuốc",
          "treated_by_procedure": "điều trị bằng thủ thuật / phương pháp", "diagnosed_by": "chẩn đoán bằng",
          "has_dosage": "liều dùng"}


def sentence_rich(text, ents):
    parts, pos = [], 0
    bold = InlineFont(b=True, color="1F4E79")
    for e in sorted(ents, key=lambda e: e["start"]):
        if e["start"] > pos:
            parts.append(text[pos:e["start"]])
        parts.append(TextBlock(bold, text[e["start"]:e["end"]]))
        pos = e["end"]
    if pos < len(text):
        parts.append(text[pos:])
    return CellRichText(parts)


def relations_text(row):
    ents = {e["id"]: e["text"] for e in row["entities"]}
    return "\n".join(f'"{ents[x["head"]]}" {x["label"]} "{ents[x["tail"]]}"' for x in row["relations"])


def main():
    pool = {r["id"]: r for r in load(SYNTH / "pool.jsonl")}
    key = json.loads((OUT / "expert_review_key.json").read_text())
    write_sheet(SHEET, [pool[k["sentence_id"]] for k in key])


def write_sheet(path, records):
    """Write the blind sheet for these pool records (also used by round2_sheet.py)."""
    key = records
    wb = Workbook()
    ws = wb.active
    ws.title = TAB
    head = ["id", "STT", "Câu", "Quan hệ trong câu", "Câu hợp lý?\n1 = Valid\n2 = Invalid",
            "Quan hệ đúng?\n1 = Valid\n2 = Invalid", "Ghi chú"]
    ws.append(head)
    thin = Side(style="thin", color="BFBFBF")
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF", size=12)
        c.fill = PatternFill("solid", fgColor="305496")
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    for i, r in enumerate(key, 1):
        ws.append([r["id"], i, sentence_rich(r["text"], r["entities"]), relations_text(r), None, None, None])
    n = len(key) + 1
    dv = DataValidation(type="list", formula1=f'"{",".join(ANSWERS)}"', allow_blank=True,
                        showErrorMessage=True, errorTitle="Nhập 1 hoặc 2",
                        error="Chỉ nhập 1 (Valid) hoặc 2 (Invalid)")
    ws.add_data_validation(dv)
    dv.add(f"E2:F{n}")
    for col, w in zip("ABCDEFG", (10, 6, 70, 48, 14, 14, 30)):
        ws.column_dimensions[col].width = w
    ws.column_dimensions["A"].hidden = True
    answer_fill = PatternFill("solid", fgColor="FFF2CC")
    for row in ws.iter_rows(min_row=2, max_row=n):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
            c.font = Font(size=12)
        for c in row[4:6]:
            c.fill = answer_fill
            c.alignment = Alignment(horizontal="center", vertical="top")
    ws.freeze_panes = "C2"
    ws.protection.sheet = False

    g = wb.create_sheet("huong_dan", 0)
    guide = [
        "HƯỚNG DẪN",
        "",
        "Gõ 1 hoặc 2 vào hai cột vàng:   1 = Valid   2 = Invalid",
        "",
        "Câu hợp lý?    1 = câu nói được và đúng y khoa.   2 = vô lý hoặc sai y khoa.",
        "Quan hệ đúng?  1 = mọi dòng quan hệ đều đúng.     2 = có dòng sai.",
        "",
        "located_at = ở vị trí · treated_by = điều trị bằng thuốc · treated_by_procedure = điều trị bằng thủ thuật",
        "diagnosed_by = chẩn đoán bằng · has_dosage = liều dùng · NO_RELATION = không có quan hệ",
        "",
        "Câu bị cắt đầu/cuối là bình thường (văn nói).",
    ]
    for line in guide:
        g.append([line])
    g["A1"].font = Font(bold=True, size=14)
    for row in g.iter_rows(min_row=2):
        row[0].font = Font(size=12)
    g.column_dimensions["A"].width = 110
    wb.active = 1
    wb.save(path)
    print(f"{path} ({len(key)} rows)")


if __name__ == "__main__":
    main()
