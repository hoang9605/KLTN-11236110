"""File Excel cho chuyên gia duyệt nhãn AI (1 = AI đúng, 0 = AI sai) và chấm điểm sau khi duyệt.

Chuyên gia KHÔNG cần đọc nhãn BIO hay mã quan hệ tiếng Anh:
  - câu được hiển thị bình thường, thực thể 1 tô ĐỎ đậm, thực thể 2 tô XANH đậm;
  - mỗi dòng là một câu hỏi tiếng Việt ("«đau» có xảy ra ở «thắt lưng» không?") và câu trả lời của AI (CÓ / KHÔNG);
  - chuyên gia chỉ điền cột ĐÁNH GIÁ: 1 nếu AI trả lời đúng, 0 nếu sai (có danh sách chọn 1/0).
Cột kỹ thuật (mã bản ghi, cờ kiểm tra K1–K7, số phiếu…) nằm bên phải, được gộp nhóm và thu gọn.

Các sheet:
  Hướng dẫn   cách chấm, nghĩa của từng câu hỏi, ô ghi tên người duyệt và ngày duyệt
  Quan hệ     mỗi dòng một cặp thực thể cần chấm
  Thực thể    các thực thể AI cho là KHÔNG hợp lệ (cặp của chúng đã bị bỏ): chuyên gia chấm AI đúng/sai
  Câu sinh    (chỉ dữ liệu sinh) mỗi câu: có tự nhiên và hợp lý không (1/0)

Phân bổ công duyệt (CoAnnotating, Li et al. 2023): tầng B (có cờ hoặc LLM tự bất đồng) duyệt 100%;
tầng A chỉ đưa một mẫu ngẫu nhiên (a_fraction).

Chấm điểm sau khi chuyên gia điền:
    .venv\\Scripts\\python.exe -X utf8 -m re_v3.expert_review <file .xlsx đã điền>
Ghi <tên>_score.json (accuracy + CI95 Wilson, kappa, hiệu quả từng cờ) và
<tên>_expert_final.jsonl (nhãn sau khi áp quyết định của chuyên gia; chỉ khi đã điền tên + ngày duyệt).
"""
import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

from relation_extraction.data import NEGATIVE

TYPE_VI = {"CONDITION": "Bệnh / triệu chứng", "DRUG": "Thuốc", "BODY_PART": "Bộ phận cơ thể",
           "TEST": "Xét nghiệm / thăm khám", "PROCEDURE": "Thủ thuật / phương pháp điều trị",
           "DOSAGE": "Liều lượng"}
# (dương, âm): quan hệ AI đưa ra viết thành câu ngắn, ví dụ «ung thư nội mạc tử cung» ở «tử cung»
RELATION_VI = {
    "located_at": ("«{h}» ở «{t}»", "«{h}» KHÔNG ở «{t}»"),
    "treated_by": ("«{h}» được chữa bằng thuốc «{t}»", "«{h}» KHÔNG được chữa bằng thuốc «{t}»"),
    "treated_by_procedure": ("«{h}» được chữa bằng «{t}»", "«{h}» KHÔNG được chữa bằng «{t}»"),
    "diagnosed_by": ("«{h}» được phát hiện / chẩn đoán bằng «{t}»", "«{h}» KHÔNG được phát hiện / chẩn đoán bằng «{t}»"),
    "has_dosage": ("thuốc «{h}» dùng liều «{t}»", "«{t}» KHÔNG phải liều của thuốc «{h}»"),
}


def relation_statement(relation, label, h, t):
    pos, neg = RELATION_VI[relation]
    return (neg if label == NEGATIVE else pos).format(h=h, t=t)
RED, BLUE = "C00000", "1F4E9A"
HEAD_FILL = PatternFill("solid", fgColor="1F3864")
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
TECH_FILL = PatternFill("solid", fgColor="EDEDED")
THIN = Border(*(Side(style="thin", color="BFBFBF"),) * 4)
WRAP = Alignment(wrap_text=True, vertical="top")

REL_COLS = [("STT", 6), ("Câu", 60), ("Thực thể 1 (đỏ)", 18), ("Loại 1", 16), ("Thực thể 2 (xanh)", 18),
            ("Loại 2", 16), ("Quan hệ AI đưa ra", 45), ("Bằng chứng AI dựa vào", 26),
            ("ĐÁNH GIÁ: quan hệ này có đúng không?\n1 = đúng\n0 = sai", 16), ("Ghi chú của chuyên gia", 28)]
REL_TECH = ["record_id", "head_id", "tail_id", "relation", "ai_label", "tier", "kb_flags", "ai_votes",
            "rule_label", "corpus_support", "head_code", "tail_code", "is_target", "variant", "parent_id"]
ENT_COLS = [("STT", 6), ("Câu", 60), ("Thực thể (đỏ)", 20), ("Loại NER gán", 18), ("Câu hỏi", 40),
            ("AI trả lời", 10), ("ĐÁNH GIÁ\n1 = AI đúng\n0 = AI sai", 13), ("Ghi chú của chuyên gia", 28)]
ENT_TECH = ["record_id", "entity_id", "label", "ai_validity"]
SYN_COLS = [("STT", 6), ("Câu sinh", 70), ("Câu này có tự nhiên như lời người thật nói và hợp lý về y khoa không?", 30),
            ("ĐÁNH GIÁ\n1 = có\n0 = không", 13), ("Ghi chú của chuyên gia", 28)]
SYN_TECH = ["record_id", "variant", "parent_id"]


# ---------------------------------------------------------------------------
# Viết file Excel
# ---------------------------------------------------------------------------
def rich_sentence(text, spans):
    """spans: [(start, end, màu)] -> ô có thực thể tô màu, đậm, kèm ngoặc «» để in đen trắng vẫn thấy."""
    parts, pos = [], 0
    for s, e, color in sorted(spans):
        if s > pos:
            parts.append(TextBlock(InlineFont(), text[pos:s]))
        parts.append(TextBlock(InlineFont(b=True, color=color), f"«{text[s:e]}»"))
        pos = e
    if pos < len(text):
        parts.append(TextBlock(InlineFont(), text[pos:]))
    return CellRichText(*parts)


def _code(checks):
    for k, field in (("K1", "icd10"), ("K2", "rxnorm")):
        hit = (checks or {}).get(k, {}).get(field)
        if hit:
            return f"{hit['code']} {hit['name']}"
    return ""


def _sheet(wb, title, cols, tech):
    ws = wb.create_sheet(title)
    headers = [c for c, _ in cols] + tech
    ws.append(headers)
    for i, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=i)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HEAD_FILL if i <= len(cols) else PatternFill("solid", fgColor="7F7F7F")
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        letter = cell.column_letter
        ws.column_dimensions[letter].width = cols[i - 1][1] if i <= len(cols) else 14
        if i > len(cols):
            ws.column_dimensions[letter].outlineLevel = 1
            ws.column_dimensions[letter].hidden = True
    ws.row_dimensions[1].height = 48
    ws.freeze_panes = "C2"
    return ws


def _finish(ws, n_cols, input_cols):
    dv = DataValidation(type="list", formula1='"1,0"', allow_blank=True, showErrorMessage=True,
                        errorTitle="Chỉ nhập 1 hoặc 0", error="1 = AI đúng, 0 = AI sai")
    ws.add_data_validation(dv)
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for c in row:
            c.alignment = WRAP
            c.border = THIN
            if c.column > n_cols:
                c.fill = TECH_FILL
        for col in input_cols:
            row[col - 1].fill = INPUT_FILL
            row[col - 1].alignment = Alignment(horizontal="center", vertical="top")
    if ws.max_row >= 2:
        for col in input_cols[:1]:
            letter = ws.cell(row=1, column=col).column_letter
            dv.add(f"{letter}2:{letter}{ws.max_row}")
    ws.auto_filter.ref = ws.dimensions


def write_xlsx(path, records, a_fraction=1.0, seed=42, title="Duyệt nhãn quan hệ y khoa", with_entities=False):
    """records: định dạng repo + kb_validation. Trả về Counter số dòng theo (tầng, có đưa duyệt)."""
    rng = random.Random(seed)
    wb = Workbook()
    guide = wb.active
    guide.title = "Hướng dẫn"
    rel = _sheet(wb, "Quan hệ", REL_COLS, REL_TECH)
    ent = _sheet(wb, "Thực thể", ENT_COLS, ENT_TECH) if with_entities else None
    synth = any(r.get("variant") for r in records)
    syn = _sheet(wb, "Câu sinh", SYN_COLS, SYN_TECH) if synth else None
    stats = Counter()
    n_rel = n_ent = n_syn = 0
    ordered = sorted(records, key=lambda r: (r["kb_validation"]["tier"] != "B", r["id"]))
    for r in ordered:
        kb = r["kb_validation"]
        sample = kb["tier"] == "B" or rng.random() < a_fraction
        stats[(kb["tier"], int(sample))] += len(r["relations"])
        if not sample:
            continue
        ents = {e["id"]: e for e in r["entities"]}
        pchecks = {(p["head"], p["tail"]): p for p in kb.get("pairs", [])}
        for x in r["relations"]:
            h, t = ents[x["head"]], ents[x["tail"]]
            pc = pchecks.get((x["head"], x["tail"]), {})
            n_rel += 1
            rel.append([n_rel, None, h["text"], TYPE_VI[h["label"]], t["text"], TYPE_VI[t["label"]],
                        relation_statement(x["allowed_relation"], x["label"], h["text"], t["text"]),
                        x.get("evidence") or "", None, None,
                        r["id"], h["id"], t["id"], x["allowed_relation"], x["label"], kb["tier"],
                        " ".join(kb["flags"]), x.get("votes", ""), pc.get("K6", {}).get("rule_label", ""),
                        pc.get("K7", {}).get("support", ""), _code(kb.get("entities", {}).get(h["id"])),
                        _code(kb.get("entities", {}).get(t["id"])),
                        int(x.get("label_source") == "target+verifier"), r.get("variant", ""), r.get("parent_id", "")])
            rel.cell(row=rel.max_row, column=2).value = rich_sentence(
                r["text"], [(h["start"], h["end"], RED), (t["start"], t["end"], BLUE)])
        for e in (r["entities"] if ent is not None else []):
            if e.get("validity") == "INVALID":
                n_ent += 1
                ent.append([n_ent, None, e["text"], TYPE_VI[e["label"]],
                            f"«{e['text']}» có đúng là {TYPE_VI[e['label']].lower()} cụ thể không?",
                            "KHÔNG", None, None, r["id"], e["id"], e["label"], "INVALID"])
                ent.cell(row=ent.max_row, column=2).value = rich_sentence(r["text"], [(e["start"], e["end"], RED)])
        if syn is not None:
            n_syn += 1
            syn.append([n_syn, r["text"], "", None, None, r["id"], r.get("variant", ""), r.get("parent_id", "")])
    _finish(rel, len(REL_COLS), [9])
    if ent is not None:
        _finish(ent, len(ENT_COLS), [7])
    if syn is not None:
        _finish(syn, len(SYN_COLS), [4])
    _write_guide(guide, title, n_rel, n_ent, n_syn)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return stats


def _write_guide(ws, title, n_rel, n_ent, n_syn):
    rows = [
        (title, True),
        ("", False),
        ("Người duyệt (bắt buộc, ghi họ tên):", True),
        ("Ngày duyệt (bắt buộc, dd/mm/yyyy):", True),
        ("", False),
        ("CÁCH CHẤM", True),
        (f"1. Sheet «Quan hệ» ({n_rel} dòng): đọc câu (thực thể 1 tô ĐỎ, thực thể 2 tô XANH) và cột «Quan hệ AI đưa "
         "ra». Hỏi: quan hệ này có đúng không? Ở cột ĐÁNH GIÁ (ô vàng): ghi 1 nếu ĐÚNG, ghi 0 nếu SAI. "
         "Ví dụ: AI ghi «ung thư nội mạc tử cung» ở «tử cung» và câu đúng là nói vậy → ghi 1. "
         "AI ghi «đau» KHÔNG ở «lưng» nhưng câu thật ra nói đau lưng → ghi 0.", False),
        ((f"2. Sheet «Thực thể» ({n_ent} dòng): các cụm AI cho là KHÔNG phải thực thể y khoa cụ thể nên đã bỏ qua. "
          "Ghi 1 nếu đồng ý với AI, 0 nếu thật ra đó là thực thể hợp lệ.") if n_ent else "", False),
        ((f"3. Sheet «Câu sinh» ({n_syn} dòng): câu do máy viết. Ghi 1 nếu câu nghe như lời người thật nói và hợp lý "
          "về y khoa, 0 nếu không.") if n_syn else "", False),
        ("4. Chỉ dựa vào chính câu đó, không suy từ kiến thức bên ngoài. Câu là lời nói được ghi lại, không có dấu câu "
         "và có thể bị cắt ngang ở đầu hoặc cuối.", False),
        ("5. Trường hợp khó hoặc hướng dẫn chưa nói tới: vẫn chấm 1 hoặc 0 theo ý anh/chị, và ghi lý do ở cột Ghi chú.", False),
        ("6. Các cột màu xám bên phải là thông tin kỹ thuật, không cần đọc và không sửa.", False),
        ("", False),
        ("KHI NÀO QUAN HỆ ĐƯỢC TÍNH LÀ CÓ (theo hướng dẫn gán nhãn)", True),
        ("• «bệnh» xảy ra ở «bộ phận»: câu nói bệnh/triệu chứng ở bộ phận đó. Câu phủ định («không còn đau khớp gối») "
         "vẫn tính là CÓ.", False),
        ("• Thuốc / thủ thuật dùng để chữa «bệnh»: câu nói đã dùng, nên dùng, hoặc «nếu bị … thì dùng …», kể cả khi dùng "
         "mà không đỡ. KHÔNG tính khi: dùng để phòng bệnh chưa mắc, thuốc gây ra bệnh (tác dụng phụ), câu hỏi chưa có "
         "câu trả lời, hoặc câu nói không nên dùng.", False),
        ("• Xét nghiệm dùng để phát hiện / chẩn đoán «bệnh»: KHÔNG tính nếu xét nghiệm và bệnh chỉ cùng xuất hiện "
         "trong câu.", False),
        ("• «liều» là liều của «thuốc»: KHÔNG tính nếu lượng đó là của thứ khác hoặc là số liệu thống kê.", False),
    ]
    ws.column_dimensions["A"].width = 120
    ws.column_dimensions["B"].width = 30
    for i, (text, bold) in enumerate(rows, 1):
        c = ws.cell(row=i, column=1, value=text)
        c.font = Font(bold=bold, size=14 if i == 1 else 11)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in (3, 4):
        ws.cell(row=r, column=2).fill = INPUT_FILL
        ws.cell(row=r, column=2).border = THIN


# ---------------------------------------------------------------------------
# Đọc file đã duyệt và chấm điểm
# ---------------------------------------------------------------------------
def _rows(ws, n_cols, tech):
    header = [c.value for c in ws[1]]
    j = next(i for i, h in enumerate(header) if str(h).startswith("ĐÁNH GIÁ"))
    n = next(i for i, h in enumerate(header) if str(h).startswith("Ghi chú"))
    out = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(header, row))
        out.append({"judge": row[j], "note": row[n] or "", **{k: d.get(k) for k in tech}})
    return out


def _judge(v):
    s = str(v).strip() if v is not None else ""
    return int(float(s)) if s in ("1", "0", "1.0", "0.0") else None


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h


def cohen_kappa(a, b):
    labels = sorted(set(a) | set(b))
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[l] * cb[l] for l in labels) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def _rate(rows):
    k = sum(r["judge"] == 1 for r in rows)
    p, lo, hi = wilson(k, len(rows))
    return {"n": len(rows), "correct": k, "acc": round(p, 3), "ci95": [round(lo, 3), round(hi, 3)]}


def read_review(path):
    wb = load_workbook(path)
    guide = wb["Hướng dẫn"]
    reviewer = {"name": guide["B3"].value, "date": str(guide["B4"].value) if guide["B4"].value else None}
    rel = [r for r in _rows(wb["Quan hệ"], len(REL_COLS), REL_TECH) if r["record_id"]]
    ent = [r for r in _rows(wb["Thực thể"], len(ENT_COLS), ENT_TECH) if r["record_id"]] if "Thực thể" in wb.sheetnames else []
    syn = [r for r in _rows(wb["Câu sinh"], len(SYN_COLS), SYN_TECH) if r["record_id"]] if "Câu sinh" in wb.sheetnames else []
    for r in rel + ent + syn:
        r["judge"] = _judge(r["judge"])
    return reviewer, rel, ent, syn


def score_rows(rel, ent, syn):
    done = [r for r in rel if r["judge"] is not None]
    for r in done:
        r["expert_label"] = r["ai_label"] if r["judge"] == 1 else (NEGATIVE if r["ai_label"] != NEGATIVE else r["relation"])
    out = {"relation_rows": len(rel), "reviewed": len(done), "not_reviewed": len(rel) - len(done)}
    groups = defaultdict(list)
    for r in done:
        pol = "CÓ" if r["ai_label"] != NEGATIVE else "KHÔNG"
        for key in ("ALL", f"tier={r['tier']}", f"relation={r['relation']}", f"relation={r['relation']}|AI={pol}",
                    f"target={r['is_target']}"):
            groups[key].append(r)
        if r.get("variant"):
            groups[f"variant={r['relation']}|{r['variant']}"].append(r)
    out["ai_accuracy"] = {k: _rate(v) for k, v in sorted(groups.items())}
    pos = [r for r in done if r["ai_label"] != NEGATIVE]
    gold_pos = [r for r in done if r["expert_label"] != NEGATIVE]
    tp = sum(r["judge"] == 1 for r in pos)
    out["ai_precision"] = round(tp / len(pos), 3) if pos else None
    out["ai_recall"] = round(tp / len(gold_pos), 3) if gold_pos else None
    out["kappa_ai_vs_expert"] = round(cohen_kappa([r["ai_label"] for r in done], [r["expert_label"] for r in done]), 3)
    rl = [r for r in done if r.get("rule_label")]
    out["kappa_rule_vs_expert"] = round(cohen_kappa([r["rule_label"] for r in rl], [r["expert_label"] for r in rl]), 3)
    flag_eff = {}
    for flag in ("K1", "K2", "K3", "K4", "K5", "K6", "K7", "SC"):
        f = [r for r in done if flag in (r.get("kb_flags") or "")]
        nf = [r for r in done if flag not in (r.get("kb_flags") or "")]
        err = lambda rs: round(sum(r["judge"] == 0 for r in rs) / len(rs), 3) if rs else None
        flag_eff[flag] = {"n_flagged": len(f), "ai_error_if_flagged": err(f), "ai_error_if_not": err(nf)}
    out["flag_effectiveness"] = flag_eff
    e = [r for r in ent if r["judge"] is not None]
    out["entity_invalid_decisions"] = _rate(e) if e else None
    s = [r for r in syn if r["judge"] is not None]
    out["synthetic_natural"] = _rate(s) if s else None
    return out


def apply_review(records, reviewer, rel, ent, syn):
    """Áp quyết định chuyên gia lên bản ghi. Bản ghi có mọi dòng đã chấm mới được human_verified = true."""
    by = defaultdict(list)
    for r in rel:
        by[r["record_id"]].append(r)
    ent_by = defaultdict(list)
    for r in ent:
        ent_by[r["record_id"]].append(r)
    syn_by = {r["record_id"]: r for r in syn}
    out = []
    for rec in records:
        rows = by.get(rec["id"], [])
        erows = ent_by.get(rec["id"], [])
        if not rows and not erows and rec["id"] not in syn_by:
            continue
        rec = json.loads(json.dumps(rec))
        decided = {(r["head_id"], r["tail_id"]): r for r in rows if r["judge"] is not None}
        for x in rec["relations"]:
            d = decided.get((x["head"], x["tail"]))
            if d:
                x["ai_label"] = x["label"]
                x["label"] = d["expert_label"] if "expert_label" in d else (
                    x["label"] if d["judge"] == 1 else (NEGATIVE if x["label"] != NEGATIVE else x["allowed_relation"]))
                x["expert_note"] = d["note"]
        needs = [r["entity_id"] for r in erows if r["judge"] == 0]
        for e in rec["entities"]:
            if e["id"] in needs:
                e["validity"] = "VALID"
                e["expert_overrode_invalid"] = True
        s = syn_by.get(rec["id"])
        if s and s["judge"] is not None:
            rec["expert_natural"] = s["judge"]
        complete = (all(r["judge"] is not None for r in rows) and all(r["judge"] is not None for r in erows)
                    and (not s or s["judge"] is not None))
        rec["human_verified"] = bool(complete)
        rec["needs_relabel_entities"] = needs
        rec["reviewer"] = reviewer
        out.append(rec)
    return out


def main():
    ap = argparse.ArgumentParser(description="Chấm file Excel chuyên gia đã duyệt")
    ap.add_argument("xlsx")
    ap.add_argument("--records", help="file .jsonl đã xuất cùng lúc với file Excel (mặc định: cùng tên, bỏ _expert_review)")
    a = ap.parse_args()
    path = Path(a.xlsx)
    reviewer, rel, ent, syn = read_review(path)
    res = score_rows(rel, ent, syn)
    res["reviewer"] = reviewer
    base = path.with_name(path.stem.replace("_expert_review", ""))
    (base.parent / f"{base.name}_score.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    rec_path = Path(a.records) if a.records else base.parent / f"{base.name}.jsonl"
    if not (reviewer["name"] and reviewer["date"]):
        print("\nChưa ghi tên và ngày duyệt ở sheet «Hướng dẫn» (ô B3, B4): chỉ chấm điểm, KHÔNG xuất nhãn cuối.")
        return
    if rec_path.exists():
        from .common import read_jsonl, write_jsonl
        final = apply_review(read_jsonl(rec_path), reviewer, rel, ent, syn)
        out = base.parent / f"{base.name}_expert_final.jsonl"
        write_jsonl(out, final)
        print(f"\nĐã xuất nhãn cuối ({sum(r['human_verified'] for r in final)}/{len(final)} bản ghi duyệt đủ): {out}")


if __name__ == "__main__":
    main()
