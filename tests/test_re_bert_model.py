"""ViHealthBERT RE extractor: interface used by the pipeline, unsupported relations, loading."""
from pathlib import Path

import pytest

import relation_extraction.bert_model as bm
from knowledge_graph import HybridRelationExtractor
from relation_extraction.bert_model import BertRelationExtractor, load_extractor
from relation_extraction.model import RelationExtractor

ROOT = Path(__file__).resolve().parents[1]
DEPLOYED = ROOT / "Model/vihealthbert-re-vietmed-811"
TEXT = "Đau ở vùng bụng, uống paracetamol."
ENTS = [{"id": "E1", "label": "CONDITION", "start": 0, "end": 3},
        {"id": "E2", "label": "BODY_PART", "start": 6, "end": 15},
        {"id": "E3", "label": "DRUG", "start": 22, "end": 33}]


def fake_extractor(supported, prob):
    cfg = {"max_len": 192, "threshold": 0.5, "supported_relations": supported, "label_source": "test"}
    return BertRelationExtractor(["seed_a", "seed_b"], None, None, cfg, None), prob


def test_predict_averages_seeds_marks_unsupported_and_thresholds(monkeypatch):
    ext, _ = fake_extractor(["located_at"], None)
    seen = []
    by_seed = {"seed_a": 0.9, "seed_b": 0.3}  # mean 0.6 -> positive although seed_b alone says negative
    monkeypatch.setattr(bm, "positive_probs", lambda m, t, s, pairs, ml, d: seen.extend(pairs) or [by_seed[m]] * len(pairs))
    preds = {(p["head"], p["tail"], p["allowed_relation"]): p for p in ext.predict(TEXT, ENTS)}
    got = preds[("E1", "E2", "located_at")]
    assert (got["label"], got["status"]) == ("located_at", "predicted") and abs(got["score"] - 0.6) < 1e-9
    assert preds[("E1", "E3", "treated_by")]["status"] == "unsupported"
    assert all(p["allowed_relation"] == "located_at" for p in seen)  # unsupported pairs never reach the encoder


def test_hybrid_uses_rules_for_unsupported(monkeypatch):
    ext, _ = fake_extractor(["located_at"], 0.1)
    monkeypatch.setattr(bm, "positive_probs", lambda m, t, s, pairs, ml, d: [0.1] * len(pairs))
    hybrid = HybridRelationExtractor(ext)
    out = {(p["head"], p["tail"], p["allowed_relation"]): p for p in hybrid.predict(TEXT, ENTS)}
    assert out[("E1", "E2", "located_at")]["source"] in ("model", "rule")
    assert out[("E1", "E3", "treated_by")]["source"] == "rule"
    assert hybrid.metadata["model_name"] == "vihealthbert-entity-marker"


def test_load_extractor_dispatches_on_path():
    assert isinstance(load_extractor(ROOT / "outputs/re_ai_v2/model.joblib"), RelationExtractor)


@pytest.mark.skipif(not (DEPLOYED / "re_config.json").exists() or not list(DEPLOYED.glob("model_seed*.safetensors")),
                    reason="trọng số ViHealthBERT RE không có trong git")
def test_deployed_model_loads_and_predicts():
    ext = load_extractor(DEPLOYED, device="cpu")
    preds = ext.predict(TEXT, ENTS)
    assert {p["status"] for p in preds} <= {"predicted", "unsupported"}
    assert all(0.0 <= p["score"] <= 1.0 for p in preds if p["status"] == "predicted")
    assert ext.metadata["human_verified"] is False
