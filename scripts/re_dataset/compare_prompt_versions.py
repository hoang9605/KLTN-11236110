r"""So sánh các phiên bản prompt gán nhãn LLM với nhãn chuyên gia của pilot (không gọi API).

Nhãn vàng lấy từ phiếu chuyên gia pilot_label_v1: chấm 1 → giữ nhãn AI v1; chấm 0 → đảo
(dương → NO_RELATION, NO_RELATION → quan hệ cho phép). Ngoại lệ: cặp có ghi chú chuyên gia rằng
thực thể sai kiểu (vd "cc kh phải pp": cấp cứu không phải phương pháp) → vàng = NO_RELATION.
Cặp mà phiên bản mới bỏ vì thực thể INVALID được tính là dự đoán NO_RELATION.

  .venv\Scripts\python.exe -X utf8 scripts\re_dataset\compare_prompt_versions.py pilot_label_v2
  .venv\Scripts\python.exe -X utf8 scripts\re_dataset\compare_prompt_versions.py re_v3\data\silver\dev_label_v3\dev_label_v3_expert_review.xlsx dev_label_v4
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
SILVER = ROOT / "re_v3" / "data" / "silver"
NEG = "NO_RELATION"
INVALID_NOTE_STT = {19, 20, 21}   # chỉ áp dụng cho phiếu pilot_label_v1   # «cấp cứu» không phải PROCEDURE (ghi chú chuyên gia dòng 19)


def gold_rows(xlsx):
    pilot = "pilot_label_v1" in str(xlsx)
    ws = load_workbook(xlsx)["Quan hệ"]
    hdr = [c.value for c in ws[1]]
    out = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(hdr, r))
        if d["STT"] is None:
            continue
        ok = str(d[hdr[8]]).strip() != "0"
        ai = d["ai_label"]
        gold = ai if ok else (NEG if ai != NEG else d["relation"])
        if pilot and d["STT"] in INVALID_NOTE_STT:
            gold = NEG
        out.append({"stt": d["STT"], "key": (d["record_id"], d["head_id"], d["tail_id"]), "rel": d["relation"],
                    "gold": gold, "v1": ai, "statement": d["Quan hệ AI đưa ra"]})
    return out


def preds(name):
    p = {}
    for line in (SILVER / name / f"{name}.jsonl").read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        for x in rec["relations"]:
            p[(rec["id"], x["head"], x["tail"])] = x["label"]
    return p


def metrics(rows, get):
    tp = fp = fn = c = 0
    per = defaultdict(Counter)
    for r in rows:
        y, g = get(r), r["gold"]
        c += y == g
        per[r["rel"]]["n"] += 1
        per[r["rel"]]["correct"] += y == g
        if y != NEG and y == g:
            tp += 1
        if y != NEG and y != g:
            fp += 1
        if g != NEG and y != g:
            fn += 1
    p = tp / max(1, tp + fp)
    rc = tp / max(1, tp + fn)
    return {"n": len(rows), "acc": round(c / len(rows), 3), "precision": round(p, 3), "recall": round(rc, 3),
            "f1": round(2 * p * rc / max(1e-9, p + rc), 3), "gold_pos": sum(r["gold"] != NEG for r in rows),
            "per_relation_acc": {k: f'{v["correct"]}/{v["n"]}' for k, v in sorted(per.items())}}


def main():
    args = sys.argv[1:]
    gold = SILVER / "pilot_label_v1" / "pilot_label_v1_expert_review.xlsx"
    if args and args[0].endswith(".xlsx"):
        gold = Path(args.pop(0))
    names = args or ["pilot_label_v2"]
    rows = gold_rows(gold)
    res = {"ai_in_sheet": metrics(rows, lambda r: r["v1"])}
    diffs = {}
    for n in names:
        p = preds(n)
        res[n] = metrics(rows, lambda r: p.get(r["key"], NEG))
        res[n]["dropped_invalid"] = sum(r["key"] not in p for r in rows)
        diffs[n] = [f'{r["stt"]} | gold={r["gold"]} v1={r["v1"]} {n}={p.get(r["key"], "INVALID→NO")} | {r["statement"]}'
                    for r in rows if p.get(r["key"], NEG) != r["v1"]]
    out = SILVER / names[-1] / "so_sanh_voi_chuyen_gia.json"
    out.write_text(json.dumps({"metrics": res, "changed_vs_v1": diffs}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    print("Chi tiết:", out)


if __name__ == "__main__":
    main()
