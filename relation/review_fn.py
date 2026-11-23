"""Phiếu soát lại các cặp test mà mô hình đã chọn (x1) bỏ sót, để biết tiêu chí nào đúng.

Lấy mẫu phân tầng theo quan hệ 40 cặp mô hình đoán âm nhưng nhãn test là dương (bỏ sót),
trộn thêm 10 cặp mô hình đoán dương đúng (đối chứng) để người duyệt không biết cặp nào thuộc nhóm nào.
Phiếu không hiện nhãn cũ hay dự đoán của mô hình. Khoá theo từng ô, chỉ mở cột kết luận và ghi chú.
Phiếu này chỉ để phân tích, không sửa relation/data/test.jsonl.

    .venv\\Scripts\\python.exe -X utf8 -m relation.review_fn make
    .venv\\Scripts\\python.exe -X utf8 -m relation.review_fn summarize
Đầu ra: relation/data/review_fn.xlsx, relation/data/review_fn_key.json, relation/outputs/review_fn_summary.json
"""
import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill, Protection
from openpyxl.worksheet.datavalidation import DataValidation

from .ai_batches import load
from .evaluate import NEGATIVE, REL, gold, predict

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
SHEET = DATA / "review_fn.xlsx"
KEY = DATA / "review_fn_key.json"
OUT = HERE / "outputs" / "review_fn_summary.json"
SEED = 20261121
N_FN, N_CTRL, MIN_PER_REL = 40, 10, 5
CONCLUSION_COL = 6


def allocate(counts, total, floor):
    """Chia total theo tỉ lệ counts, mỗi nhóm ít nhất min(floor, count)."""
    alloc = {r: min(floor, c) for r, c in counts.items()}
    rest = total - sum(alloc.values())
    pool = {r: c - alloc[r] for r, c in counts.items()}
    tot = sum(pool.values())
    for r in sorted(pool, key=lambda r: -pool[r]):
        add = min(pool[r], round(rest * pool[r] / tot)) if tot else 0
        alloc[r] += add
    while sum(alloc.values()) > total:
        r = max(alloc, key=lambda r: alloc[r]); alloc[r] -= 1
    while sum(alloc.values()) < total:
        r = max((r for r in counts if alloc[r] < counts[r]), key=lambda r: counts[r] - alloc[r]); alloc[r] += 1
    return alloc


def marked(text, h, t):
    spans = sorted([(h["start"], h["end"], "⟦", "⟧"), (t["start"], t["end"], "⟪", "⟫")], reverse=True)
    for s, e, a, b in spans:
        text = text[:s] + a + text[s:e] + b + text[e:]
    return text


def make():
    if SHEET.exists():
        wb = load_workbook(SHEET)
        if any(r[CONCLUSION_COL - 1].value for r in wb["Phiếu"].iter_rows(min_row=2)):
            raise SystemExit(f"{SHEET} đã có kết luận, không ghi đè")
    rows = {r["id"]: r for r in load(DATA / "test.jsonl")}
    g = gold(rows.values())
    p, _ = predict(json.loads((HERE / "outputs" / "train" / "x1.json").read_text(encoding="utf-8")), "test")
    fn = [k for k in g if g[k] != NEGATIVE and p[k] == NEGATIVE]
    tp = [k for k in g if g[k] != NEGATIVE and p[k] == g[k]]
    rng = random.Random(SEED)
    by = defaultdict(list)
    for k in fn:
        by[k.rsplit(":", 1)[1]].append(k)
    alloc = allocate({r: len(by[r]) for r in REL if by[r]}, N_FN, MIN_PER_REL)
    pick = [(k, "fn") for r in alloc for k in rng.sample(sorted(by[r]), alloc[r])]
    pick += [(k, "control_tp") for k in rng.sample(sorted(tp), N_CTRL)]
    rng.shuffle(pick)

    wb = Workbook()
    ws = wb.active
    ws.title = "Phiếu"
    head = ["STT", "Câu (⟦đầu⟧ … ⟪đuôi⟫)", "Quan hệ cần xét", "Thực thể đầu", "Thực thể đuôi", "Kết luận", "Ghi chú"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="DDDDDD")
    key = []
    for i, (k, group) in enumerate(pick, 1):
        sid, h, t, rel = k.split(":")
        r = rows[sid]; E = {e["id"]: e for e in r["entities"]}
        ws.append([i, marked(r["text"], E[h], E[t]), rel, E[h]["text"], E[t]["text"], None, None])
        dv = DataValidation(type="list", formula1=f'"{rel},{NEGATIVE}"', allow_blank=True, showErrorMessage=True)
        ws.add_data_validation(dv); dv.add(ws.cell(i + 1, CONCLUSION_COL))
        for col in (CONCLUSION_COL, CONCLUSION_COL + 1):
            ws.cell(i + 1, col).protection = Protection(locked=False)
            ws.cell(i + 1, col).fill = PatternFill("solid", fgColor="FFF7D6")
        key.append({"stt": i, "uid": k, "relation": rel, "group": group})
    for col, w in zip("ABCDEFG", (6, 90, 22, 22, 22, 22, 30)):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "B2"
    ws.protection.sheet = True
    ws.protection.formatRows = ws.protection.formatColumns = False

    rd = wb.create_sheet("Hướng dẫn")
    for line in [
        "Phiếu soát lại cặp quan hệ trên tập kiểm tra (50 cặp).",
        "Mỗi dòng là một cặp thực thể trong một câu: ⟦thực thể đầu⟧ và ⟪thực thể đuôi⟫.",
        "Ở cột Kết luận, chọn tên quan hệ nếu câu nói rõ quan hệ đó giữa hai thực thể; chọn NO_RELATION nếu",
        "hai thực thể chỉ cùng xuất hiện trong câu mà câu không nói quan hệ đó (ví dụ: liệt kê, phòng bệnh,",
        "tác dụng phụ, phủ định, nói về hai bệnh nhân khác nhau).",
        "located_at: bệnh/triệu chứng ở bộ phận cơ thể. treated_by: bệnh được điều trị bằng thuốc.",
        "treated_by_procedure: bệnh được điều trị bằng thủ thuật. diagnosed_by: bệnh được chẩn đoán/phát hiện bằng xét nghiệm.",
        "has_dosage: thuốc có liều dùng.",
        "Xét từng cặp độc lập, theo đúng câu chữ; không cần xem lại nhãn cũ. Chưa chắc thì ghi vào Ghi chú.",
    ]:
        rd.append([line])
    rd.column_dimensions["A"].width = 120
    wb.move_sheet("Hướng dẫn", -1)
    wb.active = 1
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    wb.save(SHEET)
    KEY.write_text(json.dumps({"seed": SEED, "model": "x1", "fn_total": len(fn), "fn_by_relation": {r: len(v) for r, v in by.items()},
                               "allocation": alloc, "items": key}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{SHEET} | {len(pick)} dòng | bỏ sót {len(fn)} cặp, lấy {N_FN}: {alloc} | đối chứng {N_CTRL}")


def wilson(k, n, z=1.96):
    if not n:
        return None
    ph = k / n; d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d; h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def summarize(blank="skip"):
    """blank='positive': ô trống được hiểu là giữ nhãn dương (người duyệt chỉ đánh dấu NO_RELATION)."""
    key = json.loads(KEY.read_text(encoding="utf-8"))
    ws = load_workbook(SHEET)["Phiếu"]
    verdict = {r[0].value: r[CONCLUSION_COL - 1].value for r in ws.iter_rows(min_row=2)}
    res = defaultdict(Counter)
    for it in key["items"]:
        v = verdict.get(it["stt"])
        tag = ("positive" if blank == "positive" else "blank") if not v else ("negative" if v == NEGATIVE else "positive")
        res[it["group"]][tag] += 1
        if it["group"] == "fn":
            res["fn:" + it["relation"]][tag] += 1
    out = {"blank_as": blank}
    for grp, c in sorted(res.items()):
        c = Counter({"positive": 0, "negative": 0, "blank": 0}) + c
        c = {k: c.get(k, 0) for k in ("positive", "negative", "blank")}
        n = c["positive"] + c["negative"]
        out[grp] = {**c, "judged": n, "positive_rate": round(c["positive"] / n, 3) if n else None,
                    "positive_rate_ci95": wilson(c["positive"], n)}
    fn = out.get("fn", {})
    if fn.get("judged"):
        est = round(fn["positive_rate"] * key["fn_total"])
        out["reading"] = (f"Trong {fn['judged']} cặp bỏ sót đã soát, {fn['positive']} vẫn là dương "
                          f"(ước tính khoảng {est}/{key['fn_total']} cặp bỏ sót là dương thật).")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "summarize"])
    ap.add_argument("--blank", choices=["skip", "positive"], default="skip")
    a = ap.parse_args()
    make() if a.cmd == "make" else summarize(a.blank)
