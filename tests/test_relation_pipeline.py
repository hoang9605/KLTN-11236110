"""Kiểm thử các bước dữ liệu của relation/: lô AI, kiểm tra nhãn AI, đánh dấu câu trên phiếu."""
import json

import pytest

from relation.ai_batches import check, item, marked
from relation.make_sheet import all_pairs, mark_pair

TEXT = "đau ở khớp gối và uống thuốc corticoid"


def ent(i, text, label):
    s = TEXT.index(text)
    return {"id": i, "text": text, "label": label, "start": s, "end": s + len(text)}


ROW = {"id": "S1", "text": TEXT,
       "entities": [ent("E1", "đau", "CONDITION"), ent("E2", "khớp gối", "BODY_PART"), ent("E3", "corticoid", "DRUG")]}


def test_all_pairs_follow_schema():
    pairs = {(p["head"], p["tail"], p["allowed_relation"]) for p in all_pairs(ROW)}
    assert pairs == {("E1", "E2", "located_at"), ("E1", "E3", "treated_by")}


def test_marks_keep_text():
    assert marked(ROW["text"], ROW["entities"]).startswith("[E1:CONDITION đau] ở [E2:BODY_PART khớp gối]")
    e = {x["id"]: x for x in ROW["entities"]}
    assert "[H: đau /H] ở [T: khớp gối /T]" in mark_pair(ROW["text"], e["E1"], e["E2"])


@pytest.mark.parametrize("labels,ok", [
    ({"E1": "VALID", "E2": "VALID", "E3": "VALID"}, {"P1": "located_at", "P2": "NO_RELATION"}),
    ({"E1": "VALID", "E2": "VALID", "E3": "INVALID"}, {"P1": "NO_RELATION", "P2": None}),
])
def test_check_accepts_valid(tmp_path, labels, ok):
    inp = tmp_path / "x_input.jsonl"
    inp.write_text(json.dumps(item(ROW), ensure_ascii=False) + "\n", encoding="utf-8")
    lab = tmp_path / "x_passA.jsonl"
    lab.write_text(json.dumps({"id": "S1", "entities": labels, "pairs": ok}) + "\n", encoding="utf-8")
    assert check(lab) == []


def test_check_rejects_wrong_relation_and_label_on_invalid(tmp_path):
    inp = tmp_path / "x_input.jsonl"
    inp.write_text(json.dumps(item(ROW), ensure_ascii=False) + "\n", encoding="utf-8")
    lab = tmp_path / "x_passA.jsonl"
    lab.write_text(json.dumps({"id": "S1", "entities": {"E1": "VALID", "E2": "VALID", "E3": "INVALID"},
                               "pairs": {"P1": "treated_by", "P2": "NO_RELATION"}}) + "\n", encoding="utf-8")
    errs = check(lab)
    assert len(errs) == 2


def test_scores_count_wrong_relation_and_missed_positive():
    from relation.evaluate import scores
    g = {"S:E1:E2:located_at": "located_at", "S:E1:E3:treated_by": "treated_by", "S:E1:E4:located_at": "NO_RELATION"}
    p = {"S:E1:E2:located_at": "located_at", "S:E1:E3:treated_by": "NO_RELATION", "S:E1:E4:located_at": "located_at"}
    s = scores(g, p)
    assert (s["micro"]["tp"], s["micro"]["fp"], s["micro"]["fn"]) == (1, 1, 1)
    assert s["macro_over"] == ["located_at", "treated_by"]


def test_synth_skeleton_and_ngrams():
    from relation.synth import ngrams, skeleton
    ents = [{"start": 0, "end": 3, "label": "CONDITION"}, {"start": 7, "end": 15, "label": "BODY_PART"}]
    assert skeleton("đau ở  khớp gối nhiều", ents) == "[condition] ở [body_part] nhiều"
    assert ngrams("a b c", 2) == {"a b", "b c"}
