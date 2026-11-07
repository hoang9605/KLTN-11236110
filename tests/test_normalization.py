"""Comprehensive unit and integration test suite for medical normalization module.

Tests:
1. ICD10Normalizer:
   - >= 10 known conditions with ground-truth codes.
   - Critical regression test: 'đau bụng' is never matched to 'đau lưng'.
   - Exact matching, synonym dictionary matching, regex pattern matching.
   - Strict no-guess rejection for unknown inputs.
2. RxNormNormalizer:
   - 5-10 common drugs with mocked HTTP responses.
   - SQLite caching verification (zero network calls on hit).
   - Unmatched drug tracking to log file.
   - Live API integration test (skips gracefully if offline).
3. Dispatcher & Pipeline:
   - Label-based routing (CONDITION -> ICD10, DRUG -> RxNorm).
   - Safe stubs for BODY_PART, TEST, PROCEDURE returning None.
   - Skipping of DOSAGE without error.
   - Batch entity enrichment.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

from normalization.base import NormalizedResult
from normalization.dispatcher import (
    EntityNormalizationPipeline,
    get_default_pipeline,
    normalize_entity,
)
from normalization.icd10 import ICD10Normalizer
from normalization.rxnorm import RxNormNormalizer
from normalization.stubs import FMANormalizer, LOINCNormalizer, MeSHNormalizer


# =====================================================================
# 1. ICD-10 Normalizer Tests
# =====================================================================
@pytest.fixture(scope="module")
def shared_icd10_normalizer():
    """Shared ICD10Normalizer instance with warm cache."""
    return ICD10Normalizer()


class TestICD10Normalizer:
    """Test suite for ICD-10 condition normalization."""

    def test_critical_dau_bung_not_dau_lung(self, shared_icd10_normalizer):
        """CRITICAL: 'đau bụng' MUST NOT be mapped to 'đau lưng' (M54)."""
        res = shared_icd10_normalizer.normalize("đau bụng")
        assert res is not None
        assert res.code == "R10", f"Expected R10 for 'đau bụng', got {res.code}"
        assert res.code != "M54", "CRITICAL BUG: 'đau bụng' mapped to 'đau lưng' (M54)!"
        assert "lưng" not in res.label_standard.lower()

    def test_exact_matches(self, shared_icd10_normalizer):
        """Verify exact matches against Ministry of Health ICD-10 catalog."""
        cases = [
            ("đau lưng", "M54", "Đau lưng"),
            ("đau đầu", "R51", "Đau đầu"),
            ("thương hàn", "A01.0", "Thương hàn"),
            ("bệnh tả không đặc hiệu", "A00.9", "Bệnh tả, không đặc hiệu"),
        ]
        for query, expected_code, expected_label in cases:
            res = shared_icd10_normalizer.normalize(query)
            assert res is not None, f"Failed to match: {query}"
            assert res.code == expected_code, f"Wrong code for {query}: {res.code} vs {expected_code}"
            assert res.match_method == "exact"

    def test_synonym_matches(self, shared_icd10_normalizer):
        """Verify synonym dictionary resolutions."""
        synonym_cases = [
            ("nhức đầu", "R51"),
            ("sốt cao", "R50"),
            ("sốt", "R50"),
            ("cao huyết áp", "I10"),
            ("tiểu đường", "E14"),
            ("viêm phổi", "J18"),
            ("viêm họng", "J02"),
            ("đột quỵ", "I64"),
            ("tai biến mạch máu não", "I64"),
            ("đau bao tử", "K29"),
        ]
        for query, expected_code in synonym_cases:
            res = shared_icd10_normalizer.normalize(query)
            assert res is not None, f"Failed to match synonym: {query}"
            assert res.code == expected_code, f"Wrong code for {query}: {res.code} vs {expected_code}"
            assert res.match_method == "synonym"

    def test_cancer_pattern_synonyms(self, shared_icd10_normalizer):
        """Verify pattern-based cancer mappings ('ung thư X' -> 'u ác của X')."""
        cancer_cases = [
            ("ung thư gan", "C22"),
            ("ung thư phổi", "C34"),
            ("ung thư dạ dày", "C16"),
            ("ung thư đại tràng", "C18"),
            ("ung thư vú", "C50"),
        ]
        for query, expected_code in cancer_cases:
            res = shared_icd10_normalizer.normalize(query)
            assert res is not None, f"Failed pattern match for: {query}"
            assert res.code == expected_code, f"Wrong cancer code for {query}: {res.code} vs {expected_code}"
            assert res.match_method == "synonym"

    def test_audit_regression_cases(self, shared_icd10_normalizer):
        """CRITICAL: Specific regression test cases from original audit that were previously mismapped.
        - 'vàng da': previously mapped to Q18.3 ('Màng da cổ'), MUST be R17 ('Vàng da không xác định').
        - 'rối loạn thần kinh': previously mapped to H53 ('Rối loạn thị giác'), MUST be None.
        - 'Viêm' (standing alone): previously mapped to L30.4 ('Viêm kẽ'), MUST be None.
        - 'não': previously mapped to G80 ('Bại não'), MUST be None.
        """
        # 1. vàng da -> R17
        res_vd = shared_icd10_normalizer.normalize("vàng da")
        assert res_vd is not None
        assert res_vd.code == "R17", f"Expected R17 for 'vàng da', got {res_vd.code}"
        assert res_vd.code != "Q18.3", "CRITICAL BUG: 'vàng da' mapped to 'Màng da cổ' (Q18.3)!"
        assert res_vd.match_method == "synonym"
        assert res_vd.label_standard == "Vàng da không xác định"

        # 2. rối loạn thần kinh -> None (not H53)
        res_rltk = shared_icd10_normalizer.normalize("rối loạn thần kinh")
        assert res_rltk is None, f"Expected None for ambiguous 'rối loạn thần kinh', got {res_rltk}"

        # 3. Viêm (alone) -> None (not L30.4)
        res_viem = shared_icd10_normalizer.normalize("Viêm")
        assert res_viem is None, f"Expected None for incomplete 'Viêm', got {res_viem}"

        # 4. não (as CONDITION or BODY_PART) -> None (not G80)
        res_nao_cond = shared_icd10_normalizer.normalize("não")
        assert res_nao_cond is None, f"Expected None for anatomical 'não' in ICD-10, got {res_nao_cond}"
        res_nao_entity = normalize_entity({"surface_text": "não", "label": "BODY_PART"})
        assert res_nao_entity is None

    def test_fuzzy_subset_false_matches_rejected(self, shared_icd10_normalizer):
        """Soát 05/11/2026: token_set_ratio cho 100 khi một tập từ chứa tập kia, gây gán sai mã.
        Luật mới (từ đầu cụm của ứng viên phải có trong truy vấn; cụm ngắn <= 2 từ không được là
        tập con thực sự) phải tự chặn các ca này, kể cả khi không có từ đồng nghĩa."""
        from normalization.icd10 import normalize_vietnamese_text
        wrong = {"huyết áp cao": "Z01.3", "đa xơ cứng": "K74.1", "rối loạn mỡ máu": "D55",
                 "nhồi máu": "D73.5", "đậu mùa bò": "B03"}
        for query in wrong:
            assert shared_icd10_normalizer._fuzzy_search(normalize_vietnamese_text(query)) is None, query
        for query, bad in wrong.items():
            res = shared_icd10_normalizer.normalize(query)
            assert res is None or res.code != bad, f"{query} still mapped to {bad}"
        expected = {"huyết áp cao": "I10", "rối loạn mỡ máu": "E78", "đa xơ cứng": "G35", "đậu mùa bò": "B08.0"}
        for query, code in expected.items():
            assert shared_icd10_normalizer.normalize(query).code == code
        # Các ca đúng trước đây vẫn phải giữ
        # 'mảng xơ vữa động mạch' is now a dictionary alias to the more specific I70.9.
        keep = {"mảng xơ vữa động mạch": "I70", "nhồi máu cơ tim": "I21", "viêm loét dạ dày": "K25"}
        for query, code in keep.items():
            assert shared_icd10_normalizer.normalize(query).code.startswith(code)

    def test_fuzzy_matches_boundary(self, shared_icd10_normalizer):
        """Verify rapidfuzz matching behaves correctly at threshold boundaries (~0.85).
        
        Boundary positive cases (slight typos of catalog diseases with score >= 0.85):
        - 'viêm xoang trán mản' (typo of 'Viêm xoang trán cấp', score ~ 0.88) -> J01.1
        - 'sốt xuất huýet dengue' (typo of 'Sốt xuất huyết Dengue', score ~ 0.90) -> A97
        - 'loét dạ day' (typo of 'Loét dạ dày', score ~ 0.91) -> K25
        - 'bệnh bạch hàu' (typo of 'Bệnh bạch hầu', score ~ 0.92) -> A36
        - 'bệnh lỵ amip cấp' (typo of 'Bệnh lỵ amíp cấp', score ~ 0.94) -> A06.0
        
        Boundary negative cases (diseases/modifiers with score < 0.85):
        - 'viêm họng hạt' (score ~ 0.818 vs 'Viêm họng cấp') -> None
        - 'sốt phát ban nhẹ' (score ~ 0.80) -> None
        """
        positive_boundary = [
            ("viêm xoang trán mản", "J01.1"),
            ("sốt xuất huýet dengue", "A97"),
            ("loét dạ day", "K25"),
            ("bệnh bạch hàu", "A36"),
            ("bệnh lỵ amip cấp", "A06.0"),
        ]
        for query, expected_code in positive_boundary:
            res = shared_icd10_normalizer.normalize(query)
            assert res is not None, f"Expected fuzzy match for boundary query '{query}'"
            assert res.code == expected_code, f"Wrong code for '{query}': {res.code} vs {expected_code}"
            assert res.match_method == "fuzzy"
            assert res.match_score >= 0.85, f"Match score {res.match_score} below cutoff 0.85 for '{query}'"

        negative_boundary = [
            "viêm họng hạt",
            "sốt phát ban nhẹ",
        ]
        for query in negative_boundary:
            res = shared_icd10_normalizer.normalize(query)
            assert res is None, f"Expected rejection for below-threshold query '{query}', got {res}"

    def test_fuzzy_matches(self, shared_icd10_normalizer):

        """Verify strict fuzzy matches meeting threshold >= 0.85 and length ratio."""
        fuzzy_cases = [
            ("viêm ruột thừa cấp tính", "K35", "Viêm ruột thừa cấp"),
        ]
        for query, expected_code, expected_label in fuzzy_cases:
            res = shared_icd10_normalizer.normalize(query)
            assert res is not None, f"Failed fuzzy match for: {query}"
            assert res.code == expected_code, f"Wrong code for {query}: {res.code} vs {expected_code}"
            assert res.match_method == "fuzzy"
            assert res.match_score >= 0.85


    def test_strict_unmatched_rejection(self, shared_icd10_normalizer):
        """Unknown or nonsensical condition names must return None without guessing."""
        invalid_queries = [
            "xyz_benh_la_khong_ton_tai",
            "bệnh abc12345",
            "",
            "   ",
        ]
        for query in invalid_queries:
            res = shared_icd10_normalizer.normalize(query)
            assert res is None, f"Expected None for invalid query '{query}', got {res}"



# =====================================================================
# 2. RxNorm Normalizer Tests
# =====================================================================
class TestRxNormNormalizer:
    """Test suite for RxNorm drug normalization with mocked and live API calls."""

    @pytest.fixture
    def mock_session(self):
        """Fixture returning a mock requests Session configured for standard drugs."""
        session = MagicMock(spec=requests.Session)

        drug_db = {
            "paracetamol": ("161", "acetaminophen"),
            "aspirin": ("1191", "aspirin"),
            "amoxicillin": ("723", "amoxicillin"),
            "ibuprofen": ("5640", "ibuprofen"),
            "metformin": ("6809", "metformin"),
        }

        def mock_get(url, params=None, timeout=None):
            resp = MagicMock()
            resp.status_code = 200

            if "rxcui.json" in url:
                name = (params or {}).get("name", "").lower()
                if name in drug_db:
                    rxcui, _ = drug_db[name]
                    resp.json.return_value = {"idGroup": {"name": name, "rxnormId": [rxcui]}}
                else:
                    resp.json.return_value = {"idGroup": {"name": name}}
                return resp

            elif "property.json" in url:
                # URL like .../rxcui/161/property.json
                for drug_name, (rxcui, std_name) in drug_db.items():
                    if f"/{rxcui}/" in url:
                        resp.json.return_value = {
                            "propConceptGroup": {
                                "propConcept": [
                                    {
                                        "propCategory": "NAMES",
                                        "propName": "RxNorm Name",
                                        "propValue": std_name,
                                    }
                                ]
                            }
                        }
                        return resp
                resp.json.return_value = {}
                return resp

            resp.status_code = 404
            return resp

        session.get.side_effect = mock_get
        return session

    def test_mocked_common_drugs(self, mock_session, tmp_path):
        """Verify normalization of 5 standard drugs via mocked API."""
        db_path = tmp_path / "test_rx_cache.db"
        unmatched_log = tmp_path / "test_unmatched.log"

        normalizer = RxNormNormalizer(
            db_path=db_path,
            unmatched_log_path=unmatched_log,
            session=mock_session,
        )

        expected = [
            ("Paracetamol", "161", "acetaminophen"),
            ("Aspirin", "1191", "aspirin"),
            ("Amoxicillin", "723", "amoxicillin"),
            ("Ibuprofen", "5640", "ibuprofen"),
            ("Metformin", "6809", "metformin"),
        ]

        for drug_name, expected_code, expected_label in expected:
            res = normalizer.normalize(drug_name)
            assert res is not None, f"Failed to normalize drug: {drug_name}"
            assert res.ontology == "RxNorm"
            assert res.code == expected_code
            assert res.label_standard.lower() == expected_label.lower()
            assert res.match_method == "api"

    def test_dosage_stripping_and_pure_drug_names(self, mock_session, tmp_path):
        """Verify RxNormNormalizer handles both pure drug names and surface text with dosage attached.
        
        Real NER entities typically extract pure drug names ('Paracetamol'), but sometimes
        surface text accidentally includes strength ('Paracetamol 500mg').
        clean_drug_name() must strip the dosage, resulting in the identical RxNorm resolution.
        """
        db_path = tmp_path / "test_rx_dosage_cache.db"
        normalizer = RxNormNormalizer(db_path=db_path, session=mock_session)

        # 1. Pure drug names (real NER format)
        res_pure = normalizer.normalize("Paracetamol")
        assert res_pure is not None
        assert res_pure.code == "161"

        # 2. Drug name with attached strength/unit
        res_dosage = normalizer.normalize("Paracetamol 500mg")
        assert res_dosage is not None
        assert res_dosage.code == "161"
        assert res_dosage.code == res_pure.code

        # 3. Another pair: Amoxicillin pure vs with unit
        res_amox_pure = normalizer.normalize("Amoxicillin")
        res_amox_dose = normalizer.normalize("Amoxicillin 250 mg")
        assert res_amox_pure is not None and res_amox_dose is not None
        assert res_amox_pure.code == "723"
        assert res_amox_dose.code == "723"


    def test_sqlite_caching(self, mock_session, tmp_path):
        """Verify that repeated queries hit SQLite cache and bypass network calls."""
        db_path = tmp_path / "test_rx_cache.db"
        normalizer = RxNormNormalizer(db_path=db_path, session=mock_session)

        # Call 1: hits mock API
        res1 = normalizer.normalize("Paracetamol")
        assert res1 is not None
        call_count_after_first = mock_session.get.call_count
        assert call_count_after_first > 0

        # Call 2: must hit SQLite cache
        res2 = normalizer.normalize("Paracetamol")
        assert res2 is not None
        assert res2.code == res1.code
        assert mock_session.get.call_count == call_count_after_first, "Cache bypassed unexpectedly!"

    def test_unmatched_drug_logged(self, mock_session, tmp_path):
        """Unmatched drug returns None and appends entry to unmatched_drugs.log."""
        db_path = tmp_path / "test_rx_cache.db"
        unmatched_log = tmp_path / "test_unmatched.log"

        normalizer = RxNormNormalizer(
            db_path=db_path,
            unmatched_log_path=unmatched_log,
            session=mock_session,
        )

        res = normalizer.normalize("Thuoc Nam Gia Truyen Khong Ro Ten")
        assert res is None

        # Verify log file
        assert unmatched_log.exists()
        content = unmatched_log.read_text(encoding="utf-8")
        assert "Thuoc Nam Gia Truyen Khong Ro Ten" in content

    def test_live_rxnav_api(self):
        """Integration test against actual NLM RxNav REST API (live network)."""
        # Test connectivity first
        try:
            probe = requests.get("https://rxnav.nlm.nih.gov/REST/version.json", timeout=3.0)
            if probe.status_code != 200:
                pytest.skip("RxNav API unavailable")
        except Exception:
            pytest.skip("No network access to RxNav API")

        normalizer = RxNormNormalizer()
        res = normalizer.normalize("Aspirin")
        assert res is not None
        assert res.ontology == "RxNorm"
        assert res.code == "1191"



# =====================================================================
# 3. Dispatcher & Pipeline Tests
# =====================================================================
@pytest.fixture(scope="module")
def shared_pipeline():
    """Pipeline fixture with initialized normalizers."""
    return get_default_pipeline()


class TestDispatcher:
    """Test suite for dispatcher routing, safe stubs, and pipeline batch execution."""

    def test_route_condition(self, shared_pipeline):
        """CONDITION entities route to ICD-10."""
        entity = {"surface_text": "đau lưng", "label": "CONDITION"}
        res = shared_pipeline.normalize_entity(entity)
        assert res is not None
        assert res.ontology == "ICD-10"
        assert res.code == "M54"

    def test_route_drug(self, shared_pipeline):
        """DRUG entities route to RxNorm."""
        entity = {"surface_text": "Aspirin", "label": "DRUG"}
        res = shared_pipeline.normalize_entity(entity)
        assert res is not None
        assert res.ontology == "RxNorm"
        assert res.code == "1191"

    def test_safe_body_part_stub(self, shared_pipeline):
        """BODY_PART entities return None safely without raising exceptions."""
        entity = {"surface_text": "phổi", "label": "BODY_PART"}
        res = shared_pipeline.normalize_entity(entity)
        assert res is None

    def test_safe_test_stub(self, shared_pipeline):
        """TEST entities return None safely without raising exceptions."""
        entity = {"surface_text": "xét nghiệm máu", "label": "TEST"}
        res = shared_pipeline.normalize_entity(entity)
        assert res is None

    def test_safe_procedure_stub(self, shared_pipeline):
        """PROCEDURE entities return None safely without raising exceptions."""
        entity = {"surface_text": "nội soi dạ dày", "label": "PROCEDURE"}
        res = shared_pipeline.normalize_entity(entity)
        assert res is None

    def test_safe_dosage_skipped(self, shared_pipeline):
        """DOSAGE entities return None and are skipped cleanly."""
        entity = {"surface_text": "500mg 2 lần/ngày", "label": "DOSAGE"}
        res = shared_pipeline.normalize_entity(entity)
        assert res is None

    def test_batch_normalize_entities(self, shared_pipeline):
        """Verify full entity batch enrichment."""
        entities = [
            {"surface_text": "đau lưng", "label": "CONDITION"},
            {"surface_text": "Aspirin", "label": "DRUG"},
            {"surface_text": "phổi", "label": "BODY_PART"},
            {"surface_text": "chụp X-quang", "label": "TEST"},
            {"surface_text": "phẫu thuật", "label": "PROCEDURE"},
            {"surface_text": "2 viên/ngày", "label": "DOSAGE"},
        ]

        enriched = shared_pipeline.normalize_entities(entities)
        assert len(enriched) == 6

        # CONDITION enriched
        assert enriched[0]["normalized"] is not None
        assert enriched[0]["normalized"]["ontology"] == "ICD-10"
        assert enriched[0]["normalized"]["code"] == "M54"

        # DRUG enriched
        assert enriched[1]["normalized"] is not None
        assert enriched[1]["normalized"]["ontology"] == "RxNorm"
        assert enriched[1]["normalized"]["code"] == "1191"

        # Stubs & skipped remain None
        assert enriched[2]["normalized"] is None
        assert enriched[3]["normalized"] is None
        assert enriched[4]["normalized"] is None
        assert enriched[5]["normalized"] is None

    def test_module_normalize_entity_shortcut(self):
        """Test convenience module-level function `normalize_entity`."""
        res = normalize_entity({"surface_text": "tiểu đường", "label": "CONDITION"})
        assert res is not None
        assert res.ontology == "ICD-10"
        assert res.code == "E14"



# =====================================================================
# 4. Top-k candidate retrieval (used by Top-k Accuracy / Recall@k evaluation)
# =====================================================================
class TestCandidates:
    """`candidates()` puts the system decision first, never repeats a code, respects k."""

    def test_icd10_decision_is_rank_one(self, shared_icd10_normalizer):
        top = shared_icd10_normalizer.normalize("đau bụng")
        cands = shared_icd10_normalizer.candidates("đau bụng", k=5)
        assert cands[0].code == top.code == "R10"
        assert cands[0].match_method != "retrieval"
        assert len(cands) <= 5
        assert len({c.code for c in cands}) == len(cands)

    def test_icd10_candidates_when_normalize_abstains(self, shared_icd10_normalizer):
        # 'rong kinh' has no safe single mapping, but the candidate list still ranks codes.
        assert shared_icd10_normalizer.normalize("rong kinh") is None
        cands = shared_icd10_normalizer.candidates("rong kinh", k=10)
        assert 0 < len(cands) <= 10
        assert all(c.match_method == "retrieval" for c in cands)

    def test_icd10_empty_input(self, shared_icd10_normalizer):
        assert shared_icd10_normalizer.candidates("   ", k=5) == []
        assert shared_icd10_normalizer.candidates("đau bụng", k=0) == []

    def test_rxnorm_candidates_cached_and_deduped(self, tmp_path):
        session = MagicMock(spec=requests.Session)

        def mock_get(url, params=None, timeout=None):
            resp = MagicMock()
            resp.status_code = 200
            if url.endswith("/approximateTerm.json"):
                resp.json.return_value = {"approximateGroup": {"candidate": [
                    {"rxcui": "161", "score": "9.0", "name": "acetaminophen"},
                    {"rxcui": "161", "score": "9.0", "name": "paracetamol"},
                    {"rxcui": "1191", "score": "3.0", "name": "aspirin"},
                ]}}
            elif url.endswith("/rxcui.json"):
                resp.json.return_value = {"idGroup": {}}
            else:
                resp.json.return_value = {}
            return resp

        session.get.side_effect = mock_get
        rx = RxNormNormalizer(db_path=tmp_path / "c.db", unmatched_log_path=tmp_path / "u.log",
                              session=session)
        cands = rx.candidates("paracetamol", k=5)
        assert [c.code for c in cands] == ["161", "1191"]
        calls = session.get.call_count
        assert [c.code for c in rx.candidates("paracetamol", k=1)] == ["161"]
        assert session.get.call_count == calls, "approximateTerm result should come from cache"


# =====================================================================
# 5. Dev-split improvements: Vietnamese drug aliases, prefix strip, guarded approx,
#    ICD-10 lay-term synonyms and the uncovered-word fuzzy safeguard
# =====================================================================
def _rx_session(exact, approx):
    """Mock RxNav: `exact` maps query -> rxcui for /rxcui.json; `approx` maps query -> [(rxcui, name)]."""
    session = MagicMock(spec=requests.Session)

    def mock_get(url, params=None, timeout=None):
        resp = MagicMock()
        resp.status_code = 200
        params = params or {}
        if url.endswith("/rxcui.json"):
            rxcui = exact.get(params.get("name"))
            resp.json.return_value = {"idGroup": {"rxnormId": [rxcui]} if rxcui else {}}
        elif url.endswith("/approximateTerm.json"):
            resp.json.return_value = {"approximateGroup": {"candidate": [
                {"rxcui": c, "name": n, "score": "9"} for c, n in approx.get(params.get("term"), [])]}}
        else:
            resp.json.return_value = {"propConceptGroup": {"propConcept": [{"propValue": "Name"}]}}
        return resp

    session.get.side_effect = mock_get
    return session


class TestDrugAliasesAndApprox:
    def _rx(self, tmp_path, exact=None, approx=None, aliases=None):
        path = tmp_path / "aliases.json"
        path.write_text(json.dumps({"aliases": aliases or {"canxi": "calcium", "đông trùng hạ thảo": "Cordyceps sinensis"}},
                                   ensure_ascii=False), encoding="utf-8")
        return RxNormNormalizer(db_path=tmp_path / "c.db", unmatched_log_path=tmp_path / "u.log",
                                aliases_path=path, session=_rx_session(exact or {}, approx or {}))

    def test_vietnamese_alias(self, tmp_path):
        rx = self._rx(tmp_path, exact={"calcium": "1895"})
        res = rx.normalize("Canxi")
        assert res.code == "1895" and res.match_method == "alias"

    def test_prefix_strip_then_alias(self, tmp_path):
        rx = self._rx(tmp_path, exact={"Cordyceps sinensis": "1427139"})
        assert rx.normalize("viên nang đông trùng hạ thảo").code == "1427139"

    def test_approx_accepts_typo_only(self, tmp_path):
        rx = self._rx(tmp_path, approx={"progesteronee": [("8727", "progesterone")],
                                        "thuốc bổ": [("2690033", "BO-653")]})
        res = rx.normalize("progesteronee")
        assert res.code == "8727" and res.match_method == "approx"
        assert rx.normalize("thuốc bổ") is None, "loose approximate match must be rejected"


class TestIcdDevImprovements:
    def test_lay_term_synonyms(self, shared_icd10_normalizer):
        assert shared_icd10_normalizer.normalize("rung nhĩ").code == "I48"
        assert shared_icd10_normalizer.normalize("loãng xương").code == "M81.9"

    def test_uncovered_word_rejected(self, shared_icd10_normalizer):
        # Candidate 'Rối loạn vận động phân ly' (F44.4) adds 'phân ly', which defines the disease.
        res = shared_icd10_normalizer.normalize("rối loạn vận động")
        assert res is None or res.code != "F44.4"

    def test_acuity_qualifier_still_matches(self, shared_icd10_normalizer):
        assert shared_icd10_normalizer.normalize("nhồi máu cơ tim").code.startswith("I21")

    def test_candidates_use_tfidf_with_aliases(self, shared_icd10_normalizer):
        cands = shared_icd10_normalizer.candidates("rong kinh", k=10)
        assert 0 < len(cands) <= 10 and len({c.code for c in cands}) == len(cands)


class TestAlwaysAnswerMode:
    def test_strict_abstains_always_suggests(self, shared_icd10_normalizer):
        strict = EntityNormalizationPipeline(icd10_normalizer=shared_icd10_normalizer)
        always = EntityNormalizationPipeline(icd10_normalizer=shared_icd10_normalizer, mode="always")
        ent = {"surface_text": "rong kinh", "label": "CONDITION"}
        assert strict.normalize_entity(ent) is None
        res = always.normalize_entity(ent)
        assert res is not None and res.match_method == "retrieval"

    def test_always_keeps_confident_decision(self, shared_icd10_normalizer):
        always = EntityNormalizationPipeline(icd10_normalizer=shared_icd10_normalizer, mode="always")
        res = always.normalize_entity({"surface_text": "đau bụng", "label": "CONDITION"})
        assert res.code == "R10" and res.match_method != "retrieval"

    def test_always_does_not_touch_other_labels(self, shared_icd10_normalizer):
        always = EntityNormalizationPipeline(icd10_normalizer=shared_icd10_normalizer, mode="always")
        assert always.normalize_entity({"surface_text": "500mg", "label": "DOSAGE"}) is None

    def test_invalid_mode(self):
        with pytest.raises(ValueError):
            EntityNormalizationPipeline(mode="sometimes")


class TestTopKOutput:
    def test_entities_carry_ranked_candidates(self, shared_icd10_normalizer):
        pipe = EntityNormalizationPipeline(icd10_normalizer=shared_icd10_normalizer, top_k=3)
        out = pipe.normalize_entities([
            {"surface_text": "đau bụng", "label": "CONDITION"},
            {"surface_text": "rong kinh", "label": "CONDITION"},
            {"surface_text": "500mg", "label": "DOSAGE"},
        ])
        confident, guess, dosage = out
        assert confident["normalized"]["code"] == "R10"
        assert confident["candidates"][0]["code"] == "R10" and confident["candidates"][0]["rank"] == 1
        assert [c["rank"] for c in confident["candidates"]] == list(range(1, len(confident["candidates"]) + 1))
        assert len(confident["candidates"]) <= 3
        # strict mode: no decision, but suggestions are still returned
        assert guess["normalized"] is None
        assert guess["candidates"] and all(c["match_method"] == "retrieval" for c in guess["candidates"])
        assert dosage["normalized"] is None and dosage["candidates"] == []

    def test_decision_matches_single_entity_call(self, shared_icd10_normalizer):
        pipe = EntityNormalizationPipeline(icd10_normalizer=shared_icd10_normalizer)
        for text in ("tiểu đường", "rong kinh", "loãng xương"):
            ent = {"surface_text": text, "label": "CONDITION"}
            single = pipe.normalize_entity(ent)
            batch = pipe.normalize_entities([ent])[0]["normalized"]
            assert (single.to_dict() if single else None) == batch

    def test_top_k_zero_disables_list(self, shared_icd10_normalizer):
        pipe = EntityNormalizationPipeline(icd10_normalizer=shared_icd10_normalizer, top_k=0)
        out = pipe.normalize_entities([{"surface_text": "đau bụng", "label": "CONDITION"}])[0]
        assert out["candidates"] == [] and out["normalized"]["code"] == "R10"
        with pytest.raises(ValueError):
            EntityNormalizationPipeline(top_k=-1)
