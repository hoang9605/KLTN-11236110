"""Logging utilities for entity normalization.

Provides daily log file generation in `normalization/logs/` and an unmatched drug
tracker in `normalization/data/unmatched_drugs.log`.
"""

import datetime
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from normalization.base import NormalizedResult

MODULE_ROOT = Path(__file__).resolve().parent
DEFAULT_LOG_DIR = MODULE_ROOT / "logs"
DEFAULT_DATA_DIR = MODULE_ROOT / "data"


def get_daily_logger(log_dir: Optional[Path] = None) -> logging.Logger:
    """Get or configure a logger that writes to a daily log file."""
    log_dir = Path(log_dir) if log_dir else DEFAULT_LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)

    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"normalization_{today_str}.log"

    logger_name = f"normalization.{today_str}"
    logger = logging.getLogger(logger_name)

    # Configure handler only if not already attached to this file
    has_file_handler = any(
        isinstance(h, logging.FileHandler) and Path(h.baseFilename) == log_file
        for h in logger.handlers
    )

    if not has_file_handler:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def log_normalization(
    entity: Dict[str, Any],
    result: Optional[NormalizedResult],
    match_method: str,
    elapsed_ms: float,
    exc: Optional[Exception] = None,
    log_dir: Optional[Path] = None,
) -> None:
    """Record an entity normalization event to the daily log.

    Args:
        entity: Input entity dictionary (surface_text, label, etc.).
        result: Result object or None.
        match_method: Resolution method description.
        elapsed_ms: Processing duration in milliseconds.
        exc: Optional exception if an unexpected error occurred.
        log_dir: Directory to place the daily log.
    """
    logger = get_daily_logger(log_dir)

    surface_text = entity.get("surface_text", "")
    label = entity.get("label", "UNKNOWN")

    if exc is not None:
        logger.error(
            f"FAILED entity='{surface_text}' label={label} "
            f"elapsed_ms={elapsed_ms:.2f} error={exc}",
            exc_info=True,
        )
        return

    if result is not None:
        logger.info(
            f"SUCCESS entity='{surface_text}' label={label} "
            f"ontology={result.ontology} code={result.code} "
            f"standard='{result.label_standard}' method={result.match_method} "
            f"score={result.match_score:.3f} elapsed_ms={elapsed_ms:.2f}"
        )
    else:
        logger.info(
            f"UNMATCHED entity='{surface_text}' label={label} "
            f"method={match_method} elapsed_ms={elapsed_ms:.2f}"
        )


def log_unmatched_drug(surface_text: str, log_path: Optional[Path] = None) -> None:
    """Append unmatched drug name to the review log file.

    Args:
        surface_text: Drug surface text that failed RxNorm normalization.
        log_path: Path to unmatched_drugs.log.
    """
    log_file = Path(log_path) if log_path else DEFAULT_DATA_DIR / "unmatched_drugs.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(str(log_file), "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {surface_text}\n")
