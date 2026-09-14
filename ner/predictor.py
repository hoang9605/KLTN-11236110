"""Model predictor and word-level subtoken alignment for Vietnamese Medical NER.

Loads ViHealthBERT checkpoint and performs:
  1. Subtoken encoding with word index mapping.
  2. Forward inference for BIO tag distribution.
  3. Strict removal of special tokens (<s>, </s>, [CLS], [SEP], [PAD]) BEFORE decoding.
  4. Word-level aggregation (first subtoken BIO tag + subtoken confidence averaging).
  5. 37 -> 6 target schema mapping (non-target labels strictly mapped to 'O').
  6. BIO decoding into entity spans with exact document character offsets.
"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer

from .config import (
    MAX_POSITION_EMBEDDINGS,
    SPECIAL_TOKENS,
    VIETMED_TO_TARGET,
    resolve_model_path,
)
from .logger import NERPipelineLogger, get_logger
from .preprocessor import TextChunk, WordToken


@dataclass
class RawEntity:
    """Represents an entity extracted prior to rule-based enhancement."""
    surface_text: str
    label: str
    start_char: int
    end_char: int
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "surface_text": self.surface_text,
            "label": self.label,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "confidence": round(self.confidence, 4),
        }


class ModelNERPredictor:
    """ViHealthBERT NER predictor with subtoken-to-word alignment."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        device: Optional[str] = None,
        logger: Optional[NERPipelineLogger] = None,
    ):
        self.logger = logger or get_logger()
        resolved_path = resolve_model_path(model_path)
        self.logger.info("SYSTEM", f"Loading ViHealthBERT checkpoint from: {resolved_path}")

        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        self.logger.info("SYSTEM", f"Using device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(str(resolved_path), use_fast=False)
        self.model = AutoModelForTokenClassification.from_pretrained(str(resolved_path))
        self.model.to(self.device)
        self.model.eval()

        self.id2label = {int(k): v for k, v in self.model.config.id2label.items()}
        self.label2id = {v: int(k) for k, v in self.model.config.id2label.items()}
        self.logger.info("SYSTEM", f"Loaded model with {len(self.id2label)} classes.")

    def predict_chunk(self, chunk: TextChunk, full_text: str) -> List[RawEntity]:
        """Run token classification on a single chunk and return mapped raw entities."""
        if not chunk.words:
            return []

        # 1. Subtoken encoding and word index mapping
        subtokens: List[str] = []
        subtoken_word_map: List[int] = []

        for word_idx, word in enumerate(chunk.words):
            pieces = self.tokenizer.tokenize(word.text)
            if not pieces:
                pieces = [self.tokenizer.unk_token]
            for p in pieces:
                subtokens.append(p)
                subtoken_word_map.append(word_idx)

        # 2. Add special tokens (<s> and </s>)
        bos_tok = self.tokenizer.bos_token or "<s>"
        eos_tok = self.tokenizer.eos_token or "</s>"
        full_tokens = [bos_tok] + subtokens + [eos_tok]
        full_word_map = [None] + subtoken_word_map + [None]

        # Truncate if chunk exceeds max sequence length
        if len(full_tokens) > MAX_POSITION_EMBEDDINGS:
            self.logger.warning(
                "PREDICT",
                f"Chunk length {len(full_tokens)} exceeds {MAX_POSITION_EMBEDDINGS}. Truncating."
            )
            full_tokens = full_tokens[:MAX_POSITION_EMBEDDINGS - 1] + [eos_tok]
            full_word_map = full_word_map[:MAX_POSITION_EMBEDDINGS - 1] + [None]

        input_ids = self.tokenizer.convert_tokens_to_ids(full_tokens)
        input_tensor = torch.tensor([input_ids], dtype=torch.long, device=self.device)

        # 3. Model forward inference
        with torch.no_grad():
            outputs = self.model(input_tensor)
            logits = outputs.logits[0]
            probs = torch.softmax(logits, dim=-1)
            confidences, pred_ids = torch.max(probs, dim=-1)

        self.logger.debug("PREDICT", f"Inference complete on {len(full_tokens)} subtokens.")

        # 4. Strict removal of special tokens BEFORE decoding
        valid_subtokens: List[Tuple[int, int, float]] = []
        for i, w_idx in enumerate(full_word_map):
            tok_str = full_tokens[i]
            if w_idx is None or tok_str in SPECIAL_TOKENS:
                continue
            pred_id = pred_ids[i].item()
            conf = confidences[i].item()
            valid_subtokens.append((w_idx, pred_id, conf))

        self.logger.debug("ALIGN", f"Discarded special tokens. Remaining valid subtokens: {len(valid_subtokens)}.")

        # 5. Word-level aggregation (first subtoken BIO tag + subtoken confidence averaging)
        word_to_subs: Dict[int, List[Tuple[int, float]]] = {}
        for w_idx, p_id, conf in valid_subtokens:
            word_to_subs.setdefault(w_idx, []).append((p_id, conf))

        aligned_tags: List[str] = []
        aligned_confs: List[float] = []

        for word_idx in range(len(chunk.words)):
            sub_list = word_to_subs.get(word_idx, [])
            if not sub_list:
                aligned_tags.append("O")
                aligned_confs.append(0.0)
                continue

            first_pred_id = sub_list[0][0]
            raw_tag = self.id2label.get(first_pred_id, "O")
            avg_conf = sum(c for _, c in sub_list) / len(sub_list)

            # 6. Apply target schema mapping (non-target mapped to 'O')
            mapped_tag = self._map_tag_to_target(raw_tag)
            aligned_tags.append(mapped_tag)
            aligned_confs.append(avg_conf)

        # 7. Decode word-level BIO tags into entity spans
        return self._decode_bio_spans(chunk.words, aligned_tags, aligned_confs, full_text)

    def _map_tag_to_target(self, raw_tag: str) -> str:
        """Map raw VietMed 37 BIO tag into 6 target categories or 'O'."""
        if raw_tag == "O" or ("-" not in raw_tag):
            return "O"

        prefix, entity_type = raw_tag.split("-", 1)
        if prefix not in ("B", "I"):
            return "O"

        if entity_type in VIETMED_TO_TARGET:
            target_label = VIETMED_TO_TARGET[entity_type]
            return f"{prefix}-{target_label}"
        else:
            return "O"

    def _decode_bio_spans(
        self,
        words: List[WordToken],
        tags: List[str],
        confs: List[float],
        full_text: str,
    ) -> List[RawEntity]:
        """Decode aligned BIO tags into RawEntity spans with full document offsets."""
        entities: List[RawEntity] = []
        curr_label: Optional[str] = None
        curr_start: Optional[int] = None
        curr_end: Optional[int] = None
        curr_confs: List[float] = []

        def flush():
            nonlocal curr_label, curr_start, curr_end, curr_confs
            if curr_label is not None and curr_start is not None and curr_end is not None:
                surface = full_text[curr_start:curr_end]
                mean_conf = sum(curr_confs) / len(curr_confs) if curr_confs else 0.0
                entities.append(
                    RawEntity(
                        surface_text=surface,
                        label=curr_label,
                        start_char=curr_start,
                        end_char=curr_end,
                        confidence=mean_conf,
                    )
                )
                self.logger.debug(
                    "MAP",
                    f"Decoded: [{curr_label}] {surface!r} [{curr_start}:{curr_end}] conf={mean_conf:.4f}"
                )
            curr_label = None
            curr_start = None
            curr_end = None
            curr_confs = []

        for word, tag, conf in zip(words, tags, confs):
            if tag == "O":
                flush()
            elif tag.startswith("B-"):
                flush()
                curr_label = tag[2:]
                curr_start = word.start_char
                curr_end = word.end_char
                curr_confs = [conf]
            elif tag.startswith("I-"):
                lbl = tag[2:]
                if curr_label == lbl:
                    curr_end = word.end_char
                    curr_confs.append(conf)
                else:
                    flush()
                    curr_label = lbl
                    curr_start = word.start_char
                    curr_end = word.end_char
                    curr_confs = [conf]

        flush()
        return entities

