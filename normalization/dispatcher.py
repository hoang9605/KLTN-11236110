"""Dispatcher and pipeline orchestrator for entity normalization.

Routes entities from MedicalNERPipeline to their respective target ontology
normalizers (ICD-10 for CONDITION, RxNorm for DRUG), safely stubs out
unimplemented ontologies (BODY_PART, TEST, PROCEDURE), skips DOSAGE,
and records structured daily audit logs.
"""

import time
from typing import Any, Dict, List, Optional

from normalization.base import NormalizedResult
from normalization.icd10 import ICD10Normalizer
from normalization.logger import log_normalization
from normalization.rxnorm import RxNormNormalizer
from normalization.stubs import FMANormalizer, LOINCNormalizer, MeSHNormalizer


class EntityNormalizationPipeline:
    """Orchestrates normalization across medical entities."""

    def __init__(
        self,
        icd10_normalizer: Optional[ICD10Normalizer] = None,
        rxnorm_normalizer: Optional[RxNormNormalizer] = None,
    ) -> None:
        """Initialize pipeline with required normalizers."""
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

    def normalize_entity(self, entity: Dict[str, Any]) -> Optional[NormalizedResult]:
        """Dispatch and normalize a single medical entity.

        Args:
            entity: Entity dict with 'surface_text', 'label', etc.

        Returns:
            NormalizedResult or None.
        """
        t0 = time.perf_counter()
        surface_text = entity.get("surface_text", "")
        label = str(entity.get("label", "")).upper()
        result: Optional[NormalizedResult] = None
        method = "unknown_label"

        try:
            if label == "CONDITION":
                result = self.icd10.normalize(surface_text)
                method = result.match_method if result else "no_match"

            elif label == "DRUG":
                result = self.rxnorm.normalize(surface_text)
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
            return result

        except Exception as e:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            log_normalization(
                entity=entity,
                result=None,
                match_method="error",
                elapsed_ms=elapsed_ms,
                exc=e,
            )
            return None

    def normalize_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize a collection of entities, attaching 'normalized' metadata.

        Args:
            entities: List of entity dicts from MedicalNERPipeline.

        Returns:
            List of updated entity dicts.
        """
        results: List[Dict[str, Any]] = []
        for ent in entities:
            ent_copy = dict(ent)
            norm_res = self.normalize_entity(ent_copy)
            ent_copy["normalized"] = norm_res.to_dict() if norm_res else None
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
