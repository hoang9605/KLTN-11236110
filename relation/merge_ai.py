"""Gộp hai lượt AI gán nhãn cho seed, đo độ đồng thuận, lập phiếu duyệt bất đồng cho người.

Đồng thuận:
  - thực thể: Cohen's kappa trên VALID/INVALID, mọi mention
  - cặp: Cohen's kappa trên nhãn quan hệ, chỉ tính cặp mà cả hai lượt đều coi hai thực thể là VALID
    (kappa nhị phân dương/âm), kèm tỉ lệ đồng ý thô
Nhãn gộp:
  - thực thể và cặp hai lượt trùng nhau: giữ nhãn chung, nguồn "ai_agreed"
  - bất đồng: chưa có nhãn, đưa vào phiếu duyệt; khi người duyệt xong, nhãn người thay thế
Phiếu duyệt (seed_review.xlsx) gồm: mọi thực thể bất đồng, mọi cặp bất đồng, và các cặp dương đã
đồng thuận của lớp hiếm (diagnosed_by, has_dosage, treated_by) để kiểm tra thêm, tối đa REVIEW_CAP dòng cặp.

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.merge_ai
Đầu ra: relation/data/seed_ai_merged.jsonl, relation/data/seed_review.xlsx, relation/data/ai_agreement_seed.json
"""
import json
import random
from collections import Counter
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.datavalidation import DataValidation
from sklearn.metrics import cohen_kappa_score

from .ai_batches import load, marked

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
AI = DATA / "ai"
NEGATIVE = "NO_RELATION"
RARE = ("diagnosed_by", "has_dosage", "treated_by")
REVIEW_CAP = 200


def kappa(a, b):
    if not a:
        return None
    if len(set(a) | set(b)) < 2:
        return 1.0
    return round(float(cohen_kappa_score(a, b)), 3)


def main():
    inputs, A, B = {}, {}, {}
    for f in sorted(AI.glob("seed_b*_input.jsonl")):
        stem = f.name.replace("_input.jsonl", "")
        for r in load(f):
            inputs[r["id"]] = r
        for r in load(AI / f"{stem}_passA.jsonl"):
            A[r["id"]] = r
        for r in load(AI / f"{stem}_passB.jsonl"):
            B[r["id"]] = r
    dev_ids = {r["id"] for r in load(DATA / "dev_unlabeled.jsonl")}
    ea, eb, pa, pb = [], [], [], []
    by_rel = {}
    merged, ent_dis, pair_dis, rare_pos = [], [], [], []
    for sid, it in inputs.items():
        a, b = A[sid], B[sid]
        ents = {}
        for e in it["entities"]:
            x, y = a["entities"][e["id"]], b["entities"][e["id"]]
            ea.append(x); eb.append(y)
            ents[e["id"]] = x if x == y else None
            if x != y:
                ent_dis.append((it, e, x, y))
        rels = []
        for p in it["pairs"]:
            x, y = a["pairs"].get(p["pair_id"]), b["pairs"].get(p["pair_id"])
            if x is not None and y is not None:
                pa.append(x != NEGATIVE); pb.append(y != NEGATIVE)
                by_rel.setdefault(p["relation"], ([], []))
                by_rel[p["relation"]][0].append(x != NEGATIVE); by_rel[p["relation"]][1].append(y != NEGATIVE)
            both_valid = ents.get(p["head"]) == "VALID" and ents.get(p["tail"]) == "VALID"
            unresolved = ents.get(p["head"]) is None or ents.get(p["tail"]) is None
            if both_valid and x == y:
                rels.append({**p, "label": x, "source": "ai_agreed"})
                if x != NEGATIVE and p["relation"] in RARE:
                    rare_pos.append((it, p, x, y))
            elif both_valid or (unresolved and (x is not None or y is not None)):
                rels.append({**p, "label": None, "source": "needs_review", "passA": x, "passB": y})
                pair_dis.append((it, p, x, y))
        merged.append({"id": sid, "split": "dev" if sid in dev_ids else "seed", "text": it["text"],
                       "entities": [{**e, "validity": ents[e["id"]], "passA": a["entities"][e["id"]],
                                     "passB": b["entities"][e["id"]]} for e in it["entities"]],
                       "relations": rels})
    pos_a = Counter(p["relation"] for it in inputs.values() for p in it["pairs"]
                    if A[it["id"]]["pairs"].get(p["pair_id"]) not in (None, NEGATIVE))
    agreed_pos = Counter(r["allowed_relation"] if "allowed_relation" in r else r["relation"]
                         for m in merged for r in m["relations"] if r["label"] not in (None, NEGATIVE))
    report = {
        "sentences": len(inputs), "mentions": len(ea), "pairs": sum(len(i["pairs"]) for i in inputs.values()),
        "entity_kappa": kappa(ea, eb), "entity_agreement": round(sum(x == y for x, y in zip(ea, eb)) / len(ea), 3),
        "entity_valid_share_passA": round(ea.count("VALID") / len(ea), 3),
        "pairs_both_valid_in_both_passes": len(pa),
        "pair_kappa": kappa(pa, pb), "pair_agreement": round(sum(x == y for x, y in zip(pa, pb)) / len(pa), 3) if pa else None,
        "pair_kappa_by_relation": {r: {"n": len(v[0]), "kappa": kappa(*v), "pos_A": sum(v[0]), "pos_B": sum(v[1])}
                                   for r, v in sorted(by_rel.items())},
        "positives_passA": dict(pos_a), "positives_agreed": dict(agreed_pos),
        "entity_disagreements": len(ent_dis), "pair_disagreements": len(pair_dis),
        "rare_agreed_positives_for_check": len(rare_pos),
    }
    with open(DATA / "seed_ai_merged.jsonl", "w", encoding="utf-8") as f:
        for m in merged:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    (DATA / "ai_agreement_seed.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    wb = Workbook()
    ws = wb.active; ws.title = "README"
    for line in ["Phiếu duyệt các chỗ hai lượt AI bất đồng (và kiểm tra cặp dương của lớp hiếm). Hướng dẫn: relation/guideline.md.",
                 "Sheet entities: cột label chọn VALID/INVALID. Sheet pairs: cột label chọn tên quan hệ hoặc NO_RELATION;",
                 "nếu một thực thể của cặp là INVALID (theo nhãn bạn chọn hoặc nhãn đã đồng thuận) thì để trống.",
                 "Cột passA/passB là nhãn của hai lượt AI, chỉ để tham khảo. Cột note để ghi chú."]:
        ws.append([line])
    ws.column_dimensions["A"].width = 120
    we = wb.create_sheet("entities")
    we.append(["sentence_id", "entity_id", "type", "mention", "sentence", "passA", "passB", "label", "note"])
    for it, e, x, y in ent_dis:
        we.append([it["id"], e["id"], e["label"], e["text"], it["marked_text"], x, y, "", ""])
    wp = wb.create_sheet("pairs")
    wp.append(["sentence_id", "pair_id", "relation", "head", "tail", "sentence", "why", "passA", "passB", "label", "note"])
    rng = random.Random(1)
    rng.shuffle(rare_pos)
    rows = [(it, p, x, y, "disagree") for it, p, x, y in pair_dis] + \
           [(it, p, x, y, "rare_positive_check") for it, p, x, y in rare_pos]
    for it, p, x, y, why in rows[:max(REVIEW_CAP, len(pair_dis))]:
        ent = {e["id"]: e for e in it["entities"]}
        wp.append([it["id"], p["pair_id"], p["relation"], f'{ent[p["head"]]["text"]} ({p["head"]})',
                   f'{ent[p["tail"]]["text"]} ({p["tail"]})', it["marked_text"], why,
                   x if x is not None else "-", y if y is not None else "-", "", ""])
    for sheet, col, opts in ((we, "H", "VALID,INVALID"),
                             (wp, "J", ",".join(sorted({p["relation"] for i in inputs.values() for p in i["pairs"]} | {NEGATIVE})))):
        dv = DataValidation(type="list", formula1=f'"{opts}"', allow_blank=True)
        sheet.add_data_validation(dv); dv.add(f"{col}2:{col}{max(sheet.max_row, 2)}")
        for c in sheet[1]:
            c.font = Font(bold=True)
        for r in sheet.iter_rows(min_row=2):
            for c in r:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        sheet.freeze_panes = "A2"
    we.column_dimensions["E"].width = 90; wp.column_dimensions["F"].width = 90
    if not (DATA / "seed_review.xlsx").exists():  # không ghi đè phiếu duyệt của relation.review_seed
        wb.save(DATA / "seed_review.xlsx")
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
