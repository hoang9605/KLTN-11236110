"""ICD-10 Normalizer for Vietnamese medical conditions.

Implements standard ICD-10 terminology resolution for entity label `CONDITION`
using official Ministry of Health (Vietnam) ICD-10 catalog with exact matching,
synonym dictionary rules, and strict rapidfuzz token-set matching.
"""

import json
import os
import pickle
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from rapidfuzz import fuzz, process

from normalization.base import BaseNormalizer, NormalizedResult

MODULE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = MODULE_ROOT.parent

DEFAULT_CATALOG_EXCEL = PROJECT_ROOT / "ICD-10" / "phu-lu-c-1-danh-mu-c-icd-10-thay-the-dmdc-phie-n-ba-n-6.xlsx"
DEFAULT_CACHE_PATH = MODULE_ROOT / "data" / "icd10_cache.pkl"
DEFAULT_SYNONYMS_PATH = MODULE_ROOT / "data" / "icd10_synonyms.json"
# Catalog words that do not change which disease a name denotes (function words, ICD qualifiers).
FUZZY_FILLER_WORDS = frozenset(
    "bệnh lý chứng của và do ở các những trong không xác định đặc hiệu khác chưa phân loại nơi"
    " cấp mạn mãn tính nguyên phát vô căn".split()
)


def normalize_vietnamese_text(text: str) -> str:
    """Normalize text for consistent string matching."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", str(text)).strip().lower()
    text = re.sub(r"[,\.;:\-\(\)\[\]/\"\'\?\!\*]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _strip_accents(word: str) -> str:
    """Remove Vietnamese diacritics ('huyết' -> 'huyet') for typo-tolerant word comparison."""
    decomposed = unicodedata.normalize("NFD", word.replace("đ", "d"))
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


class ICD10Normalizer(BaseNormalizer):
    """Normalizes medical conditions to ICD-10 codes."""

    def __init__(
        self,
        catalog_path: Optional[Path] = None,
        cache_path: Optional[Path] = None,
        synonyms_path: Optional[Path] = None,
        fuzz_threshold: float = 0.85,
        min_length_ratio: float = 0.60,
    ) -> None:
        self.catalog_path = Path(catalog_path) if catalog_path else DEFAULT_CATALOG_EXCEL
        self.cache_path = Path(cache_path) if cache_path else DEFAULT_CACHE_PATH
        self.synonyms_path = Path(synonyms_path) if synonyms_path else DEFAULT_SYNONYMS_PATH
        self.fuzz_threshold = fuzz_threshold
        self.min_length_ratio = min_length_ratio

        if not self.catalog_path.exists():
            raise FileNotFoundError(
                f"ICD-10 catalog file not found at: {self.catalog_path}."
            )

        self.exact_map: Dict[str, Dict[str, str]] = {}
        self.code_map: Dict[str, Dict[str, str]] = {}
        self.catalog_names: List[str] = []
        self.catalog_entries: List[Dict[str, str]] = []

        self._load_catalog()
        self._load_synonyms()

    def _load_catalog(self) -> None:
        """Load ICD-10 catalog from pickle cache or compile from Excel if stale."""
        source_mtime = os.path.getmtime(self.catalog_path)

        if self.cache_path.exists():
            try:
                with open(self.cache_path, "rb") as f:
                    cache_data = pickle.load(f)
                if cache_data.get("source_mtime") == source_mtime:
                    self.exact_map = cache_data["exact_map"]
                    self.code_map = cache_data["code_map"]
                    self.catalog_names = cache_data["catalog_names"]
                    self.catalog_entries = cache_data["catalog_entries"]
                    return
            except Exception:
                pass

        df = pd.read_excel(
            str(self.catalog_path),
            sheet_name="ICD10",
            skiprows=2,
            usecols=["MÃ BỆNH", "TÊN BỆNH"],
        )
        df = df.dropna(subset=["MÃ BỆNH", "TÊN BỆNH"])

        exact_map: Dict[str, Dict[str, str]] = {}
        code_map: Dict[str, Dict[str, str]] = {}
        catalog_names: List[str] = []
        catalog_entries: List[Dict[str, str]] = []

        for _, row in df.iterrows():
            raw_code = str(row["MÃ BỆNH"]).strip()
            raw_name = str(row["TÊN BỆNH"]).strip()
            clean_name = normalize_vietnamese_text(raw_name)

            if not raw_code or not clean_name:
                continue

            entry = {
                "code": raw_code,
                "name": raw_name,
                "clean_name": clean_name,
            }

            if clean_name not in exact_map:
                exact_map[clean_name] = entry
                catalog_names.append(clean_name)
                catalog_entries.append(entry)

            if raw_code not in code_map:
                code_map[raw_code] = entry

        self.exact_map = exact_map
        self.code_map = code_map
        self.catalog_names = catalog_names
        self.catalog_entries = catalog_entries

        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.cache_path, "wb") as f:
                pickle.dump(
                    {
                        "source_mtime": source_mtime,
                        "exact_map": self.exact_map,
                        "code_map": self.code_map,
                        "catalog_names": self.catalog_names,
                        "catalog_entries": self.catalog_entries,
                    },
                    f,
                    protocol=pickle.HIGHEST_PROTOCOL,
                )
        except Exception:
            pass

    def _load_synonyms(self) -> None:
        """Load synonym mappings and regex patterns from JSON."""
        self.direct_aliases: Dict[str, Dict[str, Any]] = {}
        self.synonym_patterns: List[Tuple[re.Pattern, str, str]] = []

        if not self.synonyms_path.exists():
            return

        try:
            with open(self.synonyms_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            aliases = data.get("direct_aliases", {})
            for alias, val in aliases.items():
                clean_alias = normalize_vietnamese_text(alias)
                self.direct_aliases[clean_alias] = val

            for item in data.get("patterns", []):
                pattern_str = item.get("pattern", "")
                target_tmpl = item.get("target_template", "")
                fallback_tmpl = item.get("fallback_template", "")
                if pattern_str and target_tmpl:
                    compiled = re.compile(pattern_str, re.IGNORECASE)
                    self.synonym_patterns.append((compiled, target_tmpl, fallback_tmpl))
        except Exception:
            pass

    def normalize(self, surface_text: str) -> Optional[NormalizedResult]:
        """Normalize clinical condition text to ICD-10 code.

        Resolution steps:
        1. Exact match against catalog disease names.
        2. Exact match through synonym dictionary / patterns.
        3. Strict fuzzy match (threshold >= 0.85, length ratio >= min_length_ratio).
        4. Return None if no criteria met.
        """
        clean_text = normalize_vietnamese_text(surface_text)
        if not clean_text:
            return None

        # 1. Exact match
        if clean_text in self.exact_map:
            entry = self.exact_map[clean_text]
            return NormalizedResult(
                ontology="ICD-10",
                code=entry["code"],
                label_standard=entry["name"],
                match_method="exact",
                match_score=1.0,
            )

        # 2. Synonym match
        # (a) Direct aliases
        if clean_text in self.direct_aliases:
            alias_info = self.direct_aliases[clean_text]
            target_code = alias_info.get("code")
            pref_name = alias_info.get("preferred_name")
            if target_code and target_code in self.code_map:
                catalog_entry = self.code_map[target_code]
                return NormalizedResult(
                    ontology="ICD-10",
                    code=target_code,
                    label_standard=pref_name or catalog_entry["name"],
                    match_method="synonym",
                    match_score=1.0,
                )
            elif target_code:
                return NormalizedResult(
                    ontology="ICD-10",
                    code=target_code,
                    label_standard=pref_name or surface_text,
                    match_method="synonym",
                    match_score=1.0,
                )

        # (b) Regex patterns (e.g. 'ung thư X' -> 'u ác của X')
        for pattern, target_tmpl, fallback_tmpl in self.synonym_patterns:
            match = pattern.match(clean_text)
            if match:
                groups = match.groupdict()
                transformed = target_tmpl.format(**groups)
                clean_tf = normalize_vietnamese_text(transformed)

                if clean_tf in self.exact_map:
                    entry = self.exact_map[clean_tf]
                    return NormalizedResult(
                        ontology="ICD-10",
                        code=entry["code"],
                        label_standard=entry["name"],
                        match_method="synonym",
                        match_score=1.0,
                    )

                # Check organ cancer entry match (e.g., 'u ác của ...' containing organ)
                organ = groups.get("organ", "")
                if organ:
                    clean_organ = normalize_vietnamese_text(organ)
                    for c_name, entry in self.exact_map.items():
                        if c_name.startswith("u ac cua ") or c_name.startswith("u ác của "):
                            c_words = c_name.split()
                            if clean_organ in c_words:
                                return NormalizedResult(
                                    ontology="ICD-10",
                                    code=entry["code"],
                                    label_standard=entry["name"],
                                    match_method="synonym",
                                    match_score=0.95,
                                )

                fuzzy_res = self._fuzzy_search(clean_tf)
                if fuzzy_res is not None:
                    code, standard_label, score = fuzzy_res
                    return NormalizedResult(
                        ontology="ICD-10",
                        code=code,
                        label_standard=standard_label,
                        match_method="synonym",
                        match_score=score,
                    )

                if fallback_tmpl:
                    clean_fb = normalize_vietnamese_text(fallback_tmpl.format(**groups))
                    if clean_fb in self.exact_map:
                        entry = self.exact_map[clean_fb]
                        return NormalizedResult(
                            ontology="ICD-10",
                            code=entry["code"],
                            label_standard=entry["name"],
                            match_method="synonym",
                            match_score=1.0,
                        )

        # 3. Strict fuzzy match
        fuzzy_res = self._fuzzy_search(clean_text)
        if fuzzy_res is not None:
            code, standard_label, score = fuzzy_res
            return NormalizedResult(
                ontology="ICD-10",
                code=code,
                label_standard=standard_label,
                match_method="fuzzy",
                match_score=score,
            )

        # 4. Strict no-guess fallback
        return None

    def _retrieval_index(self):
        """Lazily built TF-IDF index (character 2-4-grams within words) over catalog names
        plus synonym-dictionary aliases. Chosen on the dev split over rapidfuzz WRatio,
        token_set_ratio and word n-grams (retrieval-only Top-10 0.64 vs 0.35 for WRatio)."""
        if getattr(self, "_tfidf", None) is None:
            from sklearn.feature_extraction.text import TfidfVectorizer

            texts = list(self.catalog_names)
            entries = list(self.catalog_entries)
            for alias, info in self.direct_aliases.items():
                code = info.get("code")
                if code in self.code_map:
                    texts.append(alias)
                    entries.append(self.code_map[code])
            vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), sublinear_tf=True)
            self._tfidf = (vec, vec.fit_transform(texts), entries)
        return self._tfidf

    def candidates(self, surface_text: str, k: int = 10) -> List[NormalizedResult]:
        """Ranked ICD-10 candidates: the `normalize` decision first (if any), then
        catalog names ranked by TF-IDF character n-gram cosine similarity, without the
        precision safeguards. One entry per code."""
        clean_text = normalize_vietnamese_text(surface_text)
        if not clean_text or k <= 0:
            return []
        out: List[NormalizedResult] = []
        seen = set()
        top = self.normalize(surface_text)
        if top is not None:
            out.append(top)
            seen.add(top.code)
        vec, matrix, entries = self._retrieval_index()
        scores = (matrix @ vec.transform([clean_text]).T).toarray().ravel()
        for index in scores.argsort()[::-1][: k * 4]:
            if len(out) >= k or scores[index] <= 0:
                break
            entry = entries[index]
            if entry["code"] in seen:
                continue
            seen.add(entry["code"])
            out.append(NormalizedResult(
                ontology="ICD-10",
                code=entry["code"],
                label_standard=entry["name"],
                match_method="retrieval",
                match_score=float(scores[index]),
            ))
        return out[:k]

    def _fuzzy_search(self, clean_text: str) -> Optional[Tuple[str, str, float]]:
        """Perform rapidfuzz token_set_ratio matching with safety validations."""
        cutoff = self.fuzz_threshold * 100.0

        best_res = process.extractOne(
            clean_text,
            self.catalog_names,
            scorer=fuzz.token_set_ratio,
            score_cutoff=cutoff,
        )

        if not best_res:
            return None

        best_cand_name, score_100, index = best_res
        score = score_100 / 100.0

        # Validate length ratio
        len1 = len(clean_text)
        len2 = len(best_cand_name)
        len_ratio = min(len1, len2) / max(len1, len2) if max(len1, len2) > 0 else 0.0

        if len_ratio < self.min_length_ratio:
            return None

        # Safeguard: prevent cross-symptom false matches (e.g. 'đau bụng' vs 'đau lưng')
        query_tokens = set(clean_text.split())
        cand_tokens = set(best_cand_name.split())
        if len(query_tokens) <= 3 and len(cand_tokens) <= 3:
            jaccard = len(query_tokens & cand_tokens) / len(query_tokens | cand_tokens)
            if jaccard < 0.40:
                return None

        # Safeguard: the candidate's head word must occur in the query. token_set_ratio scores
        # 100 whenever one token set contains the other, so 'huyết áp cao' matched 'đo huyết áp'
        # (Z01.3) and 'đa xơ cứng' matched 'gan xơ cứng' (K74.1). Vietnamese disease names
        # put the head first; leading generic words are skipped. ratio >= 80 tolerates typos.
        cand_words = best_cand_name.split()
        while cand_words and cand_words[0] in ("bệnh", "lý", "chứng"):
            cand_words = cand_words[1:]
        if cand_words and not any(fuzz.ratio(cand_words[0], q) >= 80 for q in clean_text.split()):
            return None

        # Safeguard: when one name is a strict token subset of the other and the shorter one
        # has at most two tokens, the extra tokens decide the disease ('nhồi máu' vs 'nhồi máu
        # lách' D73.5, 'đậu mùa bò' vs 'đậu mùa' B03). Reject instead of guessing.
        shorter = min(query_tokens, cand_tokens, key=len)
        longer = max(query_tokens, cand_tokens, key=len)
        if shorter < longer and len(shorter) <= 2:
            return None

        # Safeguard: every content word of the candidate must appear in the query (ratio >= 80
        # tolerates typos). A differing word is usually what defines the disease: 'rối loạn vận
        # động' vs 'rối loạn vận động phân ly' (F44.4), 'viêm thần kinh tọa' vs 'viêm thần
        # kinh thị' (H46). Function words and ICD qualifiers ('không xác định') are ignored;
        # comparison ignores diacritics so tone typos ('huýet' for 'huyết') still match.
        query_plain = [_strip_accents(q) for q in query_tokens]
        for word in cand_tokens - FUZZY_FILLER_WORDS:
            plain = _strip_accents(word)
            if not any(fuzz.ratio(plain, q) >= 80 for q in query_plain):
                return None

        # Safeguard: prevent qualifier-only false matches (e.g. 'không xác định', 'không đặc hiệu')
        qualifiers = ["không xác định", "không đặc hiệu", "chưa phân loại", "nơi khác", "bệnh"]
        q_core = clean_text
        c_core = best_cand_name
        for qf in qualifiers:
            q_core = q_core.replace(qf, "")
            c_core = c_core.replace(qf, "")
        q_core = q_core.strip()
        c_core = c_core.strip()
        if q_core and c_core:
            core_score = fuzz.token_set_ratio(q_core, c_core)
            if core_score < cutoff:
                return None

        entry = self.catalog_entries[index]
        return entry["code"], entry["name"], score

