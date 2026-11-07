r"""Reviewer workbook for the normalization gold set, and import back to TSV.

make:   AI-prefilled codes with their official names and a context snippet; the
        reviewer fills the yellow columns (Đồng ý? = C/K, Mã sửa, Ghi chú).
import: writes a reviewed label TSV; rows with Đồng ý? = K take "Mã sửa"
        (codes separated by commas, or NIL). Every row must be answered.

    .venv\Scripts\python.exe -X utf8 scripts/normalization_eval/review_sheet.py make ^
        --gold data/norm_gold_v1/gold_test.jsonl --out data/norm_gold_v1/phieu_duyet_chuan_hoa_test.xlsx
    .venv\Scripts\python.exe -X utf8 scripts/normalization_eval/review_sheet.py import ^
        --workbook data/norm_gold_v1/phieu_duyet_chuan_hoa_test_da_duyet.xlsx ^
        --out data/norm_gold_v1/reviewed_labels_test.tsv
    # rồi: merge_labels.py --labels reviewed_labels_test.tsv --annotator "<tên>" --human-verified
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

HEADERS = ["ID", "Loại", "Dạng thực thể", "Tần suất", "Ngữ cảnh", "Mã AI đề xuất",
           "Tên chuẩn của mã", "Ghi chú AI", "Đồng ý? (C/K)", "Mã sửa", "Ghi chú người duyệt"]


def make(a):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from normalization.icd10 import ICD10Normalizer
    from normalization.rxnorm import RxNormNormalizer

    icd = ICD10Normalizer().code_map
    rx = RxNormNormalizer()
    wb = Workbook()
    ws = wb.active
    ws.title = "Duyet"
    ws.append(HEADERS)
    for c in ws[1]:
        c.font = Font(bold=True)
    yellow = PatternFill("solid", fgColor="FFF2CC")
    for line in Path(a.gold).read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        ctx = r["contexts"][0]
        snip = ctx["text"][max(0, ctx["start"] - 60):ctx["end"] + 60]
        if r["ontology"] == "ICD-10":
            names = [icd.get(c, {}).get("name", "?") for c in r["gold_codes"]]
        else:
            names = [rx._fetch_standard_name(c, fallback_name="?") for c in r["gold_codes"]]
        ws.append([r["id"], r["ontology"], r["form"], r["freq"], snip,
                   ", ".join(r["gold_codes"]) or "NIL",
                   " | ".join(f"{c}: {n}" for c, n in zip(r["gold_codes"], names)),
                   r.get("note", ""), "", "", ""])
        for col in (9, 10, 11):
            ws.cell(row=ws.max_row, column=col).fill = yellow
    for col, width in zip("ABCDEFGHIJK", (9, 8, 24, 8, 60, 18, 60, 30, 10, 16, 30)):
        ws.column_dimensions[col].width = width
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "D2"
    g = wb.create_sheet("Huong_dan")
    for line in (
        "Mỗi dòng là một dạng thực thể duy nhất (gom theo chữ thường, bỏ dấu câu) trong split test VietMed-NER.",
        "Mã đầu tiên là mã chính (cụ thể nhất mà ngữ cảnh cho phép); các mã sau cũng được chấp nhận là đúng.",
        "NIL = không có khái niệm phù hợp: từ chung chung (triệu chứng, biến chứng, thuốc), nhóm thuốc, không phải bệnh/thuốc, mảnh lỗi NER.",
        "ICD-10 theo danh mục Bộ Y tế (QĐ 06/BYT phụ lục 1). RxNorm ở mức hoạt chất (TTY=IN) khi có.",
        "Đồng ý? = C nếu giữ nguyên; = K và điền 'Mã sửa' (nhiều mã cách nhau dấu phẩy, hoặc NIL) nếu sửa.",
    ):
        g.append([line])
    g.column_dimensions["A"].width = 120
    wb.save(a.out)
    print(f"wrote {a.out}")


def do_import(a):
    from openpyxl import load_workbook
    ws = load_workbook(a.workbook, read_only=True)["Duyet"]
    out, missing, changed = [], [], 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[0]:
            continue
        rid, ai_codes, ai_note = row[0], str(row[5] or "").strip(), row[7] or ""
        agree = str(row[8] or "").strip().upper()
        fix, note = str(row[9] or "").strip(), str(row[10] or "").strip()
        if agree == "C":
            codes = ai_codes
        elif agree == "K" and fix:
            codes, changed = fix, changed + 1
        else:
            missing.append(rid)
            continue
        codes = "NIL" if codes.upper() == "NIL" else ",".join(c.strip() for c in codes.split(","))
        out.append(f"{rid}\t{codes}\t{note or ai_note}")
    if missing:
        sys.exit(f"{len(missing)} dòng chưa duyệt / thiếu mã sửa: {missing[:20]}")
    Path(a.out).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {len(out)} rows -> {a.out}; reviewer changed {changed} "
          f"({changed / max(len(out), 1):.1%}) AI labels")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make"); m.add_argument("--gold", required=True); m.add_argument("--out", required=True)
    i = sub.add_parser("import"); i.add_argument("--workbook", required=True); i.add_argument("--out", required=True)
    a = ap.parse_args()
    make(a) if a.cmd == "make" else do_import(a)


if __name__ == "__main__":
    main()
