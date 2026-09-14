"""Vietnamese Clinical Named Entity Recognition (NER) Pipeline.

Combines pretrained ViHealthBERT (demdecuong/vihealthbert-base-syllable on VietMed-NER)
with clinical rule-based dosage extraction and span conflict resolution.
"""
from .config import TARGET_LABELS, VIETMED_TO_TARGET, resolve_model_path
from .dosage_extractor import DosageEntity, DosageExtractor
from .logger import NERPipelineLogger, get_logger
from .pipeline import MedicalNERPipeline
from .postprocessor import PostProcessor
from .predictor import ModelNERPredictor, RawEntity
from .preprocessor import TextChunk, TextPreprocessor, WordToken

__all__ = [
    "MedicalNERPipeline",
    "TextPreprocessor",
    "ModelNERPredictor",
    "DosageExtractor",
    "PostProcessor",
    "WordToken",
    "TextChunk",
    "RawEntity",
    "DosageEntity",
    "NERPipelineLogger",
    "get_logger",
    "TARGET_LABELS",
    "VIETMED_TO_TARGET",
    "resolve_model_path",
]
