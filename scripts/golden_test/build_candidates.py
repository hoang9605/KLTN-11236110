"""Chọn ~150 đoạn từ split TEST VietMed-NER làm ứng viên golden test end-to-end NER -> RE.

- Nguồn: split test chính thức (checkpoint NER chưa thấy). Loại đoạn trùng nội dung với train.
- Lấy mẫu có chủ đích: mỗi loại quan hệ có >= --min-per-relation đoạn chứa cặp đúng kiểu,
  ưu tiên loại hiếm (has_dosage, diagnosed_by...). Thêm đoạn không có cặp và không có thực thể
  để đo dự đoán dương sai end-to-end.
- NER lấy từ nhãn gốc của dataset (ánh xạ 6 loại theo ner/config.py). Nhãn RE để TRỐNG:
  không điền sẵn bằng AI để tránh thiên lệch người duyệt.

Chạy (Windows, từ thư mục gốc repo):
  .venv\\Scripts\\python.exe -X utf8 scripts/golden_test/build_candidates.py
"""
import argparse
import json
import random
from collections import Counter
from pathlib import Path

from common import (RELATIONS, candidate_pairs, entities_from_bio, load_split, sha256, text_group,
                    write_jsonl, ROOT)

RARITY_ORDER = ["has_dosage", "diagnosed_by", "treated_by", "treated_by_procedure", "located_at"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "data" / "golden_test" / "v1"))
    ap.add_argument("--n", type=int, default=150)
    ap.add_argument("--min-per-relation", type=int, default=25)
    ap.add_argument("--no-pair", type=int, default=15, help="đoạn có thực thể nhưng không có cặp ứng viên")
    ap.add_argument("--no-entity", type=int, default=10, help="đoạn không có thực thể mục tiêu")
    ap.add_argument("--max-pairs", type=int, default=10, help="bỏ đoạn có quá nhiều cặp (tải duyệt)")
    ap.add_argument("--double", type=int, default=30, help="số đoạn cho người duyệt thứ hai (tính kappa)")
    ap.add_argument("--seed", type=int, default=20261101)
    ap.add_argument("--test-arrow"); ap.add_argument("--train-arrow")
    a = ap.parse_args()
    rng = random.Random(a.seed)

    test, test_src = load_split("test", a.test_arrow)
    train, train_src = load_split("train", a.train_arrow)
    train_groups = {text_group(" ".join(r["words"])) for r in train}

    pool, audit, seen = [], Counter(), set()
    for idx, row in enumerate(test):
        if len(row["words"]) != len(row["labels"]):
            audit["skip_bad_alignment"] += 1; continue
        text, ents = entities_from_bio(row["words"], row["labels"])
        g = text_group(text)
        if not text.strip():
            audit["skip_empty"] += 1; continue
        if g in train_groups:
            audit["skip_duplicate_of_train"] += 1; continue
        if g in seen:
            audit["skip_duplicate_within_test"] += 1; continue
        seen.add(g)
        pairs = candidate_pairs(ents)
        if len(pairs) > a.max_pairs:
            audit["skip_too_many_pairs"] += 1; continue
        pool.append({"source_row_index": idx, "text": text, "entities": ents, "pairs": pairs,
                     "pair_types": sorted({p["allowed_relation"] for p in pairs}),
                     "source_labels": list(row["labels"])})
    audit["eligible_test_rows"] = len(pool)
    rng.shuffle(pool)

    with_pairs = [r for r in pool if r["pairs"]]
    no_pair = [r for r in pool if r["entities"] and not r["pairs"]]
    no_ent = [r for r in pool if not r["entities"]]
    chosen, taken = [], set()
    def take(r, reason):
        chosen.append({**r, "selection_reason": reason}); taken.add(r["source_row_index"])
    n_pair_rows = a.n - a.no_pair - a.no_entity
    cover = Counter()
    for rel in RARITY_ORDER:
        for r in with_pairs:
            if cover[rel] >= a.min_per_relation or len(chosen) >= n_pair_rows:
                break
            if rel in r["pair_types"] and r["source_row_index"] not in taken:
                take(r, f"quota:{rel}")
                cover.update(r["pair_types"])
    for r in with_pairs:
        if len(chosen) >= n_pair_rows:
            break
        if r["source_row_index"] not in taken:
            take(r, "random_fill"); cover.update(r["pair_types"])
    for r in no_pair[:a.no_pair]:
        take(r, "no_candidate_pair")
    for r in no_ent[:a.no_entity]:
        take(r, "no_target_entity")
    chosen.sort(key=lambda r: r["source_row_index"])

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rows = []
    for n, r in enumerate(chosen, 1):
        rows.append({"id": f"GT-{n:03}", "source": "leduckhai/VietMed-NER", "source_split": "test",
                     "source_row_index": r["source_row_index"], "selection_reason": r["selection_reason"],
                     "text": r["text"], "entities": r["entities"], "source_labels": r["source_labels"],
                     "relations": [{**p, "label": None} for p in r["pairs"]],
                     "status": "candidate", "human_verified": False, "annotators": []})
    ids = [r["id"] for r in rows]
    double = sorted(rng.sample(ids, min(a.double, len(ids))))
    write_jsonl(out / "candidates.jsonl", rows)

    pair_counts = Counter(p["allowed_relation"] for r in rows for p in r["relations"])
    passages_per_rel = Counter(t for r in chosen for t in r["pair_types"])
    shortfall = {rel: passages_per_rel[rel] for rel in RELATIONS if passages_per_rel[rel] < a.min_per_relation}
    manifest = {
        "version": "v1", "purpose": "end-to-end NER -> RE golden test (candidate, chưa duyệt)",
        "seed": a.seed, "params": vars(a), "test_source": test_src, "train_source": train_src,
        "audit": dict(audit), "samples": len(rows),
        "selection": dict(Counter(r["selection_reason"].split(":")[0] for r in rows)),
        "passages_with_pair_type": dict(passages_per_rel), "candidate_pairs": dict(pair_counts),
        "entities": dict(Counter(e["label"] for r in rows for e in r["entities"])),
        "quota_shortfall": shortfall, "double_annotation_ids": double,
        "notes": [
            "Đoạn chứa cặp đúng kiểu KHÔNG đồng nghĩa có quan hệ dương; số dương thật chỉ biết sau khi duyệt.",
            "NER là nhãn gốc VietMed ánh xạ 6 loại, người duyệt có thể sửa; UNITCALIBRATOR rộng hơn định nghĩa DOSAGE.",
            "Lấy mẫu có chủ đích nên phân bố quan hệ không phản ánh phân bố tự nhiên; báo cáo kèm cách lấy mẫu.",
        ],
        "candidates_sha256": sha256(out / "candidates.jsonl"),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in ("samples", "selection", "passages_with_pair_type",
                                                "candidate_pairs", "quota_shortfall", "audit")},
                     ensure_ascii=False, indent=2))
    if shortfall:
        print("CẢNH BÁO: không đủ đoạn cho", shortfall, "- báo cáo đúng số thực tế, không bịa thêm.")


if __name__ == "__main__":
    main()
