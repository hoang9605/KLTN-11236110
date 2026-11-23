"""Phiếu duyệt nhãn seed và dev: AI gán (hai lượt), người chuyên môn duyệt từng nhãn.

Phiếu có mọi thực thể và mọi cặp của 600 câu. Cột final được điền sẵn nhãn khi hai lượt AI trùng nhau,
để trống khi hai lượt bất đồng. Người duyệt đọc và sửa bất kỳ ô final nào thấy sai, và bắt buộc điền ô trống.
Quy định bổ sung sau tập test cũng được điền sẵn: PROCEDURE chỉ gồm "điều trị" là INVALID.

  make:   .venv\\Scripts\\python.exe -X utf8 -m relation.review_seed make
          -> relation/data/seed_review.xlsx
  import: .venv\\Scripts\\python.exe -X utf8 -m relation.review_seed import
          -> relation/data/seed.jsonl, relation/data/dev.jsonl, relation/data/seed_review_summary.json
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill, Protection
from openpyxl.worksheet.datavalidation import DataValidation

from .ai_batches import load

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
AI = DATA / "ai"
SHEET = DATA / "seed_review.xlsx"
NEGATIVE = "NO_RELATION"
AGREED, CHOOSE, RULE = "AI thống nhất", "cần chọn", "quy định bổ sung"


def is_rule_invalid(e):
    return e["label"] == "PROCEDURE" and e["text"].strip().lower() == "điều trị"


def collect():
    """Câu theo thứ tự seed rồi dev, kèm nhãn hai lượt AI và offset thực thể."""
    src = {r["id"]: r for f in ("seed_unlabeled.jsonl", "dev_unlabeled.jsonl") for r in load(DATA / f)}
    dev_ids = {r["id"] for r in load(DATA / "dev_unlabeled.jsonl")}
    out = []
    for f in sorted(AI.glob("seed_b*_input.jsonl")):
        stem = f.name.replace("_input.jsonl", "")
        A = {r["id"]: r for r in load(AI / f"{stem}_passA.jsonl")}
        B = {r["id"]: r for r in load(AI / f"{stem}_passB.jsonl")}
        for it in load(f):
            off = {e["id"]: e for e in src[it["id"]]["entities"]}
            out.append({**it, "split": "dev" if it["id"] in dev_ids else "seed", "A": A[it["id"]], "B": B[it["id"]],
                        "offsets": off, "source": src[it["id"]]})
    return out


def make():
    if SHEET.exists():
        wb0 = load_workbook(SHEET, read_only=True)
        if "README" in wb0.sheetnames and any("người chuyên môn duyệt" in str(r[0].value)
                                               for r in wb0["README"].iter_rows(max_row=3)):
            raise SystemExit(f"{SHEET} đã tồn tại và có thể đã được duyệt; xóa hoặc đổi tên trước khi tạo lại.")
    items = collect()
    wb = Workbook()
    ws = wb.active; ws.title = "README"
    for line in [
        "Phiếu người chuyên môn duyệt nhãn AI cho 600 câu seed và dev. Hướng dẫn: relation/guideline.md.",
        "Cột final đã điền sẵn nhãn khi hai lượt AI trùng nhau (status = AI thống nhất). Ô final trống (status = cần chọn) bắt buộc phải điền.",
        "Đọc từng dòng và sửa bất kỳ ô final nào sai. Làm sheet entities trước, sau đó sheet pairs.",
        "Sheet pairs: cột skip tự hiện SKIP khi một thực thể của cặp có final là INVALID; dòng SKIP không cần nhãn.",
        "Mỗi dòng pairs chỉ chọn được đúng quan hệ của dòng hoặc NO_RELATION. Sheet bị khóa trừ cột final và note; có thể dùng bộ lọc.",
    ]:
        ws.append([line])
    ws.column_dimensions["A"].width = 130
    we = wb.create_sheet("entities")
    we.append(["sentence_id", "entity_id", "split", "type", "mention", "sentence", "passA", "passB", "status", "final", "note"])
    wp = wb.create_sheet("pairs")
    wp.append(["sentence_id", "pair_id", "split", "relation", "head", "tail", "sentence", "passA", "passB", "status",
               "skip", "final", "note"])
    yellow, orange = PatternFill("solid", fgColor="FFF2CC"), PatternFill("solid", fgColor="F8CBAD")
    dvs, stats = {}, Counter()
    ent_dv = DataValidation(type="list", formula1='"VALID,INVALID"', allow_blank=True, showErrorMessage=True)
    we.add_data_validation(ent_dv)
    for it in items:
        E = {e["id"]: e for e in it["entities"]}
        for e in it["entities"]:
            x, y = it["A"]["entities"][e["id"]], it["B"]["entities"][e["id"]]
            if is_rule_invalid(e):
                st, fin = RULE, "INVALID"
            elif x == y:
                st, fin = AGREED, x
            else:
                st, fin = CHOOSE, ""
            stats[f"entity_{st}"] += 1
            we.append([it["id"], e["id"], it["split"], e["label"], e["text"], it["marked_text"], x, y, st, fin, ""])
            r = we.max_row
            ent_dv.add(we.cell(r, 10))
            if st == CHOOSE:
                we.cell(r, 10).fill = orange
        for p in it["pairs"]:
            x, y = it["A"]["pairs"].get(p["pair_id"]), it["B"]["pairs"].get(p["pair_id"])
            st, fin = (AGREED, x) if x == y and x is not None else (CHOOSE, "")
            if x is None and y is None:
                st = AGREED  # cả hai lượt bỏ qua vì có thực thể INVALID
            stats[f"pair_{st}"] += 1
            r = wp.max_row + 1
            skip = (f'=IF(OR(COUNTIFS(entities!$A:$A,$A{r},entities!$B:$B,"{p["head"]}",entities!$J:$J,"INVALID")>0,'
                    f'COUNTIFS(entities!$A:$A,$A{r},entities!$B:$B,"{p["tail"]}",entities!$J:$J,"INVALID")>0),"SKIP","")')
            mk = it["marked_text"]
            wp.append([it["id"], p["pair_id"], it["split"], p["relation"], f'{E[p["head"]]["text"]} ({p["head"]})',
                       f'{E[p["tail"]]["text"]} ({p["tail"]})', mk, x or "-", y or "-", st, skip, fin or "", ""])
            rel = p["relation"]
            if rel not in dvs:
                dvs[rel] = DataValidation(type="list", formula1=f'"{rel},{NEGATIVE}"', allow_blank=True, showErrorMessage=True,
                                          errorTitle="Sai nhãn", error=f"Chỉ chọn {rel} hoặc {NEGATIVE}")
                wp.add_data_validation(dvs[rel])
            dvs[rel].add(wp.cell(r, 12))
            if st == CHOOSE:
                wp.cell(r, 12).fill = orange
    for sheet, cols, widths in ((we, (10, 11), {"F": 80, "E": 22}), (wp, (12, 13), {"G": 80, "E": 22, "F": 22})):
        for c in sheet[1]:
            c.font = Font(bold=True)
        for row in sheet.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
            for k in cols:
                row[k - 1].protection = Protection(locked=False)
                if row[k - 1].fill.fgColor.rgb in (None, "00000000"):
                    row[k - 1].fill = yellow
        for col, w in widths.items():
            sheet.column_dimensions[col].width = w
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions
        sheet.protection.sheet = True
        sheet.protection.autoFilter = False
        sheet.protection.formatRows = False
        sheet.protection.formatColumns = False
    wb.save(SHEET)
    print(json.dumps({"sheet": str(SHEET), "sentences": len(items), **dict(sorted(stats.items()))}, ensure_ascii=False, indent=1))


def _rows(ws):
    rows = list(ws.iter_rows(values_only=True))
    return [dict(zip(rows[0], r)) for r in rows[1:] if any(v is not None for v in r)]


def _clean(v):
    return str(v).strip() if v is not None else ""


def do_import(sheet=SHEET, out_dir=DATA, drop_unresolved=False):
    """drop_unresolved: ô final còn trống thì bỏ thực thể đó (validity None, mọi cặp chứa nó bị loại) và bỏ cặp đó,
    thay vì báo lỗi."""
    items = collect()
    wb = load_workbook(sheet, data_only=True)
    ent = {(r["sentence_id"], r["entity_id"]): (_clean(r["final"]).upper(), _clean(r["note"])) for r in _rows(wb["entities"])}
    pair = {(r["sentence_id"], r["pair_id"]): (_clean(r["final"]), _clean(r["note"])) for r in _rows(wb["pairs"])}
    errors, outs, stats = [], {"seed": [], "dev": []}, Counter()
    for it in items:
        sid, notes, val = it["id"], [], {}
        for e in it["entities"]:
            if (sid, e["id"]) not in ent:
                errors.append(f"{sid} {e['id']}: thiếu dòng thực thể"); continue
            v, nt = ent[(sid, e["id"])]
            if v == "" and drop_unresolved:
                stats["entity_unresolved_dropped"] += 1
                v = None
            elif v not in ("VALID", "INVALID"):
                errors.append(f"{sid} {e['id']} '{e['text']}': final '{v}' phải là VALID/INVALID")
            x, y = it["A"]["entities"][e["id"]], it["B"]["entities"][e["id"]]
            stats["entity_changed_from_ai_agreed"] += x == y and v != x
            if nt:
                notes.append(f"{e['id']}: {nt}")
            val[e["id"]] = v
        rels = []
        for p in it["pairs"]:
            ok = val.get(p["head"]) == "VALID" and val.get(p["tail"]) == "VALID"
            lab, nt = pair.get((sid, p["pair_id"]), ("", ""))
            if nt:
                notes.append(f"{p['pair_id']}: {nt}")
            if not ok:
                stats["pair_dropped_entity_unresolved"] += val.get(p["head"]) is None or val.get(p["tail"]) is None
                continue
            if lab == "" and drop_unresolved:
                stats["pair_unresolved_dropped"] += 1
                continue
            if lab not in (p["relation"], NEGATIVE):
                errors.append(f"{sid} {p['pair_id']}: final '{lab}' phải là {p['relation']} hoặc {NEGATIVE}"); continue
            x, y = it["A"]["pairs"].get(p["pair_id"]), it["B"]["pairs"].get(p["pair_id"])
            stats["pair_changed_from_ai_agreed"] += x == y and x is not None and lab != x
            stats[f"{it['split']}:{p['relation']}:{'neg' if lab == NEGATIVE else 'pos'}"] += 1
            rels.append({"head": p["head"], "tail": p["tail"], "allowed_relation": p["relation"], "label": lab,
                         "ai_passA": x, "ai_passB": y})
        s = it["source"]
        outs[it["split"]].append({
            "id": sid, "source_split": s.get("source_split"), "source_row_index": s.get("source_row_index"), "text": it["text"],
            "entities": [{"id": e["id"], "text": e["text"], "label": e["label"], "start": it["offsets"][e["id"]]["start"],
                          "end": it["offsets"][e["id"]]["end"], "validity": val.get(e["id"]),
                          "ai_passA": it["A"]["entities"][e["id"]], "ai_passB": it["B"]["entities"][e["id"]]}
                         for e in it["entities"]],
            "relations": rels, "annotator": "ai_labeled_expert_reviewed", "note": "; ".join(notes) or None})
    if errors:
        print(f"{len(errors)} lỗi, chưa ghi file:")
        print("\n".join(errors[:200]))
        raise SystemExit(1)
    for split, rows in outs.items():
        with open(out_dir / f"{split}.jsonl", "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary = {"seed_sentences": len(outs["seed"]), "dev_sentences": len(outs["dev"]), **dict(sorted(stats.items()))}
    (out_dir / "seed_review_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "import"])
    ap.add_argument("--drop-unresolved", action="store_true", help="bỏ thực thể và cặp còn để trống thay vì báo lỗi")
    a = ap.parse_args()
    make() if a.cmd == "make" else do_import(drop_unresolved=a.drop_unresolved)


if __name__ == "__main__":
    main()
