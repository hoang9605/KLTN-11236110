"""RxNorm Normalizer for pharmaceutical drugs using NLM RxNav REST API.

Implements drug entity normalization to RxCUI identifiers with SQLite caching,
exponential backoff retries, and unmatched term logging.
"""

import datetime
import re
import sqlite3
import time
import unicodedata
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import requests

from normalization.base import BaseNormalizer, NormalizedResult
from normalization.logger import log_unmatched_drug

MODULE_ROOT = Path(__file__).resolve().parent
DEFAULT_DB_PATH = MODULE_ROOT / "data" / "rxnorm_cache.db"
DEFAULT_UNMATCHED_LOG = MODULE_ROOT / "data" / "unmatched_drugs.log"
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

    def normalize(self, surface_text: str) -> Optional[NormalizedResult]:
        """Normalize drug surface text into RxNorm concept.

        Args:
            surface_text: Raw drug text extracted from clinical note.

        Returns:
            NormalizedResult if resolved to RxCUI, or None if unmapped.
        """
        clean_name = clean_drug_name(surface_text)
        if not clean_name:
            return None

        # 1. Check local SQLite cache first
        cached = self._get_from_cache(clean_name)
        if cached is not None:
            _, result = cached
            return result

        # 2. Query RxNav API
        rxcui = self._fetch_rxcui(clean_name)

        if rxcui is not None:
            std_name = self._fetch_standard_name(rxcui, fallback_name=surface_text.strip().title())
            result = NormalizedResult(
                ontology="RxNorm",
                code=rxcui,
                label_standard=std_name,
                match_method="api",
                match_score=1.0,
            )
            # Save positive result to cache
            self._save_to_cache(
                query_text=clean_name,
                rxcui=rxcui,
                label_standard=std_name,
                match_method="api",
                match_score=1.0,
            )
            return result

        # 3. Unmatched: cache negative result and log
        self._save_to_cache(
            query_text=clean_name,
            rxcui=None,
            label_standard=None,
            match_method="no_match",
            match_score=0.0,
        )
        log_unmatched_drug(surface_text, self.unmatched_log_path)
        return None

