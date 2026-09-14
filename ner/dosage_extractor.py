"""Rule-based Dosage extraction and enhancement for Vietnamese Medical NER.

Responsibilities:
  1. Detect dosage expressions using clinical regex patterns:
     - Numerical quantity / strength / concentration (e.g. 500mg, 0.5ml, 1000 IU, 1-2 viên)
     - Packaging / administration units (viên, gói, ống, giọt, chai, lọ, nhát)
     - Frequency / schedule (lần/ngày, 2 viên/ngày, ngày 2 lần, cách 8 giờ)
  2. Merge fragmented model UNITCALIBRATOR tokens (e.g. missing number '500' before 'mg').
  3. Combine composite dosages into 1 unified entity: {value, unit, frequency}.
  4. Preserve raw text if decomposition is not applicable.
"""
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .logger import NERPipelineLogger, get_logger
from .predictor import RawEntity


@dataclass
class DosageEntity:
    """Represents a finalized DOSAGE entity with optional structured breakdown."""
    surface_text: str
    label: str  # Always "DOSAGE"
    start_char: int
    end_char: int
    confidence: float
    value: Optional[str] = None
    unit: Optional[str] = None
    frequency: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "surface_text": self.surface_text,
            "label": "DOSAGE",
            "start_char": self.start_char,
            "end_char": self.end_char,
            "confidence": round(self.confidence, 4),
        }
        if self.value is not None or self.unit is not None or self.frequency is not None:
            data["dosage_details"] = {
                "value": self.value,
                "unit": self.unit,
                "frequency": self.frequency,
            }
            # Also provide top-level accessors for convenience
            data["value"] = self.value
            data["unit"] = self.unit
            data["frequency"] = self.frequency
        return data


class DosageExtractor:
    """Rule-based dosage extractor and merger for Vietnamese medical text."""

    # Value patterns: integers, decimals, fractions, ranges
    NUM_VAL = r"(?:\d+(?:[.,]\d+)?(?:\s*[-/–—]\s*\d+(?:[.,]\d+)?)?|nửa|một|hai|ba)"

    # Strength & Volume units
    STRENGTH_UNITS = (
        r"(?:mg/ml|mg/5ml|mcg/ml|g/l|UI/ml|IU/ml|"
        r"mg|mcg|microgram|ug|kg|gram|g|"
        r"ml|lit|lít|cc|l|"
        r"UI|IU|dv|đơn vị|%)"
    )

    # Pharmaceutical form / package units
    FORM_UNITS = (
        r"(?:viên|v|ống|gói|chai|lọ|nhát|giọt|nang|bình|túi|amp|tab|cap|ống tiêm|bơm tiêm)"
    )

    # Frequency expressions
    FREQ_PATTERN = (
        r"(?:"
        r"/\s*(?:ngày|ng|đêm|tuần|tháng|h|giờ|tiếng)|"
        r"(?:x\s*)?\d+(?:[.,]\d+)?\s*lần\s*/\s*(?:ngày|ng|đêm|tuần|tháng|h|giờ|tiếng)|"
        r"(?:x\s*)?\d+(?:[.,]\d+)?\s*(?:viên|ống|gói|giọt|ml|mg)\s*/\s*(?:ngày|ng|đêm|tuần|tháng|h|giờ|tiếng)|"
        r"(?:viên|ống|gói|giọt|ml|mg)\s*/\s*(?:ngày|ng|đêm|tuần|tháng|h|giờ|tiếng)|"
        r"lần\s*/\s*(?:ngày|ng|đêm|tuần|tháng|h|giờ|tiếng)|"
        r"(?:ngày|mỗi ngày)\s+\d+(?:[.,]\d+)?\s*lần|"
        r"\d+(?:[.,]\d+)?\s*lần\s+(?:mỗi\s+ngày|ngày)|"
        r"sáng\s+\d+.*tối\s+\d+|"
        r"cách\s+\d+\s*(?:giờ|h|tiếng)"
        r")"
    )

    def __init__(self, logger: Optional[NERPipelineLogger] = None):
        self.logger = logger or get_logger()
        self._build_regexes()

    def _build_regexes(self) -> None:
        """Compile regexes for dosage patterns."""
        # 1. Full composite: <num> <strength_unit> + optional <num> <form_unit> + optional <freq>
        # e.g., "500mg 2 viên/ngày", "500 mg x 2 lần/ngày", "500mg 1 viên"
        self.composite_pattern = re.compile(
            rf"\b(?P<val1>{self.NUM_VAL})\s*(?P<unit1>{self.STRENGTH_UNITS})\b"
            rf"(?:[,\s]+(?P<val2>{self.NUM_VAL})\s*(?P<unit2>{self.FORM_UNITS})\b)?"
            rf"(?:(?:[,\s]*|/)(?P<freq>{self.FREQ_PATTERN}))?",
            re.IGNORECASE,
        )

        # 2. Form + Frequency: "2 viên/ngày", "1 gói x 2 lần/ngày", "2 viên mỗi ngày"
        self.form_freq_pattern = re.compile(
            rf"\b(?P<val>{self.NUM_VAL})\s*(?P<unit>{self.FORM_UNITS})\b"
            rf"(?:(?:[,\s]*|/)(?P<freq>{self.FREQ_PATTERN}))?",
            re.IGNORECASE,
        )

        # 3. Standalone frequency: "3 lần/ngày", "ngày 2 lần"
        self.standalone_freq_pattern = re.compile(
            rf"\b(?P<freq>{self.FREQ_PATTERN})\b",
            re.IGNORECASE,
        )

        # 4. Standalone strength: "500mg", "10 ml", "1000 IU"
        self.standalone_strength_pattern = re.compile(
            rf"\b(?P<val>{self.NUM_VAL})\s*(?P<unit>{self.STRENGTH_UNITS})\b",
            re.IGNORECASE,
        )

    def extract_regex_dosages(self, text: str) -> List[DosageEntity]:
        """Extract all candidate dosage entities using clinical regex rules."""
        dosages: List[DosageEntity] = []
        if not text:
            return dosages

        occupied_spans: List[Tuple[int, int]] = []

        def span_overlaps(s: int, e: int) -> bool:
            return any(max(s, os) < min(e, oe) for os, oe in occupied_spans)

        # Pass 1: Composite patterns (e.g., "500mg 2 viên/ngày")
        for m in self.composite_pattern.finditer(text):
            s, e = m.start(), m.end()
            if span_overlaps(s, e):
                continue
            surface = text[s:e].strip()
            v1 = m.group("val1")
            u1 = m.group("unit1")
            v2 = m.group("val2")
            u2 = m.group("unit2")
            freq = m.group("freq")

            # Format structured value/unit/frequency
            if v2 and u2:
                if freq and freq.startswith("/"):
                    freq_str = f"{v2} {u2}{freq}".strip()
                elif freq:
                    freq_str = f"{v2} {u2} {freq}".strip()
                else:
                    freq_str = f"{v2} {u2}".strip()
                val_str = v1
                unit_str = u1
            else:
                val_str = v1
                unit_str = u1
                freq_str = freq

            dosages.append(
                DosageEntity(
                    surface_text=surface,
                    label="DOSAGE",
                    start_char=s,
                    end_char=e,
                    confidence=0.98,
                    value=val_str,
                    unit=unit_str,
                    frequency=freq_str,
                )
            )
            occupied_spans.append((s, e))

        # Pass 2: Form + Frequency (e.g., "2 viên/ngày")
        for m in self.form_freq_pattern.finditer(text):
            s, e = m.start(), m.end()
            if span_overlaps(s, e):
                continue
            surface = text[s:e].strip()
            val = m.group("val")
            unit = m.group("unit")
            raw_freq = m.group("freq")
            if raw_freq and raw_freq.startswith("/"):
                freq_str = f"{val} {unit}{raw_freq}".strip()
            else:
                freq_str = raw_freq

            dosages.append(
                DosageEntity(
                    surface_text=surface,
                    label="DOSAGE",
                    start_char=s,
                    end_char=e,
                    confidence=0.98,
                    value=val,
                    unit=unit,
                    frequency=freq_str,
                )
            )
            occupied_spans.append((s, e))

        # Pass 3: Standalone Frequency (e.g., "3 lần/ngày")
        for m in self.standalone_freq_pattern.finditer(text):
            s, e = m.start(), m.end()
            if span_overlaps(s, e):
                continue
            surface = text[s:e].strip()
            val, unit, freq = self._parse_dosage_components(surface)
            dosages.append(
                DosageEntity(
                    surface_text=surface,
                    label="DOSAGE",
                    start_char=s,
                    end_char=e,
                    confidence=0.98,
                    value=val,
                    unit=unit,
                    frequency=freq or surface,
                )
            )
            occupied_spans.append((s, e))

        self.logger.debug(
            "DOSAGE_RULE",
            f"Regex extracted {len(dosages)} candidate dosage entities."
        )
        return dosages

    def _parse_dosage_components(
        self, text: str
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Decompose dosage text into {value, unit, frequency} components if possible."""
        cleaned = text.strip()

        # Match composite
        m_comp = self.composite_pattern.search(cleaned)
        if m_comp:
            v1 = m_comp.group("val1")
            u1 = m_comp.group("unit1")
            v2 = m_comp.group("val2")
            u2 = m_comp.group("unit2")
            freq = m_comp.group("freq")
            if v2 and u2:
                if freq and freq.startswith("/"):
                    freq_str = f"{v2} {u2}{freq}".strip()
                elif freq:
                    freq_str = f"{v2} {u2} {freq}".strip()
                else:
                    freq_str = f"{v2} {u2}".strip()
                return v1, u1, freq_str
            return v1, u1, freq

        # Match form + freq
        m_ff = self.form_freq_pattern.search(cleaned)
        if m_ff:
            val = m_ff.group("val")
            unit = m_ff.group("unit")
            raw_freq = m_ff.group("freq")
            if raw_freq and raw_freq.startswith("/"):
                freq_str = f"{val} {unit}{raw_freq}".strip()
            else:
                freq_str = raw_freq
            return val, unit, freq_str

        # Match standalone strength
        m_str = self.standalone_strength_pattern.search(cleaned)
        if m_str:
            return m_str.group("val"), m_str.group("unit"), None

        # Match frequency pattern e.g., "3 lần/ngày"
        m_times = re.search(r"(\d+)\s*lần\s*/\s*(\w+)", cleaned, re.IGNORECASE)
        if m_times:
            return m_times.group(1), "lần", m_times.group(2)

        # Fallback: cannot decompose cleanly
        return None, None, None

    def merge_with_model_entities(
        self,
        model_entities: List[RawEntity],
        full_text: str,
    ) -> List[Any]:
        """Merge rule-based DOSAGE extractions with model-predicted entities.

        - If rule-based dosage overlaps with a model DOSAGE (UNITCALIBRATOR) entity,
          replaces it with the complete merged DOSAGE entity.
        - If model missed a dosage (e.g., '500mg', '2 viên/ngày'), adds rule entity.
        - If model predicted DOSAGE not matched by regex, parses components or keeps raw.
        """
        regex_dosages = self.extract_regex_dosages(full_text)
        merged_entities: List[Any] = []

        # Separate model entities
        other_entities: List[RawEntity] = []
        model_dosages: List[RawEntity] = []

        for ent in model_entities:
            if ent.label == "DOSAGE":
                model_dosages.append(ent)
            else:
                other_entities.append(ent)

        # Track which model dosage entities got absorbed by rule-based spans
        absorbed_model_dosage_indices = set()

        for r_dose in regex_dosages:
            # Check if this regex dosage overlaps or abuts with any model DOSAGE entity
            matching_model_confs: List[float] = []
            for idx, m_dose in enumerate(model_dosages):
                # Check overlap or adjacency (within 2 chars)
                if (max(r_dose.start_char, m_dose.start_char) < min(r_dose.end_char, m_dose.end_char)) or \
                   (abs(r_dose.start_char - m_dose.end_char) <= 1) or \
                   (abs(m_dose.start_char - r_dose.end_char) <= 1):
                    absorbed_model_dosage_indices.add(idx)
                    matching_model_confs.append(m_dose.confidence)

            # Inherit model confidence if available
            if matching_model_confs:
                r_dose.confidence = max(max(matching_model_confs), r_dose.confidence)

            merged_entities.append(r_dose)
            self.logger.info(
                "DOSAGE_RULE",
                f"Merged DOSAGE: {r_dose.surface_text!r} [{r_dose.start_char}:{r_dose.end_char}] "
                f"value={r_dose.value!r}, unit={r_dose.unit!r}, freq={r_dose.frequency!r}"
            )

        # Retain any model DOSAGE entity that was NOT covered by regex rules
        for idx, m_dose in enumerate(model_dosages):
            if idx not in absorbed_model_dosage_indices:
                val, unit, freq = self._parse_dosage_components(m_dose.surface_text)
                merged_entities.append(
                    DosageEntity(
                        surface_text=m_dose.surface_text,
                        label="DOSAGE",
                        start_char=m_dose.start_char,
                        end_char=m_dose.end_char,
                        confidence=m_dose.confidence,
                        value=val,
                        unit=unit,
                        frequency=freq,
                    )
                )

        # Add all other model entities (CONDITION, DRUG, BODY_PART, TEST, PROCEDURE)
        merged_entities.extend(other_entities)
        return merged_entities


