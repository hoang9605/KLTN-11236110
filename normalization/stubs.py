"""Stub normalizers for future ontology integrations.

These stub classes prepare the architecture for FMA (BODY_PART), LOINC (TEST),
and MeSH (PROCEDURE) without implementing external logic. They return None
safely without throwing exceptions.
"""

from typing import Optional

from normalization.base import BaseNormalizer, NormalizedResult


class FMANormalizer(BaseNormalizer):
    """Stub normalizer for anatomical entities (BODY_PART) targeting FMA ontology."""

    ontology: str = "FMA"

    def normalize(self, surface_text: str) -> Optional[NormalizedResult]:
        """Return None as FMA ontology resolution is out of scope."""
        return None


class LOINCNormalizer(BaseNormalizer):
    """Stub normalizer for diagnostic tests (TEST) targeting LOINC ontology."""

    ontology: str = "LOINC"

    def normalize(self, surface_text: str) -> Optional[NormalizedResult]:
        """Return None as LOINC ontology resolution is out of scope."""
        return None


class MeSHNormalizer(BaseNormalizer):
    """Stub normalizer for medical procedures (PROCEDURE) targeting MeSH ontology."""

    ontology: str = "MeSH"

    def normalize(self, surface_text: str) -> Optional[NormalizedResult]:
        """Return None as MeSH ontology resolution is out of scope."""
        return None
