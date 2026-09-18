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

from ner.config import (
    CLINICAL_SEVERITY_ADJECTIVES,
    DRUG_ACTION_BLACKLIST,
    TARGET_LABELS,
    VIETMED_TO_TARGET,
)
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



# ==============================================================================
# Rule 1 & Rule 2 Patch Tests
# ==============================================================================

def test_rule1_drug_action_blacklist_unit():
    """Rule 1 (Unit): Verify standalone action terms ('chỉ định', 'can thiệp', etc.) labeled as DRUG are discarded."""
    post = PostProcessor()
    entities = [
        RawEntity(surface_text="chỉ định", label="DRUG", start_char=10, end_char=18, confidence=0.95),
        RawEntity(surface_text="can thiệp", label="DRUG", start_char=20, end_char=29, confidence=0.92),
        RawEntity(surface_text="kê đơn", label="DRUG", start_char=30, end_char=36, confidence=0.90),
        RawEntity(surface_text="điều trị", label="DRUG", start_char=40, end_char=48, confidence=0.91),
        RawEntity(surface_text="Paracetamol", label="DRUG", start_char=50, end_char=61, confidence=0.99),
        RawEntity(surface_text="chỉ định", label="PROCEDURE", start_char=70, end_char=78, confidence=0.88),
    ]
    filtered = post.filter_drug_blacklist(entities)
    # The 4 DRUG action entities must be dropped; Paracetamol (DRUG) and chỉ định (PROCEDURE) must remain
    assert len(filtered) == 2
    assert filtered[0].surface_text == "Paracetamol"
    assert filtered[0].label == "DRUG"
    assert filtered[1].surface_text == "chỉ định"
    assert filtered[1].label == "PROCEDURE"


def test_rule1_drug_action_blacklist_e2e(pipeline):
    """Rule 1 (E2E): Sentence containing 'chỉ định' / 'can thiệp' -> verify dropped from output."""
    text = "Bác sĩ chỉ định can thiệp phẫu thuật và kê đơn Paracetamol 500mg cho bệnh nhân."
    res = pipeline.predict(text)
    _verify_entity_spans(res)

    extracted_drugs = [e for e in res["entities"] if e["label"] == "DRUG"]
    drug_texts = [e["surface_text"].strip().lower() for e in extracted_drugs]

    # Verify none of the blacklisted action words are labeled as DRUG
    for term in DRUG_ACTION_BLACKLIST:
        assert term not in drug_texts, f"Blacklisted term '{term}' was not filtered from DRUG"

    # Paracetamol must still be extracted as DRUG
    assert any("paracetamol" in t for t in drug_texts), "Legitimate DRUG 'Paracetamol' was incorrectly dropped"


def test_rule2_merge_severity_sot_cao_unit():
    """Rule 2 (Unit): Merge CONDITION + severity DOSAGE ('sốt' + 'cao' -> 'sốt cao' CONDITION)."""
    post = PostProcessor()
    text = "Bệnh nhân sốt cao liên tục."
    entities = [
        RawEntity(surface_text="sốt", label="CONDITION", start_char=10, end_char=13, confidence=0.98),
        RawEntity(surface_text="cao", label="DOSAGE", start_char=14, end_char=17, confidence=0.96),
    ]
    merged = post.merge_severity_into_condition(entities, text)
    assert len(merged) == 1
    assert merged[0].surface_text == "sốt cao"
    assert merged[0].label == "CONDITION"
    assert merged[0].start_char == 10
    assert merged[0].end_char == 17
    assert merged[0].confidence == round((0.98 + 0.96) / 2.0, 4)


def test_rule2_merge_severity_sot_cao_e2e(pipeline):
    """Rule 2 (E2E): Sentence 'sốt cao' -> verify 1 single CONDITION 'sốt cao', no leftover DOSAGE."""
    text = "Bệnh nhân sốt cao, mệt mỏi nhiều."
    res = pipeline.predict(text)
    _verify_entity_spans(res)

    # Verify no DOSAGE entity has text "cao"
    dosage_ents = [e for e in res["entities"] if e["label"] == "DOSAGE"]
    dosage_texts = [e["surface_text"].strip().lower() for e in dosage_ents]
    assert "cao" not in dosage_texts

    # Verify 'sốt cao' exists as a single CONDITION
    condition_ents = [e for e in res["entities"] if e["label"] == "CONDITION"]
    cond_texts = [e["surface_text"].strip().lower() for e in condition_ents]
    assert "sốt cao" in cond_texts, f"Expected 'sốt cao' in CONDITIONs, found {cond_texts}"


def test_rule2_real_dosage_not_merged_unit():
    """Rule 2 (Unit): Numeric dosage (e.g. '500mg') following CONDITION must NOT be merged."""
    post = PostProcessor()
    text = "Bệnh nhân đau ngực 500mg"
    entities = [
        RawEntity(surface_text="đau ngực", label="CONDITION", start_char=10, end_char=18, confidence=0.95),
        RawEntity(surface_text="500mg", label="DOSAGE", start_char=19, end_char=24, confidence=0.98),
    ]
    out = post.merge_severity_into_condition(entities, text)
    # Must NOT be merged
    assert len(out) == 2
    assert out[0].surface_text == "đau ngực"
    assert out[0].label == "CONDITION"
    assert out[1].surface_text == "500mg"
    assert out[1].label == "DOSAGE"


def test_rule2_severity_without_condition_not_deleted_unit():
    """Rule 2 (Unit): Severity adjective ('cao') NOT following CONDITION must be kept as DOSAGE, not deleted."""
    post = PostProcessor()
    # Case A: Following a TEST entity (not CONDITION)
    text_a = "Chỉ số huyết áp cao bất thường."
    entities_a = [
        RawEntity(surface_text="huyết áp", label="TEST", start_char=7, end_char=15, confidence=0.95),
        RawEntity(surface_text="cao", label="DOSAGE", start_char=16, end_char=19, confidence=0.92),
    ]
    out_a = post.merge_severity_into_condition(entities_a, text_a)
    assert len(out_a) == 2
    assert out_a[0].label == "TEST"
    assert out_a[1].label == "DOSAGE"
    assert out_a[1].surface_text == "cao"

    # Case B: Standalone at beginning of sentence
    text_b = "Cao điểm mùa sốt xuất huyết."
    entities_b = [
        RawEntity(surface_text="Cao", label="DOSAGE", start_char=0, end_char=3, confidence=0.85),
    ]
    out_b = post.merge_severity_into_condition(entities_b, text_b)
    assert len(out_b) == 1
    assert out_b[0].label == "DOSAGE"
    assert out_b[0].surface_text == "Cao"

