"""Kiểm thử re_v3/synth_pattern.py: offset, nhãn, tỉ lệ dương, tái lập theo seed."""
import random

import pytest

from relation_extraction.data import NEGATIVE, load_pairs
from re_v3 import config
from re_v3.common import check_record, write_jsonl
from re_v3.synth_pattern import Lexicon, fill, generate, ratio, render, replace_entity

pytestmark = pytest.mark.skipif(not (config.PATTERNS_DIR / "pair_contexts.jsonl").exists(),
                                reason="chạy python -m re_v3.mine_patterns trước")


def test_render_offsets():
    text, spans = render("{H} ở vùng {T}", {"H": "đau", "T": "bụng"}, prefix="thì", suffix="rồi")
    assert text == "thì đau ở vùng bụng rồi"
    assert text[slice(*spans["H"])] == "đau" and text[slice(*spans["T"])] == "bụng"


def test_replace_entity_shifts_later_offsets():
    row = {"text": "đau ở bụng và đầu",
           "entities": [{"id": "E1", "label": "CONDITION", "start": 0, "end": 3, "text": "đau"},
                        {"id": "E2", "label": "BODY_PART", "start": 6, "end": 10, "text": "bụng"},
                        {"id": "E3", "label": "BODY_PART", "start": 14, "end": 17, "text": "đầu"}]}
    text, ents = replace_entity(row, "E2", "dạ dày")
    assert text == "đau ở dạ dày và đầu"
    assert [e["text"] for e in ents] == ["đau", "dạ dày", "đầu"]


def test_fill_avoids_topical_with_oral_verb():
    lex, rng = Lexicon(), random.Random(0)
    for _ in range(200):
        r = fill("uống {T} để chữa {H}", [("H", "T", True)], "treated_by", lex, rng)
        if r:
            drug = next(e["text"] for e in r[1] if e["label"] == "DRUG")
            assert drug not in lex.topical_drugs


@pytest.fixture(scope="module")
def rows():
    return generate(seed=7, positives_per_relation=60, per_sentence=2, hard_negative_ratio=2.0)[0]


def test_records_valid_and_loadable(rows, tmp_path):
    for r in rows:
        check_record(r)
        assert r["human_verified"] is False and r["annotation_status"] == "SYNTHETIC_PATTERN"
    path = tmp_path / "s.jsonl"
    write_jsonl(path, rows)
    pairs, audit = load_pairs(path, allow_ai=True)
    assert audit["included_pairs"] == sum(len(r["relations"]) for r in rows)
    with pytest.raises(ValueError):
        load_pairs(path)            # không bao giờ được coi là nhãn người duyệt


def test_positive_ratio_and_every_relation_present(rows):
    low, high = config.TARGET_POSITIVE_RATIO
    assert low - 0.01 <= ratio(rows) <= high + 0.01
    rels = {x["allowed_relation"] for r in rows for x in r["relations"] if x["label"] != NEGATIVE}
    assert rels == {"located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage"}


def test_no_dosage_replacement_and_deterministic(rows):
    assert all(r.get("replaced", {}).get("entity") is None or
               next(e for e in r["entities"] if e["id"] == r["replaced"]["entity"])["label"] != "DOSAGE"
               for r in rows)
    again = generate(seed=7, positives_per_relation=60, per_sentence=2, hard_negative_ratio=2.0)[0]
    assert [r["text"] for r in again] == [r["text"] for r in rows]
