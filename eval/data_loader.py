"""Dataset loader and preprocessing utilities for VietMed-NER evaluation."""

import os
import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


from typing import Dict, List, Optional, Tuple, Any
from datasets import Dataset, DatasetDict, load_dataset, get_dataset_split_names

from ner.config import TARGET_LABELS, VIETMED_TO_TARGET

DATASET_NAME = "leduckhai/VietMed-NER"


def check_and_get_splits() -> List[str]:
    """Retrieve available split names for the dataset."""
    splits = get_dataset_split_names(DATASET_NAME)
    return list(splits)


def load_vietmed_test_split(split: str = "test") -> Dataset:
    """Load official VietMed-NER test split, removing audio to avoid decoding issues."""
    splits = check_and_get_splits()
    if split not in splits:
        raise ValueError(
            f"Requested split '{split}' not found in dataset splits: {splits}. "
            f"Stopping to avoid data leakage."
        )

    ds = load_dataset(DATASET_NAME, split=split)
    if "audio" in ds.column_names:
        ds = ds.remove_columns(["audio"])
    return ds


def normalize_bio_tag(tag: str) -> str:
    """Normalize outside tag '0' (digit zero) to 'O' (letter O)."""
    if tag == "0" or tag == 0:
        return "O"
    return str(tag).strip()


def map_raw_bio_to_target(tag: str) -> str:
    """Map a 37-class VietMed BIO tag to 6-class target BIO tag or 'O'."""
    tag = normalize_bio_tag(tag)
    if tag == "O" or "-" not in tag:
        return "O"

    prefix, entity_type = tag.split("-", 1)
    if prefix not in ("B", "I"):
        return "O"

    if entity_type in VIETMED_TO_TARGET:
        target_entity = VIETMED_TO_TARGET[entity_type]
        return f"{prefix}-{target_entity}"
    return "O"


def compute_word_char_spans(words: List[str], text: str) -> List[Tuple[int, int]]:
    """Compute (start_char, end_char) for each word in text.
    
    Handles standard single-space joined words and provides fallback for minor deviations.
    """
    spans: List[Tuple[int, int]] = []
    curr_idx = 0
    for w in words:
        found_idx = text.find(w, curr_idx)
        if found_idx != -1:
            start = found_idx
            end = start + len(w)
            spans.append((start, end))
            curr_idx = end
        else:
            # Fallback if text differs slightly
            start = curr_idx
            end = curr_idx + len(w)
            spans.append((start, end))
            curr_idx = end + 1
    return spans


def extract_gold_spans_target_schema(
    words: List[str],
    labels: List[str],
    text: str,
) -> List[Dict[str, Any]]:
    """Extract gold entity spans mapped to the 6 target categories.
    
    Non-target categories (AGE, GENDER, OCCUPATION, etc.) are excluded from gold set.
    """
    word_spans = compute_word_char_spans(words, text)
    entities: List[Dict[str, Any]] = []

    current_entity: Optional[Dict[str, Any]] = None

    for i, (word, raw_tag) in enumerate(zip(words, labels)):
        target_tag = map_raw_bio_to_target(raw_tag)
        w_start, w_end = word_spans[i]

        if target_tag == "O":
            if current_entity is not None:
                entities.append(current_entity)
                current_entity = None
            continue

        prefix, entity_type = target_tag.split("-", 1)

        if prefix == "B":
            if current_entity is not None:
                entities.append(current_entity)
            current_entity = {
                "label": entity_type,
                "start_char": w_start,
                "end_char": w_end,
                "surface_text": text[w_start:w_end],
            }
        elif prefix == "I":
            if current_entity is not None and current_entity["label"] == entity_type:
                current_entity["end_char"] = w_end
                current_entity["surface_text"] = text[current_entity["start_char"]:w_end]
            else:
                # Malformed I- tag without preceding B-: start new entity
                if current_entity is not None:
                    entities.append(current_entity)
                current_entity = {
                    "label": entity_type,
                    "start_char": w_start,
                    "end_char": w_end,
                    "surface_text": text[w_start:w_end],
                }

    if current_entity is not None:
        entities.append(current_entity)

    return entities
