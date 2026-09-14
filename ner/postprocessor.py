"""Post-processor for Vietnamese Medical NER pipeline.

Responsibilities:
  1. Strict filtering against 6 target categories (CONDITION, DRUG, BODY_PART, TEST, PROCEDURE, DOSAGE).
  2. Overlapping span resolution: if two entities overlap in character span,
     the entity with the higher confidence is preserved.
  3. Clean formatting conforming to the specified output schema.
"""
from typing import Any, Dict, List

from .config import TARGET_LABELS
from .logger import NERPipelineLogger, get_logger


class PostProcessor:
    """Filters, deduplicates, and resolves conflicts in medical NER entities."""

    def __init__(self, logger: NERPipelineLogger = None):
        self.logger = logger or get_logger()

    def filter_and_resolve_overlaps(
        self,
        entities: List[Any],
        text: str,
    ) -> List[Dict[str, Any]]:
        """Filter non-target labels, resolve character span overlaps by confidence,

        and return entities sorted by start_char.
        """
        if not entities:
            return []

        # 1. Filter against the 6 target labels
        valid_entities = []
        for ent in entities:
            lbl = getattr(ent, "label", None) or (ent.get("label") if isinstance(ent, dict) else None)
            if lbl in TARGET_LABELS:
                valid_entities.append(ent)
            else:
                self.logger.warning(
                    "FILTER",
                    f"Discarded non-target entity: {lbl!r} from candidate list."
                )

        if not valid_entities:
            return []

        # 2. Sort by confidence descending, then span length descending
        def get_conf(e: Any) -> float:
            if hasattr(e, "confidence"):
                return float(e.confidence)
            return float(e.get("confidence", 0.0))

        def get_span(e: Any) -> tuple:
            if hasattr(e, "start_char") and hasattr(e, "end_char"):
                return e.start_char, e.end_char
            return e.get("start_char", 0), e.get("end_char", 0)

        # Sort candidates
        sorted_candidates = sorted(
            valid_entities,
            key=lambda e: (
                get_conf(e),
                get_span(e)[1] - get_span(e)[0],  # span length
                -get_span(e)[0],  # earlier start
            ),
            reverse=True,
        )

        accepted_spans: List[tuple] = []
        accepted_entities: List[Any] = []

        # 3. Greedy non-overlapping span selection
        for cand in sorted_candidates:
            c_start, c_end = get_span(cand)
            # Check overlap with already accepted entities
            # Two spans overlap if max(c_start, a_start) < min(c_end, a_end)
            overlaps = False
            for a_start, a_end in accepted_spans:
                if max(c_start, a_start) < min(c_end, a_end):
                    overlaps = True
                    break

            if not overlaps:
                accepted_spans.append((c_start, c_end))
                accepted_entities.append(cand)
            else:
                lbl = getattr(cand, "label", "") or (cand.get("label", "") if isinstance(cand, dict) else "")
                surf = getattr(cand, "surface_text", "") or (cand.get("surface_text", "") if isinstance(cand, dict) else "")
                self.logger.info(
                    "FILTER",
                    f"Resolved overlap: dropped lower-confidence entity [{lbl}] {surf!r} [{c_start}:{c_end}] (conf={get_conf(cand):.4f})"
                )

        # 4. Sort accepted entities by start_char ascending
        accepted_entities.sort(key=lambda e: get_span(e)[0])

        # 5. Format to target output schema
        final_list: List[Dict[str, Any]] = []
        for ent in accepted_entities:
            if hasattr(ent, "to_dict"):
                d = ent.to_dict()
            elif isinstance(ent, dict):
                d = dict(ent)
            else:
                d = {
                    "surface_text": ent.surface_text,
                    "label": ent.label,
                    "start_char": ent.start_char,
                    "end_char": ent.end_char,
                    "confidence": round(float(ent.confidence), 4),
                }

            # Verify and clean whitespace at boundaries if needed
            s_c = d["start_char"]
            e_c = d["end_char"]
            actual_text = text[s_c:e_c]
            # Ensure surface_text matches text[s_c:e_c]
            d["surface_text"] = actual_text
            final_list.append(d)

        self.logger.info("FILTER", f"Final entities after filtering and deduplication: {len(final_list)}.")
        return final_list
