"""Main unified Medical NER Pipeline combining ViHealthBERT model and rule-based logic.

Pipeline workflow:
  1. Preprocessing: whitespace normalization, tokenization via regex, sentence chunking.
  2. Model Inference: subtoken classification on ViHealthBERT, special token removal,
     word-level aggregation, 37 -> 6 target schema mapping.
  3. Rule-based Dosage Enhancement: clinical regex extraction for dosage expressions
     (value, unit, frequency) and merging with model UNITCALIBRATOR entities.
  4. Post-processing: strict label validation and greedy confidence-based span overlap resolution.
  5. Edge-case Handling: empty strings, no entities, long documents.
"""
import sys
import traceback
from typing import Any, Dict, List, Optional

from .config import resolve_model_path
from .dosage_extractor import DosageExtractor
from .logger import NERPipelineLogger, get_logger
from .postprocessor import PostProcessor
from .predictor import ModelNERPredictor
from .preprocessor import TextPreprocessor


class MedicalNERPipeline:
    """Production-grade Vietnamese Medical NER Pipeline."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        device: Optional[str] = None,
        log_path: Optional[str] = None,
        enable_console_logging: bool = False,
    ):
        self.logger = get_logger(log_path=log_path, enable_console=enable_console_logging)
        self.logger.info("SYSTEM", "Initializing Vietnamese Medical NER Pipeline...")

        try:
            self.preprocessor = TextPreprocessor(logger=self.logger)
            self.predictor = ModelNERPredictor(model_path=model_path, device=device, logger=self.logger)
            self.dosage_extractor = DosageExtractor(logger=self.logger)
            self.postprocessor = PostProcessor(logger=self.logger)
            self.logger.info("SYSTEM", "Medical NER Pipeline successfully initialized.")
        except Exception as e:
            self.logger.error("SYSTEM", "Failed to initialize Medical NER Pipeline", exc=e)
            raise

    def predict(self, text: str) -> Dict[str, Any]:
        """Extract medical entities from Vietnamese clinical text.

        Conforms strictly to the 6 target categories:
          - CONDITION
          - DRUG
          - BODY_PART
          - TEST
          - PROCEDURE
          - DOSAGE

        Returns:
            {
                "text": "...",
                "entities": [
                    {
                        "surface_text": "...",
                        "label": "CONDITION",
                        "start_char": 0,
                        "end_char": 9,
                        "confidence": 0.99
                    }
                ]
            }
        """
        # Edge Case 1: None or empty text
        if text is None or not text.strip():
            self.logger.info("PREPROCESS", "Empty or whitespace-only input received. Returning empty entities.")
            return {"text": text or "", "entities": []}

        try:
            # Step 1: Preprocessing & Normalization
            normalized_text = self.preprocessor.normalize_whitespace(text)
            if not normalized_text:
                return {"text": "", "entities": []}

            tokens = self.preprocessor.tokenize_words(normalized_text)
            if not tokens:
                return {"text": normalized_text, "entities": []}

            chunks = self.preprocessor.chunk_tokens(tokens, normalized_text)
            self.logger.info(
                "PREPROCESS",
                f"Input text ({len(normalized_text)} chars, {len(tokens)} tokens) divided into {len(chunks)} chunks."
            )

            # Step 2: Model Prediction on each chunk
            all_model_entities = []
            for chunk_idx, chunk in enumerate(chunks):
                self.logger.debug("PREDICT", f"Processing chunk {chunk_idx + 1}/{len(chunks)} ({len(chunk.words)} tokens).")
                chunk_entities = self.predictor.predict_chunk(chunk, normalized_text)
                all_model_entities.extend(chunk_entities)

            self.logger.info("PREDICT", f"Total raw model entities before dosage rules: {len(all_model_entities)}.")

            # Step 3: Rule-based Dosage Enhancement & Merging
            merged_entities = self.dosage_extractor.merge_with_model_entities(all_model_entities, normalized_text)
            self.logger.info("DOSAGE_RULE", f"Entities after dosage rule merging: {len(merged_entities)}.")

            # Step 4: Filtering non-target labels and resolving overlapping spans by confidence
            final_entities = self.postprocessor.filter_and_resolve_overlaps(merged_entities, normalized_text)
            self.logger.info("FILTER", f"Final extracted entities: {len(final_entities)}.")

            return {
                "text": normalized_text,
                "entities": final_entities,
            }

        except Exception as e:
            # Never swallow errors silently
            self.logger.error("SYSTEM", f"Pipeline error while processing text: {text[:80]!r}", exc=e)
            raise
