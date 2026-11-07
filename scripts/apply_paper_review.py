"""Áp kết quả duyệt trên giấy vào bộ RE 600 mẫu, tạo gold v1.

Đầu vào:
  - annotations_reviewed_600.jsonl  (bản AI rà soát lần hai, 15/10/2026; không bị sửa)
  - de_xuat_sua_RE_2026-11-05.csv   (40 đề xuất; người duyệt đồng ý toàn bộ)
  - các quy ước người duyệt chốt (CONVENTIONS bên dưới)

Đầu ra trong --out:
  - annotations_gold_v1.jsonl   600 mẫu, human_verified=true, kèm lịch sử thay đổi từng mẫu
  - decisions_applied.csv       đề xuất + quyết định cuối thực tế đã áp
  - manifest.json               nguồn, SHA-256, quy ước, người duyệt, thống kê trước/sau

  python -X utf8 scripts/apply_paper_review.py --reviewer "..." --reviewed-at YYYY-MM-DD
"""
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "outputs/vietmed_600_RE_review/review_2026_10_15"

# Quy ước người duyệt chốt ngày 05/11/2026.
CONVENTIONS = {
    "generic_entities": "XÓA thực thể chung chung PROCEDURE/DRUG/TEST (danh sách GENERIC) cùng mọi cặp liên quan",
    "question": "Câu hỏi được tính như khẳng định (VM600-464 → located_at)",
    "negation": "Phủ định 'không cải thiện với thuốc' → NO_RELATION",
    "out_of_scope": "Thực phẩm chức năng/đông y và lỗi phiên âm (376, 586, 375 R3) → XÓA cặp",
    "generic_condition": "CONDITION chung chung ('bệnh', 'biến chứng'...) chưa được hỏi riêng → giữ nguyên",
}
sys.path.insert(0, str(ROOT))
from relation_extraction.data import GENERIC_ENTITIES as GENERIC  # noqa: E402  (một nguồn với MedicalREPipeline)
# Quyết định cho các dòng "CẦN QUY ƯỚC" (dòng nhóm 1 được xử lý qua GENERIC).
CONVENTION_DECISIONS = {
    ("VM600-464", "R1"): "located_at",
    ("VM600-557", "R1"): "NO_RELATION",
    ("VM600-557", "R2"): "NO_RELATION",
    ("VM600-586", "R1"): "DELETE",
    ("VM600-376", "R1"): "DELETE",
    ("VM600-376", "R2"): "DELETE",
    ("VM600-375", "R3"): "DELETE",
}
VALID = {"located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage",
         "NO_RELATION", "CHUA_RO", "DELETE"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel_stats(rows):
    return dict(Counter(r["label"] for d in rows for r in d["relations"]))


def ent_stats(rows):
    return dict(Counter(e["label"] for d in rows for e in d["entities"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=str(REVIEW_DIR / "annotations_reviewed_600.jsonl"))
    ap.add_argument("--decisions", default=str(REVIEW_DIR / "de_xuat_sua_RE_2026-11-05.csv"))
    ap.add_argument("--out", default=str(ROOT / "data/re_gold_v1"))
    ap.add_argument("--reviewer", required=True)
    ap.add_argument("--reviewed-at", required=True)
    a = ap.parse_args()

    rows = [json.loads(l) for l in Path(a.source).read_text(encoding="utf-8").splitlines() if l.strip()]
    by_id = {d["id"]: d for d in rows}
    before = {"relations": rel_stats(rows), "entities": ent_stats(rows)}
    history = {d["id"]: [] for d in rows}

    # 1. Áp quyết định từng cặp.
    applied = []
    with open(a.decisions, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        decisions = list(reader)
    for row in decisions:
        key = (row["sample_id"], row["relation_id"])
        final = row["de_xuat"]
        if final == "CẦN QUY ƯỚC":
            final = CONVENTION_DECISIONS.get(key, "GENERIC_RULE" if row["nhom"].startswith("1.") else None)
        if final is None:
            raise ValueError(f"{key}: chưa có quyết định")
        row["quyet_dinh_bac_si"] = final
        applied.append(row)
        if final == "GENERIC_RULE":
            continue  # xử lý ở bước 2
        if final not in VALID:
            raise ValueError(f"{key}: nhãn lạ {final}")
        d = by_id[key[0]]
        rel = next(r for r in d["relations"] if r["id"] == key[1])
        if rel["label"] != row["nhan_hien_tai"]:
            raise ValueError(f"{key}: nhãn hiện tại không khớp CSV")
        if final == "DELETE":
            d["relations"].remove(rel)
            history[d["id"]].append({"op": "delete_relation", "relation": rel["id"], "before": rel["label"],
                                     "reason": "quy ước ngoài phạm vi"})
        elif final != rel["label"]:
            history[d["id"]].append({"op": "relabel", "relation": rel["id"], "before": rel["label"], "after": final})
            rel["label"] = final

    # 2. Xóa thực thể chung chung và các cặp liên quan; cập nhật BIO.
    removed_entities = Counter()
    for d in rows:
        drop = [e for e in d["entities"] if e["text"].lower() in GENERIC.get(e["label"], ())]
        if not drop:
            continue
        ids = {e["id"] for e in drop}
        for e in drop:
            removed_entities[(e["label"], e["text"].lower())] += 1
            for i in range(e["token_start"], e["token_end"]):
                d["labels"][i] = "O"
            history[d["id"]].append({"op": "delete_entity", "entity": e["id"], "text": e["text"],
                                     "label": e["label"], "reason": "thực thể chung chung"})
        for r in [r for r in d["relations"] if r["head"] in ids or r["tail"] in ids]:
            d["relations"].remove(r)
            history[d["id"]].append({"op": "delete_relation", "relation": r["id"], "before": r["label"],
                                     "reason": "đầu mút là thực thể chung chung"})
        d["entities"] = [e for e in d["entities"] if e["id"] not in ids]

    # 3. Kiểm tra và gắn trạng thái người duyệt.
    for d in rows:
        text = d["text"]
        for e in d["entities"]:
            assert text[e["start"]:e["end"]] == e["text"], (d["id"], e["id"])
            assert d["labels"][e["token_start"]].startswith("B-"), (d["id"], e["id"])
        ent_ids = {e["id"] for e in d["entities"]}
        assert all(r["head"] in ent_ids and r["tail"] in ent_ids for r in d["relations"]), d["id"]
        assert all(r["label"] in VALID - {"DELETE"} for r in d["relations"]), d["id"]
        d["ai_review_flags"] = d.pop("review_flags", [])
        d["review_flags"] = []
        d["annotation_status"] = "HUMAN_PAPER_REVIEWED"
        d["reviewer"] = a.reviewer
        d["reviewed_at"] = a.reviewed_at
        d["review_note"] = "Duyệt trên giấy: đồng ý bản AI rà soát và 40 đề xuất ngày 05/11/2026"
        d["human_verified"] = True
        d["training_eligible"] = True
        d["gold_v1_changes"] = history[d["id"]]

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    gold = out / "annotations_gold_v1.jsonl"
    gold.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in rows), encoding="utf-8")
    with open(out / "decisions_applied.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(applied)
    after = {"relations": rel_stats(rows), "entities": ent_stats(rows)}
    manifest = {
        "source": str(Path(a.source).relative_to(ROOT)), "source_sha256": sha(a.source),
        "decisions": str(Path(a.decisions).relative_to(ROOT)), "decisions_sha256": sha(a.decisions),
        "output_sha256": sha(gold), "reviewer": a.reviewer, "reviewed_at": a.reviewed_at,
        "review_mode": "paper; reviewer agreed with all AI labels and all 40 suggestions",
        "conventions": CONVENTIONS, "generic_entities": {k: sorted(v) for k, v in GENERIC.items()},
        "removed_generic_entities": {f"{k[0]}:{k[1]}": v for k, v in sorted(removed_entities.items())},
        "before": before, "after": after,
        "samples_changed": sum(bool(h) for h in history.values()),
        "limitations": ["Source is VietMed-NER train split; not an independent test set for NER",
                        "Single reviewer, no inter-annotator agreement measured",
                        "CHUA_RO pairs remain and are excluded from training/evaluation"],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"before": before, "after": after, "samples_changed": manifest["samples_changed"],
                      "removed_generic_entities": manifest["removed_generic_entities"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
