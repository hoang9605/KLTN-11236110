"""Gán lại toàn bộ cặp của tập test theo tiêu chí chặt (sau phiếu soát 50 cặp ngày 2026-11-21).

Phiếu xếp theo câu để mỗi câu chỉ đọc một lần, không hiện nhãn cũ hay dự đoán của mô hình.
Mọi dòng phải được chọn rõ (tên quan hệ hoặc NO_RELATION): ở phiếu 50 cặp, ô trống có lúc rơi vào cặp
hiển nhiên sai (estrogen – "những bệnh nhân" là has_dosage), nên ô trống không được hiểu là có quan hệ.
Chỉ các kết luận NO_RELATION đã chọn rõ ở relation/data/review_fn.xlsx được điền sẵn.
Thực thể giữ nguyên như test.jsonl (chỉ các cặp có hai thực thể VALID).
Tập test cũ (relation/data/test.jsonl) được giữ nguyên; nhãn mới ghi vào test_v2.jsonl.

    .venv\\Scripts\\python.exe -X utf8 -m relation.relabel_test make
    .venv\\Scripts\\python.exe -X utf8 -m relation.relabel_test import
    .venv\\Scripts\\python.exe -X utf8 -m relation.relabel_test score
Đầu ra: relation/data/test_relabel.xlsx, relation/data/test_v2.jsonl, relation/outputs/evaluation_test_v2.json
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill, Protection
from openpyxl.worksheet.datavalidation import DataValidation

from .ai_batches import load
from .evaluate import NEGATIVE, bootstrap, gold, predict, scores
from .review_fn import KEY as FN_KEY, SHEET as FN_SHEET, marked

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
SHEET = DATA / "test_relabel.xlsx"
OUT_DATA = DATA / "test_v2.jsonl"
OUT_EVAL = HERE / "outputs" / "evaluation_test_v2.json"
COLS = ["Mã cặp", "STT câu", "Câu (⟦đầu⟧ … ⟪đuôi⟫)", "Quan hệ cần xét", "Thực thể đầu", "Thực thể đuôi",
        "Kết luận", "Ghi chú", "Đã soát ở phiếu 50 cặp"]
C_UID, C_VERDICT, C_NOTE = 1, 7, 8


def uid(r, x):
    return f"{r['id']}:{x['head']}:{x['tail']}:{x['allowed_relation']}"


def prior_review():
    key = json.loads(FN_KEY.read_text(encoding="utf-8"))
    ws = load_workbook(FN_SHEET)["Phiếu"]
    v = {r[0].value: (r[5].value, r[6].value) for r in ws.iter_rows(min_row=2)}
    return {it["uid"]: v[it["stt"]] for it in key["items"]}


def make(force=False):
    if SHEET.exists() and not force:
        raise SystemExit(f"{SHEET} đã có, không ghi đè (thêm --force nếu chắc chắn phiếu chưa được điền)")
    rows = sorted(load(DATA / "test.jsonl"), key=lambda r: r["id"])
    prior = prior_review()
    wb = Workbook()
    ws = wb.active
    ws.title = "Phiếu"
    ws.append(COLS)
    for c in ws[1]:
        c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="DDDDDD")
    dvs, n = {}, 0
    band = [PatternFill("solid", fgColor="FFFFFF"), PatternFill("solid", fgColor="F2F2F2")]
    for si, r in enumerate(rows, 1):
        E = {e["id"]: e for e in r["entities"]}
        for x in r["relations"]:
            n += 1
            u = uid(r, x); rel = x["allowed_relation"]
            v, note = prior.get(u, (None, None))
            done = v is not None
            ws.append([u, si, marked(r["text"], E[x["head"]], E[x["tail"]]), rel, E[x["head"]]["text"],
                       E[x["tail"]]["text"], v, note, "có" if done else None])
            row = n + 1
            if rel not in dvs:
                dvs[rel] = DataValidation(type="list", formula1=f'"{rel},{NEGATIVE}"', allow_blank=True, showErrorMessage=True)
                ws.add_data_validation(dvs[rel])
            dvs[rel].add(ws.cell(row, C_VERDICT))
            for col in range(1, len(COLS) + 1):
                ws.cell(row, col).fill = band[si % 2]
            for col in (C_VERDICT, C_NOTE):
                ws.cell(row, col).protection = Protection(locked=False)
                ws.cell(row, col).fill = PatternFill("solid", fgColor="FFF7D6")
            ws.cell(row, 3).alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABCDEFGHI", (4, 7, 80, 20, 20, 20, 20, 26, 12)):
        ws.column_dimensions[col].width = w
    ws.column_dimensions["A"].hidden = True
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:I{n + 1}"
    ws.protection.sheet = True
    ws.protection.autoFilter = False
    ws.protection.formatRows = ws.protection.formatColumns = False

    rd = wb.create_sheet("Hướng dẫn", 0)
    for line in [
        f"Gán lại toàn bộ {n} cặp quan hệ của tập kiểm tra ({len(rows)} câu), xếp theo câu.",
        "Mỗi dòng là một cặp: ⟦thực thể đầu⟧ và ⟪thực thể đuôi⟫. Dòng cùng màu nền là cùng một câu.",
        "Chọn cho MỌI dòng: tên quan hệ nếu câu có nói quan hệ đó giữa hai thực thể, NO_RELATION nếu không.",
        "Không để trống: dòng trống sẽ không được nhập. Lọc cột Kết luận theo (Blanks) để tìm dòng còn sót.",
        "Chọn NO_RELATION khi hai thực thể chỉ cùng xuất hiện mà câu không nói quan hệ đó: liệt kê nhiều bệnh,",
        "phòng bệnh/dự phòng, giảm nguy cơ, tác dụng phụ, phủ định, nói về hai đối tượng khác nhau, câu bị cắt dở.",
        "Cũng chọn NO_RELATION khi một thực thể không đúng loại (ví dụ 'những bệnh nhân' không phải liều dùng).",
        "Tiêu chí giống phiếu 50 cặp vừa soát. Các cặp đã chọn NO_RELATION ở phiếu đó được điền sẵn (cột 'Đã soát' = có).",
        "located_at: bệnh/triệu chứng ở bộ phận cơ thể. treated_by: bệnh được điều trị bằng thuốc.",
        "treated_by_procedure: bệnh được điều trị bằng thủ thuật (không gồm tầm soát/chẩn đoán).",
        "diagnosed_by: bệnh được chẩn đoán/phát hiện bằng xét nghiệm, khám, chẩn đoán hình ảnh. has_dosage: thuốc có liều dùng.",
        "Nếu quan hệ đúng là một quan hệ khác với cột 'Quan hệ cần xét', chọn NO_RELATION và ghi quan hệ đúng vào Ghi chú.",
    ]:
        rd.append([line])
    rd.column_dimensions["A"].width = 120
    wb.active = 1
    wb.save(SHEET)
    print(f"{SHEET} | {len(rows)} câu | {n} cặp | điền sẵn {sum(1 for v, _ in prior.values() if v)} cặp từ phiếu 50 cặp")


def do_import(sheet=None, annotator="expert"):
    sheet = Path(sheet) if sheet else SHEET
    ws = load_workbook(sheet)["Phiếu"]
    v = {r[C_UID - 1].value: (r[C_VERDICT - 1].value, r[C_NOTE - 1].value) for r in ws.iter_rows(min_row=2)}
    blank = [u for u, (verdict, _) in v.items() if not verdict]
    if blank:
        raise SystemExit(f"còn {len(blank)} dòng chưa chọn Kết luận, ví dụ: {blank[:5]}")
    rows = load(DATA / "test.jsonl")
    changed = Counter()
    with open(OUT_DATA, "w", encoding="utf-8") as f:
        for r in rows:
            rr = json.loads(json.dumps(r))
            for x in rr["relations"]:
                verdict, note = v[uid(r, x)]
                if verdict not in (NEGATIVE, x["allowed_relation"]):
                    raise SystemExit(f"nhãn lạ {verdict!r} ở {uid(r, x)}")
                new = NEGATIVE if verdict == NEGATIVE else x["allowed_relation"]
                changed[f"{x['label'] != NEGATIVE}->{new != NEGATIVE}"] += 1
                x["label_v1"] = x["label"]; x["label"] = new
                if note:
                    x["note"] = note
            rr["annotator"] = annotator
            rr["annotation_source"] = str(sheet) if sheet != SHEET else "relation/data/" + SHEET.name
            rr["note"] = "nhãn quan hệ gán lại theo tiêu chí chặt 2026-11-21"
            f.write(json.dumps(rr, ensure_ascii=False) + "\n")
    print(f"{OUT_DATA} | thay đổi (dương cũ -> dương mới): {dict(changed)}")


def score(config="x1"):
    rows = load(OUT_DATA)
    g = gold(rows)
    p, _ = predict(json.loads((HERE / "outputs" / "train" / f"{config}.json").read_text(encoding="utf-8")), "test")
    allpos = {k: k.rsplit(":", 1)[1] for k in g}
    sent_of = {k: k.split(":")[0] for k in g}
    rep = {"config": config, "test_set": "test_v2", "annotator": sorted({r["annotator"] for r in rows}), "pairs": len(g), "positives": sum(v != NEGATIVE for v in g.values()),
           "model": scores(g, p), "always_positive": scores(g, allpos),
           "ci95_micro_f1": bootstrap(g, {"model": p, "always_positive": allpos}, sent_of)}
    OUT_EVAL.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: rep[k] for k in ("pairs", "positives", "ci95_micro_f1")} |
                     {"model_micro": rep["model"]["micro"], "model_macro": rep["model"]["macro_f1"],
                      "always_positive_micro": rep["always_positive"]["micro"],
                      "per_relation_f1": {r: v["f1"] for r, v in rep["model"]["per_relation"].items()}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "import", "score"])
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--sheet")
    ap.add_argument("--annotator", default="expert")
    a = ap.parse_args()
    make(a.force) if a.cmd == "make" else do_import(a.sheet, a.annotator) if a.cmd == "import" else score()
