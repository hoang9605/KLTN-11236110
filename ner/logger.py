"""Structured logger for Vietnamese Medical NER pipeline.

Logs every pipeline stage to a dedicated log file:
  - PREPROCESS: tokenization, whitespace normalization, sentence chunking
  - PREDICT: model inference, subtoken generation, logits
  - ALIGN: subtoken-to-word alignment, special token removal
  - MAP: 37 VietMed labels to 6 target labels mapping and filtering
  - DOSAGE_RULE: regex dosage extraction and {value, unit, frequency} merging
  - FILTER: removing non-target labels, overlap resolution by confidence
"""
import logging
import os
import sys
import traceback
from pathlib import Path
from typing import Optional

from .config import DEFAULT_LOG_PATH


class NERPipelineLogger:
    """Dedicated logger writing pipeline steps to a dedicated log file."""

    VALID_STAGES = {
        "SYSTEM",
        "PREPROCESS",
        "PREDICT",
        "ALIGN",
        "MAP",
        "DOSAGE_RULE",
        "FILTER",
        "RULE_BLACKLIST",
        "RULE_MERGE",
        "NORMALIZE",
    }

    def __init__(self, log_path: Optional[Path] = None, enable_console: bool = False):
        self.log_path = Path(log_path) if log_path else DEFAULT_LOG_PATH
        self.enable_console = enable_console
        self.logger = logging.getLogger("MedicalNERPipeline")
        self.logger.setLevel(logging.DEBUG)

        # Avoid duplicate handlers if re-initialized
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Create file handler and optional console handler."""
        # Ensure log directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(stage)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File Handler (UTF-8 encoding)
        file_handler = logging.FileHandler(self.log_path, encoding="utf-8", mode="a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console Handler (optional)
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log(self, stage: str, message: str, level: str = "INFO") -> None:
        """Log a message for a specific pipeline stage."""
        stage_tag = stage.upper() if stage.upper() in self.VALID_STAGES else "SYSTEM"
        log_level = getattr(logging, level.upper(), logging.INFO)
        extra = {"stage": stage_tag}
        self.logger.log(log_level, message, extra=extra)

    def debug(self, stage: str, message: str) -> None:
        self.log(stage, message, level="DEBUG")

    def info(self, stage: str, message: str) -> None:
        self.log(stage, message, level="INFO")

    def warning(self, stage: str, message: str) -> None:
        self.log(stage, message, level="WARNING")

    def error(self, stage: str, message: str, exc: Optional[BaseException] = None) -> None:
        """Log an error with traceback without swallowing exceptions."""
        stage_tag = stage.upper() if stage.upper() in self.VALID_STAGES else "SYSTEM"
        extra = {"stage": stage_tag}
        if exc is not None:
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            self.logger.error(f"{message}\nException: {exc}\nTraceback:\n{tb}", extra=extra)
        else:
            self.logger.error(message, extra=extra)

    def log_blacklist_dropped(
        self,
        entity_label: str,
        surface_text: str,
        start_char: int,
        end_char: int,
        confidence: float,
    ) -> None:
        """Log when an entity is dropped by Rule 1 (DRUG action blacklist)."""
        self.info(
            "RULE_BLACKLIST",
            f"Rule 1 Dropped: [{entity_label}] {surface_text!r} [{start_char}:{end_char}] (conf={confidence:.4f})",
        )

    def log_severity_merged(
        self,
        cond_text: str,
        cond_start: int,
        cond_end: int,
        cond_conf: float,
        dos_text: str,
        dos_start: int,
        dos_end: int,
        dos_conf: float,
        merged_text: str,
        merged_start: int,
        merged_end: int,
        merged_conf: float,
    ) -> None:
        """Log when Rule 2 merges a clinical severity DOSAGE entity into preceding CONDITION."""
        self.info(
            "RULE_MERGE",
            f"Rule 2 Merged: [CONDITION] {cond_text!r} [{cond_start}:{cond_end}] (conf={cond_conf:.4f}) "
            f"+ [DOSAGE] {dos_text!r} [{dos_start}:{dos_end}] (conf={dos_conf:.4f}) "
            f"-> [CONDITION] {merged_text!r} [{merged_start}:{merged_end}] (conf={merged_conf:.4f})",
        )

    def log_normalized(
        self,
        entity_label: str,
        surface_text: str,
        ontology: str,
        code: str,
        match_method: str,
    ) -> None:
        """Log when an entity is successfully normalized into a standard ontology."""
        self.info(
            "NORMALIZE",
            f"Normalized: [{entity_label}] {surface_text!r} -> [{ontology}] code={code!r} (method={match_method})",
        )



# Default module-level singleton instance
_default_logger: Optional[NERPipelineLogger] = None


def get_logger(log_path: Optional[Path] = None, enable_console: bool = False) -> NERPipelineLogger:
    """Retrieve or create singleton logger instance."""
    global _default_logger
    if _default_logger is None:
        _default_logger = NERPipelineLogger(log_path=log_path, enable_console=enable_console)
    return _default_logger
