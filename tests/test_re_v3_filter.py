"""Kiểm thử re_v3/filter_synth.py: rò rỉ test, trùng lặp, giới hạn khung câu, lấy mẫu theo tỉ lệ."""
import json
import random

import pytest

from relation_extraction.data import NEGATIVE
from re_v3 import config
from re_v3.filter_synth import run, skeleton, subsample
from re_v3.synth_pattern import make_record, ratio

pytestmark = pytest.mark.skipif(not all(p.exists() for p in config.SEED_FILES), reason="thiếu dữ liệu seed")


def rec(i, cond, body, label="located_at", mid="ở"):
    text = f"{cond} {mid} {body}"
    ents = [{"id": "E1", "label": "CONDITION", "start": 0, "end": len(cond), "text": cond},
            {"id": "E2", "label": "BODY_PART", "start": len(cond) + len(mid) + 2, "end": len(text), "text": body}]
    return make_record(f"SP-{i:05d}", "template", text, ents,
                       [{"head": "E1", "tail": "E2", "allowed_relation": "located_at", "label": label}])


def test_leak_duplicate_and_skeleton_cap(tmp_path):
    test_text = "một hai ba bốn năm sáu bảy tám chín mười"
    test_file = tmp_path / "test.jsonl"
    test_file.write_text(json.dumps({"text": test_text}, ensure_ascii=False) + "\n", encoding="utf-8")
    leak = rec(1, "đau", "bụng", mid="một hai ba bốn năm sáu bảy tám")   # chung 8-gram với test
    dup_a, dup_b = rec(2, "viêm", "khớp"), rec(3, "viêm", "khớp")
    same_skeleton = [rec(10 + i, c, "da", label=NEGATIVE) for i, c in enumerate(["mụn", "nám", "chàm", "vảy nến", "khô ngứa"])]
    rows = [leak, dup_a, dup_b] + same_skeleton
    kept, _, audit = run(rows, random.Random(0), test_paths=[test_file])
    ids = {r["id"] for r in kept}
    assert "SP-00001" not in ids and audit["drop_test_leak"] == 1
    assert "SP-00002" in ids and "SP-00003" not in ids
    # dup_a cũng có khung "[CONDITION] ở [BODY_PART]", nên chiếm một suất
    assert audit["drop_skeleton_cap"] == 1 + len(same_skeleton) - config.MAX_PER_SKELETON
    assert all("filter_flags" in r for r in kept)


def test_skeleton_masks_entities():
    assert skeleton(rec(1, "đau", "bụng")) == "[CONDITION] ở [BODY_PART]"


def test_subsample_keeps_ratio():
    rows = [rec(i, f"bệnh{i}", "da", label="located_at" if i % 4 == 0 else NEGATIVE, mid=f"x{i}") for i in range(400)]
    small = subsample(rows, 100, random.Random(1))
    assert 90 <= sum(len(r["relations"]) for r in small) <= 110
    assert abs(ratio(small) - ratio(rows)) < 0.03
