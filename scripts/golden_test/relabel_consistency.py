r"""Golden test v1.1: align the AI pre-labels with the conventions used for gold v1 and RE v2.

The golden test AI labels (ai_labels.jsonl) were written in an earlier session than RE v2
and departed from the reviewer's conventions (data/re_gold_v1/manifest.json) in a few
places. This pass re-reads every scored pair against those conventions only (text +
guideline; model predictions were NOT consulted per pair) and records each change.
The original file is kept unchanged; evaluation reports both versions.

Label "XOA" = pair removed from evaluation (generic entity or out-of-scope product),
the same treatment gold v1 gives such pairs.

    .venv\Scripts\python.exe -X utf8 scripts/golden_test/relabel_consistency.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GT = ROOT / "data/golden_test/v1"

CONTAINED = "CONDITION đã chứa bộ phận (cụm đầy đủ) → không tạo located_at với lần nhắc bộ phận"
CHANGES = [
    ("GT-009", "R1", "CHUA_RO", "Câu bị cắt; không nói đặt mỏ vịt để chẩn đoán chảy máu"),
    ("GT-012", "R1", "NO_RELATION", CONTAINED + " (“u xơ tử cung” → “tử cung”)"),
    ("GT-026", "R1", "NO_RELATION", "“hai mươi mốt viên” là số viên trong vỉ, không phải liều dùng"),
    ("GT-026", "R2", "NO_RELATION", "“hai mươi mốt viên” là số viên trong vỉ, không phải liều dùng"),
    ("GT-027", "R1", "XOA", "“thuốc bổ”: thực phẩm chức năng → ngoài phạm vi (xóa cặp); “bảy viên” là thành phần vỉ"),
    ("GT-027", "R2", "XOA", "“thuốc bổ”: thực phẩm chức năng → ngoài phạm vi (xóa cặp)"),
    ("GT-050", "R1", "XOA", "“thuốc” là DRUG chung chung (GENERIC_ENTITIES) → xóa cặp"),
    ("GT-055", "R1", "XOA", "“thuốc” là DRUG chung chung → xóa cặp"),
    ("GT-056", "R1", "XOA", "“thuốc” là DRUG chung chung → xóa cặp"),
    ("GT-057", "R1", "XOA", "“thuốc” là DRUG chung chung → xóa cặp"),
    ("GT-061", "R2", "NO_RELATION", CONTAINED + " (“viêm đại tràng” → “đại tràng”)"),
    ("GT-065", "R4", "NO_RELATION", "Phủ định “không có tổn thương ở niêm mạc của đại tràng” → NO_RELATION"),
    ("GT-069", "R1", "XOA", "“bạch thược”: đông y → ngoài phạm vi (xóa cặp)"),
    ("GT-124", "R1", "NO_RELATION", "“cao” chỉ mức độ bổ sung, không phải liều"),
    ("GT-133", "R1", "treated_by", "Câu hỏi được tính như khẳng định: “có nên dùng thuốc giảm đau hạ sốt” cho sốt"),
    ("GT-133", "R3", "treated_by", "Câu hỏi được tính như khẳng định: “có nên dùng thuốc giảm đau hạ sốt” cho đau"),
    ("GT-137", "R3", "NO_RELATION", CONTAINED + " (“ung thư dạ dày” → “dạ dày”)"),
]


def main():
    rows = [json.loads(l) for l in (GT / "ai_labels.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    by_id = {r["id"]: r for r in rows}
    log = []
    for sid, rid, new, why in CHANGES:
        rel = by_id[sid]["relations"][rid]
        log.append({"id": sid, "relation": rid, "before": rel.get("label"), "after": new, "reason": why})
        rel["label"] = new
        rel["reason"] = why
        rel["revised"] = "v1.1 consistency pass 2026-11-08"
    with open(GT / "ai_labels_v1_1.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(GT / "ai_labels_v1_1_changes.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "relation", "before", "after", "reason"])
        w.writeheader()
        w.writerows(log)
    print(f"{len(log)} changes -> {GT / 'ai_labels_v1_1.jsonl'}")


if __name__ == "__main__":
    main()
