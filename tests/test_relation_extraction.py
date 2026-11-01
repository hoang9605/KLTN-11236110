import copy
import json

import pytest

from relation_extraction.data import load_pairs, split_pairs, mark_pair, candidates
from relation_extraction.model import RelationExtractor, evaluate
from relation_extraction.pipeline import MedicalREPipeline


def record(label="located_at", sample_id="one"):
    return {"id": sample_id, "text": "đau ở gan", "human_verified": False,
            "training_eligible": False, "review_flags": ["provisional"],
            "entities": [{"id": "E1", "label": "CONDITION", "start": 0, "end": 3, "text": "đau"},
                         {"id": "E2", "label": "BODY_PART", "start": 6, "end": 9, "text": "gan"}],
            "relations": [{"head": "E1", "tail": "E2", "label": label}]}


def write_rows(tmp_path, rows):
    path = tmp_path / "data.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
    return path


def test_ai_opt_in_unknown_not_negative_and_no_invented_pairs(tmp_path):
    rows = [record(), record("CHUA_RO", "two"), record("NO_RELATION", "three"), record(sample_id="four")]
    rows[-1]["relations"] = []
    path = write_rows(tmp_path, rows)
    with pytest.raises(ValueError, match="allow_ai"):
        load_pairs(path)
    pairs, audit = load_pairs(path, allow_ai=True)
    assert [p["label"] for p in pairs] == ["located_at", "NO_RELATION"]
    assert audit["unknown_pairs_excluded"] == 1
    assert audit["included_pairs_with_review_flags"] == 2
    assert pairs[0]["human_verified"] is False


@pytest.mark.parametrize("error", ["offset", "direction", "duplicate", "missing", "wrong_label"])
def test_invalid_annotations_fail(tmp_path, error):
    row = record()
    if error == "offset":
        row["entities"][0]["end"] = 4
    elif error == "direction":
        row["relations"][0].update(head="E2", tail="E1")
    elif error == "duplicate":
        row["relations"].append(copy.deepcopy(row["relations"][0]))
    elif error == "missing":
        row["relations"][0]["head"] = "E404"
    else:
        row["relations"][0]["label"] = "treated_by"
    with pytest.raises(ValueError):
        load_pairs(write_rows(tmp_path, [row]), allow_ai=True)


def test_group_split_reproducible_no_duplicate_text_leak(tmp_path):
    rows = []
    for i in range(30):
        r = record("located_at" if i % 2 else "NO_RELATION", str(i))
        r["text"] += " " + str(i // 2)
        rows.append(r)
    pairs, _ = load_pairs(write_rows(tmp_path, rows), allow_ai=True)
    splits = split_pairs(pairs, seed=42)
    assert splits == split_pairs(pairs, seed=42)
    groups = [{p["group"] for p in v} for v in splits.values()]
    assert all(groups)
    assert not groups[0] & groups[1] and not groups[0] & groups[2] and not groups[1] & groups[2]
    assert sum(map(len, splits.values())) == len(pairs)


def test_markers_direction_and_candidate_schema():
    row = record()
    head, tail = row["entities"]
    marked = mark_pair(row["text"], head, tail)
    assert "[HEAD_CONDITION]đau[/HEAD]" in marked
    assert "[TAIL_BODY_PART]gan[/TAIL]" in marked
    assert len(candidates(row["text"], [tail, head])) == 1
    reversed_text = "gan bị đau"
    assert "[TAIL_BODY_PART]gan[/TAIL]" in mark_pair(reversed_text, {**head, "start": 7, "end": 10}, {**tail, "start": 0, "end": 3})


def test_fit_save_load_and_unsupported(tmp_path):
    pairs, _ = load_pairs(write_rows(tmp_path, [record(), record("NO_RELATION", "two")]), allow_ai=True)
    model = RelationExtractor().fit(pairs)
    before = model.predict_pairs(pairs)
    model.save(tmp_path / "model.joblib")
    restored = RelationExtractor.load(tmp_path / "model.joblib")
    assert before == restored.predict_pairs(pairs)
    unseen = {**pairs[0], "allowed_relation": "diagnosed_by"}
    assert restored.predict_pairs([unseen])[0]["status"] == "unsupported"
    assert restored.predict_pairs([unseen])[0]["label"] is None


def test_positive_metrics_count_negative_false_positives():
    result = evaluate(["located_at", "NO_RELATION", "treated_by"], ["located_at", "located_at", None])
    assert result["positive_micro"]["precision"] == pytest.approx(0.5)
    assert result["positive_micro"]["recall"] == pytest.approx(0.5)
    assert result["positive_micro"]["f1"] == pytest.approx(0.5)
    assert result["per_relation"]["diagnosed_by"]["support"] == 0


def test_ner_adapter_uses_returned_text_and_offsets(tmp_path):
    pairs, _ = load_pairs(write_rows(tmp_path, [record(), record("NO_RELATION", "two")]), allow_ai=True)
    model = RelationExtractor().fit(pairs)

    class NER:
        def predict(self, text, normalize=None):
            return {"text": "đau ở gan", "entities": [
                {"label": "CONDITION", "start_char": 0, "end_char": 3, "surface_text": "đau"},
                {"label": "BODY_PART", "start_char": 6, "end_char": 9, "surface_text": "gan"}]}

    output = MedicalREPipeline(model, ner=NER()).predict("đau   ở gan")
    assert output["text"] == "đau ở gan"
    assert len(output["relation_candidates"]) == 1
    assert output["entities"][0]["id"] == "E1"
    assert model.predict("", []) == []
