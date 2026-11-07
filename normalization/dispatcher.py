"""Dispatcher and pipeline orchestrator for entity normalization.

Routes entities from MedicalNERPipeline to their respective target ontology
normalizers (ICD-10 for CONDITION, RxNorm for DRUG), safely stubs out
unimplemented ontologies (BODY_PART, TEST, PROCEDURE), skips DOSAGE,
and records structured daily audit logs.
"""

import time
from typing import Any, Dict, List, Optional, Tuple

from normalization.base import NormalizedResult
from normalization.icd10 import ICD10Normalizer
from normalization.logger import log_normalization
from normalization.rxnorm import RxNormNormalizer
from normalization.stubs import FMANormalizer, LOINCNormalizer, MeSHNormalizer


NORMALIZATION_MODES = ("strict", "always")
DEFAULT_TOP_K = 5


class EntityNormalizationPipeline:
    """Orchestrates normalization across medical entities."""

    def __init__(
        self,
        icd10_normalizer: Optional[ICD10Normalizer] = None,
        rxnorm_normalizer: Optional[RxNormNormalizer] = None,
        mode: str = "strict",
        top_k: int = DEFAULT_TOP_K,
    ) -> None:
        """Initialize pipeline with required normalizers.

        Args:
            mode: "strict" (default) abstains when no confident match exists;
                "always" falls back to the top-ranked retrieval candidate, whose
                match_method is "retrieval" so callers can show it as a suggestion.
            top_k: number of ranked candidates `normalize_entities` attaches to each
                CONDITION/DRUG entity as "candidates" (0 disables the list).
        """
        if top_k < 0:
            raise ValueError(f"top_k must be >= 0, got {top_k}")
        self.top_k = top_k
        if mode not in NORMALIZATION_MODES:
            raise ValueError(f"mode must be one of {NORMALIZATION_MODES}, got {mode!r}")
        self.mode = mode
        self._icd10 = icd10_normalizer
        self._rxnorm = rxnorm_normalizer
        self.fma_stub = FMANormalizer()
        self.loinc_stub = LOINCNormalizer()
        self.mesh_stub = MeSHNormalizer()

    @property
    def icd10(self) -> ICD10Normalizer:
        """Lazy-loaded ICD-10 normalizer instance."""
        if self._icd10 is None:
            self._icd10 = ICD10Normalizer()
        return self._icd10

    @property
    def rxnorm(self) -> RxNormNormalizer:
        """Lazy-loaded RxNorm normalizer instance."""
        if self._rxnorm is None:
            self._rxnorm = RxNormNormalizer()
        return self._rxnorm

    def _decide(
        self, normalizer: Any, surface_text: str, top_k: int
    ) -> Tuple[Optional[NormalizedResult], List[NormalizedResult]]:
        """Decision plus ranked candidates. The candidate list starts with the confident
        match when there is one, so the decision is read off it without a second lookup:
        strict mode takes rank 1 only if it is not a "retrieval" guess, always mode takes it."""
        k = max(top_k, 1 if self.mode == "always" else 0)
        if k == 0:
            return normalizer.normalize(surface_text), []
        cands = normalizer.candidates(surface_text, k=k)
        if cands and (self.mode == "always" or cands[0].match_method != "retrieval"):
            decision = cands[0]
        else:
            decision = None
        return decision, cands[:top_k]

    def normalize_entity(self, entity: Dict[str, Any]) -> Optional[NormalizedResult]:
        """Dispatch and normalize a single medical entity.

        Args:
            entity: Entity dict with 'surface_text', 'label', etc.

        Returns:
            NormalizedResult or None.
        """
        return self._resolve(entity, top_k=0)[0]

    def _resolve(
        self, entity: Dict[str, Any], top_k: int
    ) -> Tuple[Optional[NormalizedResult], List[NormalizedResult]]:
        """Normalize one entity; returns (decision, top-k candidates) and logs the decision."""
        t0 = time.perf_counter()
        surface_text = entity.get("surface_text", "")
        label = str(entity.get("label", "")).upper()
        result: Optional[NormalizedResult] = None
        cands: List[NormalizedResult] = []
        method = "unknown_label"

        try:
            if label in ("CONDITION", "DRUG"):
                normalizer = self.icd10 if label == "CONDITION" else self.rxnorm
                result, cands = self._decide(normalizer, surface_text, top_k)
                method = result.match_method if result else "no_match"

            elif label == "BODY_PART":
                result = self.fma_stub.normalize(surface_text)
                method = "not_implemented"

            elif label == "TEST":
                result = self.loinc_stub.normalize(surface_text)
                method = "not_implemented"

            elif label == "PROCEDURE":
                result = self.mesh_stub.normalize(surface_text)
                method = "not_implemented"

            elif label == "DOSAGE":
                # Structured dosage has separate schema from NER, skip ontology normalization
                result = None
                method = "skipped"

            else:
                result = None
                method = "unknown_label"

            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            log_normalization(
                entity=entity,
                result=result,
                match_method=method,
                elapsed_ms=elapsed_ms,
            )
            return result, cands

        except Exception as e:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            log_normalization(
                entity=entity,
                result=None,
                match_method="error",
                elapsed_ms=elapsed_ms,
                exc=e,
            )
            return None, []

    def normalize_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize a collection of entities, attaching 'normalized' metadata.

        Each entity gets "normalized" (the decision, or None) and "candidates": up to
        `top_k` ranked concepts, each with a 1-based "rank" (empty for labels without an
        ontology). Candidates with match_method "retrieval" are suggestions to confirm.

        Args:
            entities: List of entity dicts from MedicalNERPipeline.

        Returns:
            List of updated entity dicts.
        """
        results: List[Dict[str, Any]] = []
        for ent in entities:
            ent_copy = dict(ent)
            norm_res, cands = self._resolve(ent_copy, top_k=self.top_k)
            ent_copy["normalized"] = norm_res.to_dict() if norm_res else None
            ent_copy["candidates"] = [{"rank": i, **c.to_dict()} for i, c in enumerate(cands, 1)]
            results.append(ent_copy)
        return results


# Default singleton instance
_default_pipeline: Optional[EntityNormalizationPipeline] = None


def get_default_pipeline() -> EntityNormalizationPipeline:
    """Get or create singleton EntityNormalizationPipeline."""
    global _default_pipeline
    if _default_pipeline is None:
        _default_pipeline = EntityNormalizationPipeline()
    return _default_pipeline


def normalize_entity(entity: Dict[str, Any]) -> Optional[NormalizedResult]:
    """Top-level dispatcher function to normalize an entity dictionary.

    Args:
        entity: Entity dict with 'surface_text', 'label', etc.

    Returns:
        NormalizedResult or None.
    """
    return get_default_pipeline().normalize_entity(entity)
