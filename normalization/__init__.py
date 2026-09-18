"""Medical Entity Normalization Module for Vietnamese Clinical NLP Pipeline.

Provides normalization from extracted NER entities to standard ontologies:
- CONDITION -> ICD-10 (Ministry of Health catalog)
- DRUG -> RxNorm (NLM RxNav REST API)
- BODY_PART, TEST, PROCEDURE -> Prepared interfaces for FMA / LOINC / MeSH
- DOSAGE -> Passthrough / Skipped
"""

from normalization.base import BaseNormalizer, NormalizedResult
from normalization.dispatcher import (
    EntityNormalizationPipeline,
    get_default_pipeline,
    normalize_entity,
)
from normalization.icd10 import ICD10Normalizer
from normalization.logger import log_normalization, log_unmatched_drug
from normalization.rxnorm import RxNormNormalizer
from normalization.stubs import FMANormalizer, LOINCNormalizer, MeSHNormalizer

__all__ = [
    "BaseNormalizer",
    "NormalizedResult",
    "ICD10Normalizer",
    "RxNormNormalizer",
    "FMANormalizer",
    "LOINCNormalizer",
    "MeSHNormalizer",
    "EntityNormalizationPipeline",
    "get_default_pipeline",
    "normalize_entity",
    "log_normalization",
    "log_unmatched_drug",
]
