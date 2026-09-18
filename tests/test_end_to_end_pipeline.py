"""Integration tests for End-to-End Medical NER and Normalization Pipeline.

Verifies:
  1. End-to-end extraction and standard coding (ICD-10 for CONDITION, RxNorm for DRUG).
  2. Safe stubbing (BODY_PART, TEST, PROCEDURE -> normalized is None).
  3. Dosage handling (DOSAGE -> structured details, normalized is None).
  4. Toggle controls (`enable_normalization` constructor flag and `predict(..., normalize=bool)`).
  5. Helper methods (`normalize_entity`, `normalize_entities`).
  6. Pipeline aliases (`EndToEndMedicalPipeline`, `ClinicalPipeline`).
  7. Edge cases (empty string, non-clinical sentences).
  8. Dependency injection (custom normalizer).
"""
import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

import pytest
from unittest.mock import MagicMock

from ner import ClinicalPipeline, EndToEndMedicalPipeline, MedicalNERPipeline
from normalization.dispatcher import EntityNormalizationPipeline


@pytest.fixture(scope="module")
def pipeline():
    """Module-level pipeline instance with normalization enabled."""
    return MedicalNERPipeline(enable_console_logging=False, enable_normalization=True)


def test_pipeline_aliases():
    """Verify production class aliases."""
    assert EndToEndMedicalPipeline is MedicalNERPipeline
    assert ClinicalPipeline is MedicalNERPipeline


def test_e2e_condition_and_drug_normalization(pipeline):
    """Verify that CONDITION entities map to ICD-10 and DRUG entities map to RxNorm."""
    text = "Bệnh nhân đau dạ dày, chỉ định uống Paracetamol 500mg 2 viên/ngày."
    res = pipeline.predict(text)

    assert "text" in res
    assert "entities" in res
    entities = res["entities"]
    assert len(entities) > 0

    # Locate CONDITION entity
    cond_ents = [e for e in entities if e["label"] == "CONDITION"]
    assert len(cond_ents) >= 1
    cond = cond_ents[0]
    assert "normalized" in cond
    if cond["normalized"]:
        assert cond["normalized"]["ontology"] == "ICD-10"
        assert cond["normalized"]["code"] != ""
        assert "label_standard" in cond["normalized"]
        assert "match_method" in cond["normalized"]
        assert "match_score" in cond["normalized"]

    # Locate DRUG entity
    drug_ents = [e for e in entities if e["label"] == "DRUG"]
    assert len(drug_ents) >= 1
    drug = drug_ents[0]
    assert "normalized" in drug
    if drug["normalized"]:
        assert drug["normalized"]["ontology"] == "RxNorm"
        assert drug["normalized"]["code"] != ""
        assert "label_standard" in drug["normalized"]


def test_e2e_dosage_normalization_skipped(pipeline):
    """Verify that DOSAGE entities retain structured details and normalized is None."""
    text = "Bệnh nhân uống Tenofovir 300mg 1 viên/ngày."
    res = pipeline.predict(text)

    dosage_ents = [e for e in res["entities"] if e["label"] == "DOSAGE"]
    assert len(dosage_ents) >= 1
    dosage = dosage_ents[0]

    assert "normalized" in dosage
    assert dosage["normalized"] is None

    # Check structured dosage fields are preserved
    assert "value" in dosage
    assert "unit" in dosage


def test_e2e_stub_labels_normalization(pipeline):
    """Verify that BODY_PART, TEST, and PROCEDURE have normalized=None (safe stubs)."""
    text = "Khám dạ dày và chụp X-quang phổi cho bệnh nhân."
    res = pipeline.predict(text)

    for ent in res["entities"]:
        if ent["label"] in ("BODY_PART", "TEST", "PROCEDURE"):
            assert "normalized" in ent
            assert ent["normalized"] is None


def test_disable_normalization_via_predict_argument(pipeline):
    """Verify predict(normalize=False) bypasses normalization step."""
    text = "Bệnh nhân sốt cao uống Paracetamol 500mg."
    res = pipeline.predict(text, normalize=False)

    for ent in res["entities"]:
        assert "normalized" not in ent


def test_disable_normalization_via_pipeline_init():
    """Verify MedicalNERPipeline(enable_normalization=False) defaults to no normalization."""
    pipe = MedicalNERPipeline(enable_normalization=False, enable_console_logging=False)
    text = "Bệnh nhân sốt cao uống Paracetamol 500mg."

    # Normalization disabled by default
    res = pipe.predict(text)
    for ent in res["entities"]:
        assert "normalized" not in ent

    # Can be overridden dynamically on single call
    res_override = pipe.predict(text, normalize=True)
    for ent in res_override["entities"]:
        assert "normalized" in ent


def test_pipeline_helper_methods(pipeline):
    """Verify pipeline.normalize_entity and pipeline.normalize_entities helper methods."""
    single_entity = {
        "surface_text": "đau dạ dày",
        "label": "CONDITION",
        "start_char": 0,
        "end_char": 10,
        "confidence": 0.95,
    }
    norm = pipeline.normalize_entity(single_entity)
    assert norm is not None
    assert norm.ontology == "ICD-10"

    entity_list = [
        single_entity,
        {"surface_text": "Paracetamol", "label": "DRUG", "start_char": 12, "end_char": 23, "confidence": 0.98},
    ]
    batch_norm = pipeline.normalize_entities(entity_list)
    assert len(batch_norm) == 2
    assert "normalized" in batch_norm[0]
    assert batch_norm[0]["normalized"]["ontology"] == "ICD-10"
    assert "normalized" in batch_norm[1]
    assert batch_norm[1]["normalized"]["ontology"] == "RxNorm"


def test_custom_normalizer_injection():
    """Verify dependency injection of a custom normalizer."""
    mock_normalizer = MagicMock()
    mock_normalizer.normalize_entities.return_value = [
        {"surface_text": "Aspirin", "label": "DRUG", "normalized": {"ontology": "Custom", "code": "C123"}}
    ]

    pipe = MedicalNERPipeline(
        enable_normalization=True,
        normalizer=mock_normalizer,
        enable_console_logging=False,
    )
    res = pipe.predict("Uống Aspirin")

    mock_normalizer.normalize_entities.assert_called_once()
    assert res["entities"][0]["normalized"]["ontology"] == "Custom"


def test_empty_and_whitespace_edge_cases(pipeline):
    """Verify empty or whitespace strings return empty entities without error."""
    assert pipeline.predict("")["entities"] == []
    assert pipeline.predict("   \n\t  ")["entities"] == []
    assert pipeline.predict(None)["entities"] == []
