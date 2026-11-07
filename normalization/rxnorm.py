"""RxNorm Normalizer for pharmaceutical drugs using NLM RxNav REST API.

Implements drug entity normalization to RxCUI identifiers with SQLite caching,
exponential backoff retries, and unmatched term logging.
"""

import datetime
from dataclasses import replace
import json
import re
import sqlite3
import time
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from rapidfuzz import fuzz

from normalization.base import BaseNormalizer, NormalizedResult
from normalization.logger import log_unmatched_drug

MODULE_ROOT = Path(__file__).resolve().parent
DEFAULT_DB_PATH = MODULE_ROOT / "data" / "rxnorm_cache.db"
DEFAULT_UNMATCHED_LOG = MODULE_ROOT / "data" / "unmatched_drugs.log"
DEFAULT_ALIASES_PATH = MODULE_ROOT / "data" / "rxnorm_vi_aliases.json"
# Leading words that name a container, dosage form or herbal unit, not the ingredient.
DRUG_PREFIXES = ("viên nang", "viên uống", "viên", "chai", "thuốc", "hoạt chất", "chế phẩm",
                 "hoocmon", "hormone", "quả thể nấm", "nấm", "men", "vị", "lá")
RXNAV_BASE_URL = "https://rxnav.nlm.nih.gov/REST"


def clean_drug_name(text: str) -> str:
    """Normalize drug query name for RxNav API query."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", str(text)).strip().lower()
    # Remove dosage / strength if accidentally attached to drug surface text
    # e.g., 'paracetamol 500mg' -> 'paracetamol'
    text = re.sub(r"\s+\d+(\.\d+)?\s*(mg|g|ml|mcg|iu|%)\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[,\.;:\-\(\)\[\]/\"\'\?\!\*]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class RxNormNormalizer(BaseNormalizer):
    """Normalizes medication names to RxNorm identifiers (RxCUI).

    Resolution features:
    - Direct local SQLite cache lookup before any HTTP call.
    - RxNav REST API query (/REST/rxcui.json and /REST/rxcui/{id}/property.json).
    - Up to 3 retries with exponential backoff on network errors or HTTP timeouts.
    - Caching of both positive hits and negative results to avoid redundant API hits.
    - Logging of unmatched drugs into `normalization/data/unmatched_drugs.log`.
    """

    def __init__(
        self,
        db_path: Optional[Path] = None,
        unmatched_log_path: Optional[Path] = None,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        session: Optional[requests.Session] = None,
        aliases_path: Optional[Path] = None,
        approx_min_ratio: float = 90.0,
    ) -> None:
        """Initialize RxNorm normalizer.

        Args:
            db_path: Path to SQLite cache database.
            unmatched_log_path: Path to unmatched drugs log file.
            timeout: HTTP request timeout in seconds.
            max_retries: Maximum retry attempts for transient API failures.
            backoff_factor: Multiplier for exponential sleep between retries.
            session: Optional pre-configured requests Session (useful for mocking).
        """
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.unmatched_log_path = (
            Path(unmatched_log_path) if unmatched_log_path else DEFAULT_UNMATCHED_LOG
        )
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = session or requests.Session()
        self.approx_min_ratio = approx_min_ratio
        self.aliases: Dict[str, str] = {}
        path = Path(aliases_path) if aliases_path else DEFAULT_ALIASES_PATH
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            self.aliases = {clean_drug_name(k): v for k, v in raw.get("aliases", {}).items()}

        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite cache schema."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(str(self.db_path), timeout=10.0) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rxnorm_cache (
                    query_text TEXT PRIMARY KEY,
                    rxcui TEXT,
                    label_standard TEXT,
                    match_method TEXT,
                    match_score REAL,
                    created_at TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rxnorm_candidates_cache (
                    query_text TEXT PRIMARY KEY,
                    candidates_json TEXT,
                    created_at TEXT
                )
                """
            )
            conn.commit()


    def _get_from_cache(self, query_text: str) -> Optional[Tuple[bool, Optional[NormalizedResult]]]:
        """Look up query text in local SQLite cache.

        Returns:
            Tuple (is_cached: bool, result: Optional[NormalizedResult]) or None if not cached.
        """
        with sqlite3.connect(str(self.db_path), timeout=10.0) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT rxcui, label_standard, match_method, match_score FROM rxnorm_cache WHERE query_text = ?",
                (query_text,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            rxcui, label_standard, match_method, match_score = row
            if rxcui is None:
                # Cached negative hit (previously queried and not found)
                return True, None

            return True, NormalizedResult(
                ontology="RxNorm",
                code=str(rxcui),
                label_standard=str(label_standard),
                match_method=str(match_method),
                match_score=float(match_score),
            )

    def _save_to_cache(
        self,
        query_text: str,
        rxcui: Optional[str],
        label_standard: Optional[str],
        match_method: str,
        match_score: float,
    ) -> None:
        """Store lookup result (positive or negative) into SQLite cache."""
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(str(self.db_path), timeout=10.0) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO rxnorm_cache
                (query_text, rxcui, label_standard, match_method, match_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (query_text, rxcui, label_standard, match_method, match_score, now_str),
            )
            conn.commit()

    def _call_api_with_retry(self, url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Perform HTTP GET request with retries and exponential backoff."""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
            except (requests.RequestException, requests.Timeout):
                if attempt < self.max_retries - 1:
                    sleep_time = self.backoff_factor * (2**attempt)
                    time.sleep(sleep_time)
                else:
                    return None
        return None

    def _fetch_rxcui(self, name: str) -> Optional[str]:
        """Query RxNav endpoint to obtain RxCUI identifier."""
        url = f"{RXNAV_BASE_URL}/rxcui.json"
        data = self._call_api_with_retry(url, {"name": name})
        if not data:
            return None

        id_group = data.get("idGroup", {})
        rxnorm_ids = id_group.get("rxnormId", [])
        if rxnorm_ids and len(rxnorm_ids) > 0:
            return str(rxnorm_ids[0])
        return None

    def _fetch_standard_name(self, rxcui: str, fallback_name: str) -> str:
        """Query official RxNorm concept preferred name."""
        url = f"{RXNAV_BASE_URL}/rxcui/{rxcui}/property.json"
        data = self._call_api_with_retry(url, {"propName": "RxNorm Name"})
        if not data:
            return fallback_name

        try:
            concept_group = data.get("propConceptGroup", {})
            concepts = concept_group.get("propConcept", [])
            if concepts and len(concepts) > 0:
                prop_val = concepts[0].get("propValue")
                if prop_val:
                    return str(prop_val)
        except Exception:
            pass

        return fallback_name

    def _queries(self, clean_name: str) -> List[Tuple[str, str]]:
        """Ordered RxNav queries for a cleaned name, with the method that produced each.

        1. the name itself; 2. its Vietnamese->English alias (canxi -> calcium);
        3. the name without a leading container/class word ('viên nang', 'thuốc', 'vị'...)
        and that remainder's alias."""
        out: List[Tuple[str, str]] = []

        def add(q: str, method: str) -> None:
            if q and q not in [x for x, _ in out]:
                out.append((q, method))

        add(clean_name, "api")
        add(self.aliases.get(clean_name, ""), "alias")
        rest = clean_name
        for prefix in DRUG_PREFIXES:
            if rest.startswith(prefix + " ") and len(rest) > len(prefix) + 1:
                rest = rest[len(prefix) + 1:]
                break
        if rest != clean_name:
            add(self.aliases.get(rest, ""), "alias")
            add(rest, "prefix_strip")
        return out

    def _lookup_exact(self, query: str, surface_text: str) -> Optional[NormalizedResult]:
        """Exact RxNav name lookup for one query, through the SQLite cache (hits and misses)."""
        cached = self._get_from_cache(query)
        if cached is not None:
            return cached[1]
        rxcui = self._fetch_rxcui(query)
        if rxcui is None:
            self._save_to_cache(query_text=query, rxcui=None, label_standard=None,
                                match_method="no_match", match_score=0.0)
            return None
        std_name = self._fetch_standard_name(rxcui, fallback_name=surface_text.strip().title())
        self._save_to_cache(query_text=query, rxcui=rxcui, label_standard=std_name,
                            match_method="api", match_score=1.0)
        return NormalizedResult(ontology="RxNorm", code=rxcui, label_standard=std_name,
                                match_method="api", match_score=1.0)

    def normalize(self, surface_text: str) -> Optional[NormalizedResult]:
        """Normalize drug surface text into an RxNorm concept (RxCUI).

        Resolution order (first hit wins):
        1. exact RxNav lookup of the name, then of its Vietnamese->English alias, then of
           the name without a leading container word ('viên nang đông trùng hạ thảo');
        2. spelling-tolerant match: RxNav approximateTerm top-1, accepted only if its
           name is near-identical to the query (rapidfuzz ratio >= approx_min_ratio),
           which catches typos ('progesteronee') but not loose matches.
        Returns None (and logs the term) when nothing qualifies.
        """
        clean_name = clean_drug_name(surface_text)
        if not clean_name:
            return None
        queries = self._queries(clean_name)
        for query, method in queries:
            res = self._lookup_exact(query, surface_text)
            if res is not None:
                return replace(res, match_method=method) if method != "api" else res
        for query, _ in queries:
            for cand in self._approximate(query)[:1]:
                name = clean_drug_name(cand["name"])
                if name and fuzz.ratio(query, name) >= self.approx_min_ratio:
                    return NormalizedResult(ontology="RxNorm", code=cand["rxcui"],
                                            label_standard=cand["name"], match_method="approx",
                                            match_score=fuzz.ratio(query, name) / 100.0)
        log_unmatched_drug(surface_text, self.unmatched_log_path)
        return None

    def _approximate(self, clean_name: str) -> List[Dict[str, Any]]:
        """RxNav /approximateTerm ranked candidates [{rxcui, name, score}], cached in SQLite.
        A network failure returns [] and is not cached."""
        with sqlite3.connect(str(self.db_path), timeout=10.0) as conn:
            row = conn.execute(
                "SELECT candidates_json FROM rxnorm_candidates_cache WHERE query_text = ?",
                (clean_name,),
            ).fetchone()
        if row is not None:
            return json.loads(row[0])

        data = self._call_api_with_retry(
            f"{RXNAV_BASE_URL}/approximateTerm.json", {"term": clean_name, "maxEntries": 10}
        )
        if data is None:
            return []
        cands: List[Dict[str, Any]] = []
        seen = set()
        for c in (data.get("approximateGroup") or {}).get("candidate") or []:
            rxcui = str(c.get("rxcui") or "")
            if not rxcui or rxcui in seen:
                continue
            seen.add(rxcui)
            cands.append({"rxcui": rxcui, "name": c.get("name") or "",
                          "score": float(c.get("score") or 0.0)})
        for c in cands:
            if not c["name"]:
                c["name"] = self._fetch_standard_name(c["rxcui"], fallback_name="")
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(str(self.db_path), timeout=10.0) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO rxnorm_candidates_cache VALUES (?, ?, ?)",
                (clean_name, json.dumps(cands, ensure_ascii=False), now_str),
            )
            conn.commit()
        return cands

    def candidates(self, surface_text: str, k: int = 10) -> List[NormalizedResult]:
        """Ranked RxNorm candidates: the `normalize` decision first (if any), then
        RxNav approximate-match results. One entry per RxCUI."""
        clean_name = clean_drug_name(surface_text)
        if not clean_name or k <= 0:
            return []
        out: List[NormalizedResult] = []
        top = self.normalize(surface_text)
        if top is not None:
            out.append(top)
        seen = {r.code for r in out}
        for c in self._approximate(clean_name):
            if len(out) >= k:
                break
            if c["rxcui"] in seen:
                continue
            seen.add(c["rxcui"])
            out.append(NormalizedResult(
                ontology="RxNorm",
                code=c["rxcui"],
                label_standard=c["name"],
                match_method="retrieval",
                match_score=c["score"],
            ))
        return out[:k]
