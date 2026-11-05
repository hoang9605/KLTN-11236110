"""Đọc phiếu đã duyệt -> gold.jsonl (+ đoạn cần lượt 2, + kappa nếu có phiếu thứ hai).

  python scripts/golden_test/import_workbook.py --workbook data/golden_test/v1/phieu_duyet_A_da_duyet.xlsx --annotator A
  python scripts/golden_test/import_workbook.py --workbook ...A.xlsx --annotator A --second ...B_double.xlsx --second-annotator B

Quy tắc: chỉ đoạn có DA_DUYET_XONG=CO, mọi thực thể có KET_LUAN và mọi cặp có NHAN mới vào gold.
Sửa NER làm xuất hiện cặp ứng viên mới -> đoạn chuyển sang pending_round2 (không tự đoán nhãn).
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import load_workbook

from common import (ENTITY_TYPES, NEGATIVE, RELATIONS, UNKNOWN, ROOT, candidate_pairs, read_jsonl,
                    sha256, write_jsonl)


def sheet_rows(wb, name):
    ws = wb[name]
    head = [c.value for c in ws[1]]
    for row in ws.iter_rows(min_row=2, values_only=True):
        if any(v not in (None, "") for v in row):
            yield {h: (v.strip() if isinstance(v, str) else v) for h, v in zip(head, row)}


def read_review(path):
    wb = load_workbook(path, data_only=True)
    rv = {"done": {}, "ent": defaultdict(dict), "add": defaultdict(list), "rel": defaultdict(dict), "notes": defaultdict(list)}
    for r in sheet_rows(wb, "DOAN"):
        rv["done"][r["ma_doan"]] = (r.get("DA_DUYET_XONG") or "").upper() == "CO"
        if r.get("GHI_CHU"): rv["notes"][r["ma_doan"]].append(r["GHI_CHU"])
    for r in sheet_rows(wb, "THUC_THE"):
        rv["ent"][r["ma_doan"]][r["ma_tt"]] = r
    for r in sheet_rows(wb, "THEM_THUC_THE"):
        if r.get("ma_doan") and r.get("CUM_TU"):
            rv["add"][r["ma_doan"]].append(r)
    for r in sheet_rows(wb, "QUAN_HE"):
        rv["rel"][r["ma_doan"]][r["ma_cap"]] = r
    return rv


def find_occurrence(text, phrase, near=None, nth=None):
    hits, i = [], text.find(phrase)
    while i != -1:
        hits.append(i); i = text.find(phrase, i + 1)
    if not hits:
        return None
    if nth:
        return hits[int(nth) - 1] if int(nth) <= len(hits) else None
    return min(hits, key=lambda h: abs(h - near)) if near is not None else hits[0]


def apply_review(row, rv, issues):
    sid, text = row["id"], row["text"]
    if not rv["done"].get(sid):
        issues[sid].append("chưa đánh dấu DA_DUYET_XONG=CO"); return None
    ents, changed = [], False
    for e in row["entities"]:
        r = rv["ent"][sid].get(e["id"])
        verdict = (r or {}).get("KET_LUAN")
        if verdict not in ("DUNG", "SAI_NHAN", "SAI_RANH_GIOI", "XOA"):
            issues[sid].append(f"{e['id']}: thiếu KET_LUAN"); return None
        e = {k: e[k] for k in ("id", "text", "label", "start", "end")}
        if verdict == "XOA":
            changed = True; continue
        if verdict == "SAI_NHAN" or r.get("NHAN_DUNG"):
            if r.get("NHAN_DUNG") not in ENTITY_TYPES:
                issues[sid].append(f"{e['id']}: NHAN_DUNG không hợp lệ"); return None
            changed |= r["NHAN_DUNG"] != e["label"]; e["label"] = r["NHAN_DUNG"]
        if verdict == "SAI_RANH_GIOI":
            phrase = r.get("CUM_TU_DUNG")
            pos = find_occurrence(text, phrase, near=e["start"]) if phrase else None
            if pos is None:
                issues[sid].append(f"{e['id']}: CUM_TU_DUNG không có trong câu"); return None
            e.update(start=pos, end=pos + len(phrase), text=phrase); changed = True
        ents.append(e)
    for n, add in enumerate(rv["add"][sid], 1):
        pos = find_occurrence(text, add["CUM_TU"], nth=add.get("LAN_XUAT_HIEN"))
        if pos is None or add.get("NHAN") not in ENTITY_TYPES:
            issues[sid].append(f"thực thể bổ sung '{add['CUM_TU']}' không tìm thấy/sai nhãn"); return None
        ents.append({"id": f"A{n}", "text": add["CUM_TU"], "label": add["NHAN"], "start": pos, "end": pos + len(add["CUM_TU"])})
        changed = True
    ents.sort(key=lambda e: e["start"])
    if any(a["end"] > b["start"] for a, b in zip(ents, ents[1:])):
        issues[sid].append("thực thể chồng lấn sau khi sửa"); return None
    # Relation labels from reviewer for original pairs (by entity ids)
    labels = {(p["head"], p["tail"]): p["label"] for p in row.get("prior_relations", [])}
    for p in row["relations"]:
        r = rv["rel"][sid].get(p["id"])
        lab = (r or {}).get("NHAN")
        if lab not in (p["allowed_relation"], NEGATIVE, UNKNOWN):
            issues[sid].append(f"{p['id']}: thiếu/sai NHAN"); return None
        labels[(p["head"], p["tail"])] = lab
    rels, pending = [], []
    for p in candidate_pairs(ents):
        key = (p["head"], p["tail"])
        if key in labels:
            rels.append({"head": p["head"], "tail": p["tail"], "allowed_relation": p["allowed_relation"], "label": labels[key]})
        else:
            pending.append(p)
    out = {**{k: row[k] for k in ("id", "source", "source_split", "source_row_index", "selection_reason", "text")},
           "entities": ents, "relations": rels, "ner_changed": changed, "notes": rv["notes"].get(sid, [])}
    return out, pending


def kappa(a, b):
    n = len(a)
    if not n: return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / (n * n)
    return round((po - pe) / (1 - pe), 4) if pe < 1 else 1.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", default=str(ROOT / "data/golden_test/v1/candidates.jsonl"))
    ap.add_argument("--workbook", required=True); ap.add_argument("--annotator", required=True)
    ap.add_argument("--second"); ap.add_argument("--second-annotator", default="B")
    a = ap.parse_args()
    base = Path(a.candidates).parent
    cands = read_jsonl(a.candidates)
    rv = read_review(a.workbook)
    issues, gold, round2 = defaultdict(list), [], []
    for row in cands:
        res = apply_review(row, rv, issues)
        if res is None: continue
        g, pending = res
        if pending:
            round2.append({**g, "pending_pairs": pending}); continue
        gold.append({**g, "status": "gold", "human_verified": True, "annotators": [a.annotator]})
    tag = "" if Path(a.candidates).stem == "candidates" else "_" + Path(a.candidates).stem
    write_jsonl(base / f"gold{tag}.jsonl", gold)
    r2 = []
    for g in round2:
        pend = [{**p, "id": f"N{n}", "label": None} for n, p in enumerate(g["pending_pairs"], 1)]
        r2.append({**{k: v for k, v in g.items() if k != "pending_pairs"}, "prior_relations": g["relations"], "relations": pend})
    write_jsonl(base / f"round2_candidates{tag}.jsonl", r2)
    # Mức đồng thuận giữa nhãn AI tiền gán và người duyệt (nếu phiếu có cột *_AI)
    ai_cmp = {"entity": [0, 0], "relation": [0, 0]}
    for ents in rv["ent"].values():
        for r in ents.values():
            if r.get("KET_LUAN_AI") and r.get("KET_LUAN"):
                ai_cmp["entity"][0] += 1; ai_cmp["entity"][1] += r["KET_LUAN_AI"] != r["KET_LUAN"]
    for rels in rv["rel"].values():
        for r in rels.values():
            if r.get("NHAN_AI") and r.get("NHAN"):
                ai_cmp["relation"][0] += 1; ai_cmp["relation"][1] += r["NHAN_AI"] != r["NHAN"]
    ai_prefill = any(n for n, _ in ai_cmp.values())
    if ai_prefill:
        for g in gold:
            g["label_source"] = "ai_prefill_human_reviewed"
            g["annotators"] = ["claude-ai (tiền gán)"] + g["annotators"]
        write_jsonl(base / f"gold{tag}.jsonl", gold)
    report = {"workbook": str(a.workbook), "workbook_sha256": sha256(a.workbook), "annotator": a.annotator,
              "candidates": len(cands), "gold": len(gold), "round2": len(round2),
              "incomplete": len(issues), "issues": dict(issues),
              "ai_prefill_changed_by_reviewer": {k: {"reviewed": n, "changed": c, "changed_pct": round(100 * c / n, 1) if n else None}
                                                 for k, (n, c) in ai_cmp.items()} if ai_prefill else None,
              "gold_entities": dict(Counter(e["label"] for r in gold for e in r["entities"])),
              "gold_relations": dict(Counter(x["label"] for r in gold for x in r["relations"]))}
    if a.second:
        rv2 = read_review(a.second)
        ea, eb, ra, rb = [], [], [], []
        for sid, ents in rv2["ent"].items():
            for eid, r2 in ents.items():
                r1 = rv["ent"].get(sid, {}).get(eid)
                if r1 and r1.get("KET_LUAN") and r2.get("KET_LUAN"):
                    ea.append(r1["KET_LUAN"]); eb.append(r2["KET_LUAN"])
        for sid, rels in rv2["rel"].items():
            for pid, r2 in rels.items():
                r1 = rv["rel"].get(sid, {}).get(pid)
                if r1 and r1.get("NHAN") and r2.get("NHAN"):
                    ra.append(r1["NHAN"]); rb.append(r2["NHAN"])
        report["agreement"] = {"second_annotator": a.second_annotator,
                               "entity_verdict": {"n": len(ea), "observed": round(sum(x == y for x, y in zip(ea, eb)) / max(len(ea), 1), 4), "cohen_kappa": kappa(ea, eb)},
                               "relation_label": {"n": len(ra), "observed": round(sum(x == y for x, y in zip(ra, rb)) / max(len(ra), 1), 4), "cohen_kappa": kappa(ra, rb)}}
    (base / f"import_report{tag}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "issues"}, ensure_ascii=False, indent=2))
    if round2:
        print(f"{len(round2)} đoạn có cặp mới sau khi sửa NER -> chạy make_workbook.py --candidates "
              f"{base / f'round2_candidates{tag}.jsonl'} để duyệt lượt 2")


if __name__ == "__main__":
    main()
