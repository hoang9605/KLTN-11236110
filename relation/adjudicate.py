"""Phân xử nhãn test: đặt nhãn người (gán mù) cạnh nhãn AI ở mọi chỗ hai bên lệch nhau, người chốt nhãn cuối.

Kết quả gán mù được giữ nguyên để báo cáo:
  relation/data/test_blind.jsonl            nhãn người gán mù
  relation/data/ai_agreement_test_blind.json  kappa người–AI trước phân xử

  make:   .venv\\Scripts\\python.exe -X utf8 -m relation.adjudicate make
          -> relation/data/test_adjudication.xlsx
  import: .venv\\Scripts\\python.exe -X utf8 -m relation.adjudicate import
          -> relation/data/test.jsonl (nhãn cuối), relation/data/adjudication_summary.json

Dòng đưa vào phiếu:
  - thực thể: nhãn người khác nhãn AI
  - cặp: nhãn người khác nhãn AI, kể cả khi một bên bỏ qua cặp vì coi một thực thể là INVALID
Chỗ người và AI trùng nhau giữ nguyên nhãn người, không đưa vào phiếu.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill, Protection
from openpyxl.worksheet.datavalidation import DataValidation

from .ai_batches import load, marked
from .make_sheet import mark_pair

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
SHEET = DATA / "test_adjudication.xlsx"
NEGATIVE = "NO_RELATION"

RULE = {
    "located_at": "Dương khi bệnh hoặc triệu chứng xảy ra ở chính bộ phận đó. Âm khi bộ phận chỉ được nhắc cùng câu, "
                  "hoặc gắn với triệu chứng khác.",
    "treated_by": "Dương khi thuốc được dùng hoặc chỉ định để chữa, giảm, kiểm soát chính bệnh đó. Âm khi chỉ cùng câu, "
                  "phòng bệnh chưa mắc, tác dụng phụ, câu hỏi chưa có trả lời.",
    "treated_by_procedure": "Dương khi thủ thuật được dùng để chữa, giảm, kiểm soát chính bệnh đó. Âm khi chỉ cùng câu, "
                            "phòng bệnh chưa mắc, tác dụng phụ, câu hỏi chưa có trả lời.",
    "diagnosed_by": "Dương khi xét nghiệm hay thăm khám dùng để phát hiện, chẩn đoán, theo dõi chính bệnh đó. "
                    "Âm khi xét nghiệm và bệnh chỉ cùng xuất hiện.",
    "has_dosage": "Dương khi liều hay lượng là của chính thuốc đó. Âm khi lượng là của thứ khác hoặc là thống kê.",
}


def _human_ai():
    key = {r["id"]: r for r in load(DATA / "test_sheet_key.jsonl")}
    human = {r["id"]: r for r in load(DATA / "test_blind.jsonl")}
    ai = {r["id"]: r for r in load(DATA / "ai" / "test_b1_passA.jsonl")}
    return key, human, ai


def _pair_labels(h):
    return {(r["head"], r["tail"]): r["label"] for r in h["relations"]}


def make():
    key, human, ai = _human_ai()
    ent_rows, pair_rows = [], []
    for s in key.values():
        sid, h, a = s["id"], human[s["id"]], ai[s["id"]]
        E = {e["id"]: e for e in s["entities"]}
        hv = {e["id"]: e["validity"] for e in h["entities"]}
        mk = marked(s["text"], s["entities"])
        for e in s["entities"]:
            if hv[e["id"]] != a["entities"][e["id"]]:
                ent_rows.append([s["sentence_no"], sid, e["id"], e["label"], e["text"], mk,
                                 hv[e["id"]], a["entities"][e["id"]], "", ""])
        hl = _pair_labels(h)
        for p in s["pairs"]:
            x = hl.get((p["head"], p["tail"]))
            y = a["pairs"].get(p["pair_id"])
            ent_dis = any(hv[k] != a["entities"][k] for k in (p["head"], p["tail"]))
            if x == y and not (x is None and ent_dis):
                continue
            pair_rows.append([s["sentence_no"], sid, p["pair_id"], p["allowed_relation"],
                              f'{E[p["head"]]["text"]} ({p["head"]})', f'{E[p["tail"]]["text"]} ({p["tail"]})',
                              mark_pair(s["text"], E[p["head"]], E[p["tail"]]),
                              x or "bỏ qua (thực thể INVALID)", y or "bỏ qua (thực thể INVALID)",
                              RULE[p["allowed_relation"]], "", ""])
    wb = Workbook()
    ws = wb.active; ws.title = "README"
    for line in [
        "Phiếu phân xử tập test. Mỗi dòng là một chỗ nhãn gán mù của bạn khác nhãn AI. Hướng dẫn: relation/guideline.md.",
        "Cột human là nhãn bạn gán mù, cột ai là nhãn AI. Cả hai chỉ để tham khảo; đọc lại câu và chọn nhãn đúng theo hướng dẫn ở cột final.",
        "Làm sheet entities trước. Sheet pairs: nếu sau phân xử một thực thể của cặp là INVALID thì để trống final.",
        "Mỗi dòng của sheet pairs chỉ chọn được đúng quan hệ của dòng hoặc NO_RELATION. Sheet bị khóa trừ cột final và note.",
        "Những chỗ bạn và AI trùng nhau không có trong phiếu và giữ nguyên nhãn của bạn.",
    ]:
        ws.append([line])
    ws.column_dimensions["A"].width = 130
    we = wb.create_sheet("entities")
    we.append(["sentence_no", "sentence_id", "entity_id", "type", "mention", "sentence", "human", "ai", "final", "note"])
    for r in ent_rows:
        we.append(r)
    dv = DataValidation(type="list", formula1='"VALID,INVALID"', allow_blank=True, showErrorMessage=True)
    we.add_data_validation(dv)
    if ent_rows:
        dv.add(f"I2:I{len(ent_rows) + 1}")
    wp = wb.create_sheet("pairs")
    wp.append(["sentence_no", "sentence_id", "pair_id", "relation", "head", "tail", "sentence", "human", "ai", "rule",
               "final", "note"])
    dvs = {}
    for i, r in enumerate(pair_rows, 2):
        wp.append(r)
        rel = r[3]
        if rel not in dvs:
            dvs[rel] = DataValidation(type="list", formula1=f'"{rel},{NEGATIVE}"', allow_blank=True,
                                      showErrorMessage=True, errorTitle="Sai nhãn", error=f"Chỉ chọn {rel} hoặc {NEGATIVE}")
            wp.add_data_validation(dvs[rel])
        dvs[rel].add(wp.cell(i, 11))
    yellow = PatternFill("solid", fgColor="FFF2CC")
    for sheet, cols, widths in ((we, (9, 10), {"F": 90, "E": 22}), (wp, (11, 12), {"G": 80, "J": 45, "E": 22, "F": 22})):
        for c in sheet[1]:
            c.font = Font(bold=True)
        for row in sheet.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
            for k in cols:
                row[k - 1].protection = Protection(locked=False)
                row[k - 1].fill = yellow
        for col, w in widths.items():
            sheet.column_dimensions[col].width = w
        sheet.freeze_panes = "A2"
        sheet.protection.sheet = True
        sheet.protection.formatRows = False
        sheet.protection.formatColumns = False
    wb.save(SHEET)
    print(json.dumps({"sheet": str(SHEET), "entity_rows": len(ent_rows), "pair_rows": len(pair_rows),
                      "pair_rows_by_relation": dict(Counter(r[3] for r in pair_rows))}, ensure_ascii=False, indent=1))


def _rows(ws):
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:] if any(v is not None for v in r)]


def _clean(v):
    return str(v).strip() if v is not None else ""


def do_import():
    key, human, ai = _human_ai()
    wb = load_workbook(SHEET, data_only=True)
    ent_fix = {(r["sentence_id"], r["entity_id"]): (_clean(r["final"]).upper(), _clean(r["note"])) for r in _rows(wb["entities"])}
    pair_fix = {(r["sentence_id"], r["pair_id"]): (_clean(r["final"]), _clean(r["note"])) for r in _rows(wb["pairs"])}
    errors, out, stats = [], [], Counter()
    for s in key.values():
        sid, h, a = s["id"], human[s["id"]], ai[s["id"]]
        hv = {e["id"]: e["validity"] for e in h["entities"]}
        final_v, notes = {}, [h["note"]] if h.get("note") else []
        for e in s["entities"]:
            if (sid, e["id"]) in ent_fix:
                v, n = ent_fix[(sid, e["id"])]
                if v not in ("VALID", "INVALID"):
                    errors.append(f"câu {s['sentence_no']} ({sid}) {e['id']} '{e['text']}': final '{v}' phải là VALID/INVALID")
                stats["entity_adjudicated"] += 1
                stats["entity_changed_from_human"] += v != hv[e["id"]]
                if n:
                    notes.append(f"phân xử {e['id']}: {n}")
            else:
                v = hv[e["id"]]
            final_v[e["id"]] = v
        hl = _pair_labels(h)
        rels = []
        for p in s["pairs"]:
            ok = final_v[p["head"]] == "VALID" and final_v[p["tail"]] == "VALID"
            x, y = hl.get((p["head"], p["tail"])), a["pairs"].get(p["pair_id"])
            if (sid, p["pair_id"]) in pair_fix:
                lab, n = pair_fix[(sid, p["pair_id"])]
                if n:
                    notes.append(f"phân xử {p['pair_id']}: {n}")
                if ok and lab not in (p["allowed_relation"], NEGATIVE):
                    errors.append(f"câu {s['sentence_no']} ({sid}) {p['pair_id']}: final '{lab}' phải là "
                                  f"{p['allowed_relation']} hoặc {NEGATIVE}")
                    continue
                if not ok and lab:
                    errors.append(f"câu {s['sentence_no']} ({sid}) {p['pair_id']}: có thực thể INVALID sau phân xử nên để trống")
                    continue
                src = "adjudicated"
                stats["pair_adjudicated"] += 1
            else:
                lab, src = x, "human_ai_agree"
                if ok and lab is None:
                    errors.append(f"câu {s['sentence_no']} ({sid}) {p['pair_id']}: hai thực thể VALID nhưng không có nhãn "
                                  "(cặp không có trong phiếu); chạy lại make")
                    continue
            if ok:
                rels.append({"head": p["head"], "tail": p["tail"], "allowed_relation": p["allowed_relation"],
                             "label": lab, "source": src, "blind_human": x, "ai": y})
                stats[f"{p['allowed_relation']}:{'pos' if lab != NEGATIVE else 'neg'}"] += 1
                if src == "adjudicated":
                    stats["pair_final_eq_human"] += lab == x
                    stats["pair_final_eq_ai"] += lab == y
        out.append({"id": sid, "source_split": s["source_split"], "source_row_index": s["source_row_index"],
                    "text": s["text"],
                    "entities": [{**e, "validity": final_v[e["id"]], "blind_human": hv[e["id"]],
                                  "ai": a["entities"][e["id"]]} for e in s["entities"]],
                    "relations": rels, "annotator": "human_adjudicated",
                    "annotation_source": "test_blind.jsonl + test_adjudication.xlsx",
                    "note": "; ".join(notes) or None})
    if errors:
        print(f"{len(errors)} lỗi, chưa ghi file:")
        print("\n".join(errors[:200]))
        raise SystemExit(1)
    with open(DATA / "test.jsonl", "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary = {"sentences": len(out), **dict(sorted(stats.items()))}
    (DATA / "adjudication_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "import"])
    a = ap.parse_args()
    make() if a.cmd == "make" else do_import()


if __name__ == "__main__":
    main()
