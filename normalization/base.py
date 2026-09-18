"""Base classes and data contracts for Medical Entity Normalization.

This module defines the unified interface and result structure for all
ontology normalizers in the Vietnamese clinical NLP pipeline.
"""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class NormalizedResult:
    """Standardized representation of a normalized medical entity.

    Attributes:
        ontology: Target terminology/ontology system (e.g., 'ICD-10', 'RxNorm').
        code: Concept identifier within the ontology (e.g., 'R10', '161').
        label_standard: Canonical/preferred concept name.
        match_method: Strategy used to resolve entity ('exact', 'synonym',
            'fuzzy', 'api', 'cache', 'not_implemented', 'skipped').
        match_score: Confidence score of normalization (0.0 to 1.0).
    """

    ontology: str
    code: str
    label_standard: str
    match_method: str
    match_score: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert result dataclass to dictionary."""
        return asdict(self)


class BaseNormalizer(ABC):
    """Abstract base class for all medical ontology normalizers.

    Subclasses must implement `normalize` accepting a surface text string
    and returning an optional `NormalizedResult`.
    """

    @abstractmethod
    def normalize(self, surface_text: str) -> Optional[NormalizedResult]:
        """Normalize raw entity text into target ontology standard concept.

        Args:
            surface_text: Raw entity text extracted from medical text.

        Returns:
            NormalizedResult if successfully normalized, or None if unmapped.
        """
        raise NotImplementedError
