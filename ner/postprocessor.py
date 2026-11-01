"""Post-processor for Vietnamese Medical NER pipeline.

Responsibilities:
  1. Strict filtering against 6 target categories (CONDITION, DRUG, BODY_PART, TEST, PROCEDURE, DOSAGE).
  2. Rule 1: Generic action blacklist filter for DRUG entities ('chỉ định', 'can thiệp', 'kê đơn', 'điều trị').
  2b. Rule 1b: Lab-test names labeled DRUG ('men tim', 'Troponin T') are relabeled TEST.
  3. Rule 2: Clinical severity adjective merge into immediately preceding CONDITION ('sốt cao' -> CONDITION).
  4. Overlapping span resolution: if two entities overlap in character span,
     the entity with the higher confidence is preserved.
  5. Clean formatting conforming to the specified output schema.
"""
from typing import Any, Dict, List, Optional

from .config import CLINICAL_SEVERITY_ADJECTIVES, DRUG_ACTION_BLACKLIST, LAB_TEST_TERMS, TARGET_LABELS
from .logger import NERPipelineLogger, get_logger
from .predictor import RawEntity


class PostProcessor:
    """Filters, deduplicates, and resolves conflicts in medical NER entities."""

    def __init__(self, logger: Optional[NERPipelineLogger] = None):
        self.logger = logger or get_logger()

    @staticmethod
    def _get_ent_prop(ent: Any, prop: str, default: Any = None) -> Any:
        """Helper to get property from dataclass object or dict."""
        if hasattr(ent, prop):
            return getattr(ent, prop)
        if isinstance(ent, dict):
            return ent.get(prop, default)
        return default

    def filter_schema(self, entities: List[Any]) -> List[Any]:
        """Filter entities against the 6 target categories."""
        valid_entities = []
        for ent in entities:
            lbl = self._get_ent_prop(ent, "label", None)
            if lbl in TARGET_LABELS:
                valid_entities.append(ent)
            else:
                self.logger.warning(
                    "FILTER",
                    f"Discarded non-target entity: {lbl!r} from candidate list."
                )
        return valid_entities

    def filter_drug_blacklist(self, entities: List[Any]) -> List[Any]:
        """Rule 1: Discard DRUG entities matching generic action/indication terms in DRUG_ACTION_BLACKLIST.

        Applies only when the entity's surface_text (case-insensitive, stripped) is an exact match
        for a blacklisted term (standalone), not when it's part of a longer drug name.
        """
        kept_entities = []
        for ent in entities:
            lbl = self._get_ent_prop(ent, "label", "")
            surf = self._get_ent_prop(ent, "surface_text", "")
            s_c = self._get_ent_prop(ent, "start_char", 0)
            e_c = self._get_ent_prop(ent, "end_char", 0)
            conf = float(self._get_ent_prop(ent, "confidence", 0.0))

            surf_clean = surf.strip().lower()
            if lbl == "DRUG" and surf_clean in DRUG_ACTION_BLACKLIST:
                self.logger.log_blacklist_dropped(
                    entity_label=lbl,
                    surface_text=surf,
                    start_char=s_c,
                    end_char=e_c,
                    confidence=conf,
                )
                continue
            kept_entities.append(ent)
        return kept_entities

    def relabel_lab_tests_from_drug(self, entities: List[Any]) -> List[Any]:
        """Rule 1b: Relabel DRUG entities whose surface text is a known lab/diagnostic test as TEST."""
        for ent in entities:
            lbl = self._get_ent_prop(ent, "label", "")
            surf = (self._get_ent_prop(ent, "surface_text", "") or "").strip().lower()
            if lbl == "DRUG" and surf in LAB_TEST_TERMS:
                if isinstance(ent, dict):
                    ent["label"] = "TEST"
                else:
                    ent.label = "TEST"
                self.logger.info("FILTER", f"Relabeled lab test from DRUG to TEST: {surf!r}")
        return entities

    def merge_severity_into_condition(
        self,
        entities: List[Any],
        text: str,
    ) -> List[Any]:
        """Rule 2: Merge clinical severity adjectives labeled as DOSAGE into immediately preceding CONDITION.

        Conditions:
          1. Entity has label == 'DOSAGE' and surface_text (lowercased, stripped) in CLINICAL_SEVERITY_ADJECTIVES.
          2. Entity does not contain digits or measurement units.
          3. Immediately follows a CONDITION entity (adjacent, separated by exactly 1 space:
             dosage.start_char == condition.end_char + 1 and text[condition.end_char:dosage.start_char] == ' ').
        If matched, merges both into 1 CONDITION:
          - surface_text: text[cond.start_char:dosage.end_char]
          - start_char: cond.start_char, end_char: dosage.end_char
          - confidence: average of both entities
        If not preceded by a CONDITION, keeps as DOSAGE (do not merge or drop).
        """
        if not entities:
            return []

        # Sort by start_char ascending, then end_char ascending
        sorted_entities = sorted(
            entities,
            key=lambda e: (
                self._get_ent_prop(e, "start_char", 0),
                self._get_ent_prop(e, "end_char", 0),
            )
        )

        merged_result: List[Any] = []
        for ent in sorted_entities:
            lbl = self._get_ent_prop(ent, "label", "")
            surf = self._get_ent_prop(ent, "surface_text", "")
            s_c = self._get_ent_prop(ent, "start_char", 0)
            e_c = self._get_ent_prop(ent, "end_char", 0)
            conf = float(self._get_ent_prop(ent, "confidence", 0.0))
            surf_clean = surf.strip().lower()

            is_severity_dosage = (
                lbl == "DOSAGE"
                and surf_clean in CLINICAL_SEVERITY_ADJECTIVES
                and not any(c.isdigit() for c in surf_clean)
            )

            if is_severity_dosage and merged_result:
                prev = merged_result[-1]
                prev_lbl = self._get_ent_prop(prev, "label", "")
                prev_s_c = self._get_ent_prop(prev, "start_char", 0)
                prev_e_c = self._get_ent_prop(prev, "end_char", 0)
                prev_conf = float(self._get_ent_prop(prev, "confidence", 0.0))
                prev_surf = self._get_ent_prop(prev, "surface_text", "")

                is_adjacent = (
                    prev_lbl == "CONDITION"
                    and s_c == prev_e_c + 1
                    and 0 <= prev_e_c < len(text)
                    and text[prev_e_c:s_c] == " "
                )

                if is_adjacent:
                    merged_result.pop()
                    merged_text = text[prev_s_c:e_c]
                    merged_conf = round((prev_conf + conf) / 2.0, 4)

                    self.logger.log_severity_merged(
                        cond_text=prev_surf,
                        cond_start=prev_s_c,
                        cond_end=prev_e_c,
                        cond_conf=prev_conf,
                        dos_text=surf,
                        dos_start=s_c,
                        dos_end=e_c,
                        dos_conf=conf,
                        merged_text=merged_text,
                        merged_start=prev_s_c,
                        merged_end=e_c,
                        merged_conf=merged_conf,
                    )

                    if isinstance(prev, dict):
                        merged_ent: Any = {
                            "surface_text": merged_text,
                            "label": "CONDITION",
                            "start_char": prev_s_c,
                            "end_char": e_c,
                            "confidence": merged_conf,
                        }
                    else:
                        merged_ent = RawEntity(
                            surface_text=merged_text,
                            label="CONDITION",
                            start_char=prev_s_c,
                            end_char=e_c,
                            confidence=merged_conf,
                        )
                    merged_result.append(merged_ent)
                    continue

            # Default: keep entity as-is
            merged_result.append(ent)

        return merged_result


    def filter_and_resolve_overlaps(
        self,
        entities: List[Any],
        text: str,
    ) -> List[Dict[str, Any]]:
        """Filter schema, apply Rule 1 (blacklist DRUG) & Rule 2 (merge severity),

        resolve character span overlaps by confidence, and return entities sorted by start_char.
        Pipeline order: filter schema -> blacklist DRUG -> merge severity -> resolve overlap.
        """
        if not entities:
            return []

        # 1. Filter against the 6 target labels
        valid_entities = self.filter_schema(entities)
        if not valid_entities:
            return []

        # 2. Rule 1: Discard generic action terms from DRUG
        entities_after_blacklist = self.filter_drug_blacklist(valid_entities)
        if not entities_after_blacklist:
            return []

        # 2b. Rule 1b: Relabel lab-test names from DRUG to TEST
        entities_after_blacklist = self.relabel_lab_tests_from_drug(entities_after_blacklist)

        # 3. Rule 2: Merge severity adjectives into preceding CONDITION
        entities_after_merge = self.merge_severity_into_condition(entities_after_blacklist, text)
        if not entities_after_merge:
            return []

        # 4. Sort candidates by confidence descending, then span length descending
        def get_conf(e: Any) -> float:
            return float(self._get_ent_prop(e, "confidence", 0.0))

        def get_span(e: Any) -> tuple:
            return self._get_ent_prop(e, "start_char", 0), self._get_ent_prop(e, "end_char", 0)

        sorted_candidates = sorted(
            entities_after_merge,
            key=lambda e: (
                get_conf(e),
                get_span(e)[1] - get_span(e)[0],  # span length
                -get_span(e)[0],  # earlier start
            ),
            reverse=True,
        )

        accepted_spans: List[tuple] = []
        accepted_entities: List[Any] = []

        # 5. Greedy non-overlapping span selection
        for cand in sorted_candidates:
            c_start, c_end = get_span(cand)
            # Check overlap with already accepted entities
            overlaps = False
            for a_start, a_end in accepted_spans:
                if max(c_start, a_start) < min(c_end, a_end):
                    overlaps = True
                    break

            if not overlaps:
                accepted_spans.append((c_start, c_end))
                accepted_entities.append(cand)
            else:
                lbl = self._get_ent_prop(cand, "label", "")
                surf = self._get_ent_prop(cand, "surface_text", "")
                self.logger.info(
                    "FILTER",
                    f"Resolved overlap: dropped lower-confidence entity [{lbl}] {surf!r} [{c_start}:{c_end}] (conf={get_conf(cand):.4f})"
                )

        # 6. Sort accepted entities by start_char ascending
        accepted_entities.sort(key=lambda e: get_span(e)[0])

        # 7. Format to target output schema
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
