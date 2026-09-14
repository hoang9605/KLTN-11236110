"""Comprehensive test suite for Vietnamese Medical NER Pipeline.

Covers:
  - Unit tests for preprocessor, dosage regex, overlap resolver, label mapping.
  - End-to-end integration tests using ViHealthBERT model:
      1. Consecutive entities
      2. Punctuated text with punctuation between entities
      3. DOSAGE forms ("500mg", "2 viên/ngày", composite "500mg 2 viên/ngày")
      4. Empty string and whitespace-only input
      5. Non-clinical text (zero entities)
      6. Long text exceeding max sequence length (sentence chunking)
"""
import json
import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Windows OpenMP safety
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

import pytest

from ner.config import TARGET_LABELS, VIETMED_TO_TARGET
from ner.dosage_extractor import DosageEntity, DosageExtractor
from ner.pipeline import MedicalNERPipeline
from ner.postprocessor import PostProcessor
from ner.predictor import RawEntity
from ner.preprocessor import TextPreprocessor, WordToken


# ==============================================================================
# Unit Tests
# ==============================================================================

def test_whitespace_normalization():
    """Test whitespace normalization preserving medical tokens."""
    preprocessor = TextPreprocessor()
    raw = "  Bệnh nhân    đau ngực ,  uống   Aspirin  100mg .   "
    clean = preprocessor.normalize_whitespace(raw)
    assert clean == "Bệnh nhân đau ngực , uống Aspirin 100mg ."


def test_tokenization_punctuation_decoupling():
    """Verify punctuation is strictly decoupled from word tokens."""
    preprocessor = TextPreprocessor()
    text = "đau dạ dày, viêm gan B (mạn tính): uống Paracetamol 500mg."
    tokens = preprocessor.tokenize_words(text)
    token_texts = [t.text for t in tokens]

    # Punctuation must be isolated tokens
    assert "," in token_texts
    assert "(" in token_texts
    assert ")" in token_texts
    assert ":" in token_texts
    assert "." in token_texts

    # Tokens must not have attached punctuation
    assert "dày," not in token_texts
    assert "tính):" not in token_texts
    assert "500mg." not in token_texts

    # Offsets must match exactly
    for tok in tokens:
        assert text[tok.start_char:tok.end_char] == tok.text


def test_label_mapping_and_filtering():
    """Verify 37 VietMed labels map into 6 target categories and others become 'O'."""
    assert VIETMED_TO_TARGET["DISEASESYMTOM"] == "CONDITION"
    assert VIETMED_TO_TARGET["DRUGCHEMICAL"] == "DRUG"
    assert VIETMED_TO_TARGET["PREVENTIVEMED"] == "DRUG"
    assert VIETMED_TO_TARGET["ORGAN"] == "BODY_PART"
    assert VIETMED_TO_TARGET["DIAGNOSTICS"] == "TEST"
    assert VIETMED_TO_TARGET["SURGERY"] == "PROCEDURE"
    assert VIETMED_TO_TARGET["MEDDEVICETECHNIQUE"] == "PROCEDURE"
    assert VIETMED_TO_TARGET["TREATMENT"] == "PROCEDURE"
    assert VIETMED_TO_TARGET["UNITCALIBRATOR"] == "DOSAGE"

    # Non-target classes must not be in mapping
    non_targets = [
        "AGE", "GENDER", "DATETIME", "OCCUPATION", "LOCATION",
        "ORGANIZATION", "FOODDRINK", "PERSONALCARE", "TRANSPORTATION"
    ]
    for nt in non_targets:
        assert nt not in VIETMED_TO_TARGET


def test_dosage_regex_extraction():
    """Verify clinical dosage regex extracts value, unit, and frequency."""
    extractor = DosageExtractor()

    # Case A: Standalone strength
    t1 = "Uống Paracetamol 500mg khi sốt."
    d1 = extractor.extract_regex_dosages(t1)
    assert len(d1) == 1
    assert d1[0].surface_text == "500mg"
    assert d1[0].value == "500"
    assert d1[0].unit == "mg"

    # Case B: Form + Frequency
    t2 = "Dùng 2 viên/ngày sau bữa ăn."
    d2 = extractor.extract_regex_dosages(t2)
    assert len(d2) >= 1
    assert any("2 viên" in d.surface_text for d in d2)

    # Case C: Composite strength + form + frequency
    t3 = "Augmentin 500mg 2 viên/ngày"
    d3 = extractor.extract_regex_dosages(t3)
    assert len(d3) == 1
    assert d3[0].surface_text == "500mg 2 viên/ngày"
    assert d3[0].frequency == "2 viên/ngày"


def test_overlap_resolution_higher_confidence():
    """Verify that when 2 entities overlap, higher confidence is strictly preserved."""
    post = PostProcessor()
    text = "Bệnh nhân đau dạ dày cấp tính"

    # Simulated overlapping entities:
    # E1: "đau dạ dày" [10:20] CONDITION, conf=0.85
    # E2: "dạ dày" [14:20] BODY_PART, conf=0.98
    e1 = RawEntity(surface_text="đau dạ dày", label="CONDITION", start_char=10, end_char=20, confidence=0.85)
    e2 = RawEntity(surface_text="dạ dày", label="BODY_PART", start_char=14, end_char=20, confidence=0.98)

    resolved = post.filter_and_resolve_overlaps([e1, e2], text)
    assert len(resolved) == 1
    assert resolved[0]["surface_text"] == "dạ dày"
    assert resolved[0]["label"] == "BODY_PART"
    assert resolved[0]["confidence"] == 0.98


# ==============================================================================
# Pipeline Integration Tests (Using Pretrained ViHealthBERT Model)
# ==============================================================================

@pytest.fixture(scope="module")
def pipeline():
    """Shared pipeline instance for integration tests."""
    return MedicalNERPipeline()


def _verify_entity_spans(result: dict):
    """Utility to assert that every entity span matches the exact surface text."""
    text = result["text"]
    for ent in result["entities"]:
        s = ent["start_char"]
        e = ent["end_char"]
        surf = ent["surface_text"]
        lbl = ent["label"]
        conf = ent["confidence"]

        assert lbl in TARGET_LABELS, f"Invalid label: {lbl}"
        assert 0.0 <= conf <= 1.0, f"Confidence out of bounds: {conf}"
        assert text[s:e] == surf, f"Span mismatch! text[{s}:{e}]='{text[s:e]}' vs '{surf}'"


def test_empty_string(pipeline):
    """Case 4: Empty string and whitespace-only."""
    res_empty = pipeline.predict("")
    assert res_empty["entities"] == []

    res_spaces = pipeline.predict("   \t  \n  ")
    assert res_spaces["entities"] == []


def test_non_clinical_text(pipeline):
    """Case 5: Non-clinical sentence without medical entities."""
    text = "Hôm nay trời nhiều mây và có thể có mưa rào vào buổi chiều."
    res = pipeline.predict(text)
    print("\n--- Non-clinical Text Output ---")
    print(json.dumps(res, ensure_ascii=False, indent=2))
    assert res["entities"] == []


def test_consecutive_entities(pipeline):
    """Case 1: Multiple consecutive entities."""
    text = "Bệnh nhân đau dạ dày, viêm gan B, chỉ định nội soi dạ dày."
    res = pipeline.predict(text)
    print("\n--- Consecutive Entities Output ---")
    print(json.dumps(res, ensure_ascii=False, indent=2))

    _verify_entity_spans(res)
    labels = [e["label"] for e in res["entities"]]
    surfaces = [e["surface_text"] for e in res["entities"]]

    # Expect CONDITION / BODY_PART / PROCEDURE entities
    assert len(res["entities"]) >= 2
    assert any(lbl in ("CONDITION", "BODY_PART") for lbl in labels)


def test_punctuated_text(pipeline):
    """Case 2: Punctuation interspersed between entities."""
    text = "Chẩn đoán: Viêm gan B (mạn tính); điều trị: Tenofovir 300mg; xét nghiệm: ALT, AST."
    res = pipeline.predict(text)
    print("\n--- Punctuated Text Output ---")
    print(json.dumps(res, ensure_ascii=False, indent=2))

    _verify_entity_spans(res)
    # Check that punctuation like ';', ':', '(', ')' are never in surface_text
    for ent in res["entities"]:
        for bad_char in [";", ":", "(", ")"]:
            assert not ent["surface_text"].startswith(bad_char)
            assert not ent["surface_text"].endswith(bad_char)


def test_dosage_patterns(pipeline):
    """Case 3: Dosage forms '500mg' and '2 viên/ngày'."""
    text = "Bệnh nhân sốt cao, uống Paracetamol 500mg 2 viên/ngày sau bữa ăn."
    res = pipeline.predict(text)
    print("\n--- Dosage Patterns Output ---")
    print(json.dumps(res, ensure_ascii=False, indent=2))

    _verify_entity_spans(res)
    labels = [e["label"] for e in res["entities"]]
    assert "DOSAGE" in labels
    assert "DRUG" in labels

    # Find the dosage entity
    dosage_ents = [e for e in res["entities"] if e["label"] == "DOSAGE"]
    assert len(dosage_ents) >= 1
    d_surf = dosage_ents[0]["surface_text"]
    assert "500mg" in d_surf or "viên" in d_surf


def test_long_text_sentence_chunking(pipeline):
    """Case 6: Long medical record exceeding max_position_embeddings (258 subtokens)."""
    long_sentences = [
        "Bệnh nhân nam 65 tuổi, tiền sử tăng huyết áp và đái tháo đường tuýp 2 đang điều trị đều.",
        "Cách nhập viện 3 ngày, bệnh nhân xuất hiện đau tức ngực trái âm ỉ, lan lên vai trái và hàm dưới.",
        "Khám lâm sàng ghi nhận huyết áp 150/90 mmHg, nhịp tim đều 85 lần/phút, không có ran ở phổi.",
        "Bác sĩ chỉ định làm điện tâm đồ và xét nghiệm men tim Troponin T định lượng.",
        "Kết quả điện tâm đồ ghi nhận đoạn ST chênh lên ở các chuyển đạo V1 đến V4, chẩn đoán nhồi máu cơ tim cấp.",
        "Bệnh nhân được xử trí cấp cứu: thở oxy qua gọng kính, dùng Aspirin 300mg nhai và Clopidogrel 300mg uống.",
        "Bệnh nhân được chuyển khoa Tim mạch can thiệp để chụp mạch vành và đặt stent động mạch vành.",
        "Sau can thiệp, bệnh nhân ổn định, tiếp tục dùng Atorvastatin 20mg 1 viên/ngày và Enoxaparin tiêm dưới da."
    ]
    long_text = " ".join(long_sentences)

    res = pipeline.predict(long_text)
    print("\n--- Long Text Chunking Output ---")
    print(f"Input text length: {len(long_text)} characters")
    print(f"Total entities extracted: {len(res['entities'])}")
    print(json.dumps(res, ensure_ascii=False, indent=2))

    _verify_entity_spans(res)
    assert len(res["entities"]) >= 5

    # Check distribution of extracted labels
    labels = {e["label"] for e in res["entities"]}
    assert "CONDITION" in labels or "DRUG" in labels or "PROCEDURE" in labels

