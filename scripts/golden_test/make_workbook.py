"""Tạo phiếu Excel cho người duyệt từ candidates.jsonl.

  python scripts/golden_test/make_workbook.py --annotator A
  python scripts/golden_test/make_workbook.py --annotator B --only-double   # 30 đoạn để tính kappa
"""
import argparse
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from common import ENTITY_TYPES, NEGATIVE, UNKNOWN, ROOT, marked, read_jsonl

ENTITY_VERDICTS = ["DUNG", "SAI_NHAN", "SAI_RANH_GIOI", "XOA"]
HEAD = PatternFill("solid", fgColor="DDE7F3")
EDIT = PatternFill("solid", fgColor="FFF5CC")

GUIDE = [
    "PHIẾU DUYỆT TẬP GOLDEN TEST — NER → RE (VietMed-NER, split test)",
    "",
    "Làm theo thứ tự: (1) sheet THUC_THE, (2) THEM_THUC_THE nếu thiếu, (3) QUAN_HE, (4) đánh dấu xong ở DOAN.",
    "Chỉ điền các cột nền vàng. Không đổi mã đoạn (GT-xxx), mã thực thể (E) hay mã cặp (R).",
    "",
    "THỰC THỂ — 6 loại: CONDITION (bệnh/triệu chứng), DRUG (thuốc), BODY_PART (bộ phận), TEST (xét nghiệm/chẩn đoán), "
    "PROCEDURE (thủ thuật/điều trị không dùng thuốc), DOSAGE (liều thuốc: hàm lượng, lượng dùng, tần suất).",
    "  DUNG = đúng cả cụm từ và nhãn. SAI_NHAN = đúng cụm, sai nhãn → điền NHAN_DUNG. "
    "SAI_RANH_GIOI = cụm bị cắt thừa/thiếu → điền CUM_TU_DUNG (chép đúng chữ trong câu). XOA = không phải thực thể.",
    "  Cụm bệnh chứa bộ phận (vd. 'viêm loét dạ dày') giữ là MỘT CONDITION. Số thứ tự, tỉ lệ, mức độ, lượng thực phẩm không phải DOSAGE.",
    "",
    "QUAN HỆ — chiều cố định head ⟦…⟧ → tail ⟪…⟫:",
    "  located_at: CONDITION → BODY_PART | treated_by: CONDITION → DRUG | treated_by_procedure: CONDITION → PROCEDURE",
    "  diagnosed_by: CONDITION → TEST | has_dosage: DRUG → DOSAGE",
    "  Chọn đúng quan hệ ở cột QUAN_HE_DUOC_PHEP nếu câu nói RÕ quan hệ giữa CHÍNH hai cụm đó; NO_RELATION nếu không; "
    "CHUA_RO nếu câu bị cắt, là câu hỏi/phủ định, hoặc không đủ căn cứ.",
    "  Cùng xuất hiện chưa đủ. Phòng ngừa, nguyên nhân, tác dụng phụ KHÔNG phải điều trị. Không dùng kiến thức ngoài câu.",
    "  Nếu đã XOA/sửa một thực thể, các cặp có thực thể đó vẫn cứ gán theo câu; hệ thống sẽ đưa cặp mới (nếu có) vào lượt 2.",
    "",
    "NẾU CÓ NHÃN AI TIỀN GÁN: cột vàng đã điền sẵn bằng nhãn AI (cột *_AI và LY_DO_AI chỉ để tham khảo, không sửa). "
    "Đọc câu, tự quyết định; đồng ý thì giữ, không đồng ý thì sửa cột vàng. Tỉ lệ sửa sẽ được báo cáo trong khóa luận.",
    "",
    "Câu là bản ghi lời nói, có thể bị cắt ở đầu/cuối và không có dấu câu — đánh giá theo đúng chữ trong câu.",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", default=str(ROOT / "data/golden_test/v1/candidates.jsonl"))
    ap.add_argument("--annotator", required=True)
    ap.add_argument("--only-double", action="store_true")
    ap.add_argument("--ids", help="file JSON danh sách id (vd. lượt 2)")
    ap.add_argument("--out")
    ap.add_argument("--ai-labels", help="ai_labels.jsonl: nhãn AI tiền gán (hiện kèm lý do, điền sẵn vào cột duyệt)")
    a = ap.parse_args()
    ai = {}
    if a.ai_labels:
        ai = {r["id"]: r for r in read_jsonl(a.ai_labels)}
    rows = read_jsonl(a.candidates)
    base = Path(a.candidates).parent
    if a.only_double:
        keep = set(json.loads((base / "manifest.json").read_text(encoding="utf-8"))["double_annotation_ids"])
        rows = [r for r in rows if r["id"] in keep]
    if a.ids:
        keep = set(json.loads(Path(a.ids).read_text(encoding="utf-8")))
        rows = [r for r in rows if r["id"] in keep]
    out = Path(a.out or base / f"phieu_duyet_{a.annotator}{'_double' if a.only_double else ''}.xlsx")

    wb = Workbook()
    ws = wb.active; ws.title = "HUONG_DAN"
    for i, line in enumerate(GUIDE, 1):
        ws.cell(i, 1, line).alignment = Alignment(wrap_text=True)
    ws["A1"].font = Font(bold=True, size=13); ws.column_dimensions["A"].width = 150
    ws.cell(len(GUIDE) + 2, 1, f"Người duyệt: {a.annotator}    Ngày duyệt: ________").font = Font(bold=True)

    def sheet(title, headers, widths):
        s = wb.create_sheet(title)
        s.append(headers)
        for c, w in zip(s[1], widths):
            c.font = Font(bold=True); c.fill = HEAD; s.column_dimensions[c.column_letter].width = w
        s.freeze_panes = "A2"
        return s

    sd = sheet("DOAN", ["ma_doan", "van_ban", "so_thuc_the", "so_cap", "DA_DUYET_XONG", "GHI_CHU"], [9, 110, 10, 8, 15, 30])
    se = sheet("THUC_THE", ["ma_doan", "ma_tt", "cum_tu", "nhan", "start", "end", "ngu_canh",
                            "KET_LUAN", "NHAN_DUNG", "CUM_TU_DUNG", "GHI_CHU", "KET_LUAN_AI", "LY_DO_AI"],
               [9, 7, 24, 12, 7, 7, 80, 16, 14, 24, 25, 14, 50])
    sa = sheet("THEM_THUC_THE", ["ma_doan", "CUM_TU", "LAN_XUAT_HIEN", "NHAN", "GHI_CHU"], [9, 30, 15, 14, 30])
    sr = sheet("QUAN_HE", ["ma_doan", "ma_cap", "head", "head_text", "tail", "tail_text", "QUAN_HE_DUOC_PHEP",
                           "cau_danh_dau", "NHAN", "GHI_CHU", "NHAN_AI", "LY_DO_AI"], [9, 7, 6, 20, 6, 20, 20, 90, 20, 25, 20, 60])

    dv_done = DataValidation(type="list", formula1='"CO,CHUA"', allow_blank=True)
    dv_ent = DataValidation(type="list", formula1='"' + ",".join(ENTITY_VERDICTS) + '"', allow_blank=True)
    dv_type = DataValidation(type="list", formula1='"' + ",".join(ENTITY_TYPES) + '"', allow_blank=True)
    dv_type2 = DataValidation(type="list", formula1='"' + ",".join(ENTITY_TYPES) + '"', allow_blank=True)
    for s, dv in ((sd, dv_done), (se, dv_ent), (se, dv_type), (sa, dv_type2)):
        s.add_data_validation(dv)

    rel_dv = {}
    for r in rows:
        ents = {e["id"]: e for e in r["entities"]}
        note = ai.get(r["id"], {}).get("note")
        sd.append([r["id"], r["text"], len(r["entities"]), len(r["relations"]), None, f"[AI] {note}" if note else None])
        sd.cell(sd.max_row, 2).alignment = Alignment(wrap_text=True)
        dv_done.add(sd.cell(sd.max_row, 5)); sd.cell(sd.max_row, 5).fill = EDIT; sd.cell(sd.max_row, 6).fill = EDIT
        for e in r["entities"]:
            ctx = r["text"][:e["start"]] + "【" + e["text"] + "】" + r["text"][e["end"]:]
            ae = ai.get(r["id"], {}).get("entities", {}).get(e["id"], {})
            se.append([r["id"], e["id"], e["text"], e["label"], e["start"], e["end"], ctx,
                       ae.get("verdict"), ae.get("label"), ae.get("phrase"), None, ae.get("verdict"), ae.get("reason")])
            i = se.max_row
            se.cell(i, 7).alignment = Alignment(wrap_text=True); se.cell(i, 13).alignment = Alignment(wrap_text=True)
            dv_ent.add(se.cell(i, 8)); dv_type.add(se.cell(i, 9))
            for c in range(8, 12): se.cell(i, c).fill = EDIT
        for p in r["relations"]:
            h, t = ents[p["head"]], ents[p["tail"]]
            ar = ai.get(r["id"], {}).get("relations", {}).get(p["id"], {})
            sr.append([r["id"], p["id"], h["id"], h["text"], t["id"], t["text"], p["allowed_relation"],
                       marked(r["text"], h, t), ar.get("label"), None, ar.get("label"), ar.get("reason")])
            i = sr.max_row
            sr.cell(i, 8).alignment = Alignment(wrap_text=True); sr.cell(i, 12).alignment = Alignment(wrap_text=True)
            rel = p["allowed_relation"]
            if rel not in rel_dv:
                rel_dv[rel] = DataValidation(type="list", formula1=f'"{rel},{NEGATIVE},{UNKNOWN}"', allow_blank=True)
                sr.add_data_validation(rel_dv[rel])
            rel_dv[rel].add(sr.cell(i, 9))
            sr.cell(i, 9).fill = EDIT; sr.cell(i, 10).fill = EDIT
    for r in rows:
        for add in ai.get(r["id"], {}).get("additions", []):
            sa.append([r["id"], add["phrase"], add.get("nth"), add["label"], f"[AI đề xuất] {add.get('reason') or ''}".strip()])
            dv_type2.add(sa.cell(sa.max_row, 4))
            for c in range(1, 6): sa.cell(sa.max_row, c).fill = EDIT
    for _ in range(60):
        sa.append([None] * 5)
        dv_type2.add(sa.cell(sa.max_row, 4))
        for c in range(1, 6): sa.cell(sa.max_row, c).fill = EDIT
    flags = [f for r in rows for f in ai.get(r["id"], {}).get("flags", [])]
    if flags:
        sf = wb.create_sheet("CAN_XEM_LAI", 1)
        sf.append(["Các điểm soát lại phát hiện trong nhãn AI tiền gán — người duyệt quyết định, không tự áp dụng."])
        sf["A1"].font = Font(bold=True)
        sf.append(["ma_doan", "ma", "loai", "van_de", "goi_y", "NGUOI_DUYET_QUYET_DINH"])
        for c in sf[2]: c.font = Font(bold=True); c.fill = HEAD
        for f in flags:
            sf.append([f["id"], f.get("ref"), f["kind"], f["issue"], f.get("suggest"), None])
            sf.cell(sf.max_row, 6).fill = EDIT
            for c in (4, 5): sf.cell(sf.max_row, c).alignment = Alignment(wrap_text=True)
        for col, w in zip("ABCDEF", (9, 8, 18, 70, 45, 22)): sf.column_dimensions[col].width = w
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"{out}  ({len(rows)} đoạn, {sum(len(r['entities']) for r in rows)} thực thể, "
          f"{sum(len(r['relations']) for r in rows)} cặp)")


if __name__ == "__main__":
    main()
