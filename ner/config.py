"""Configuration and label mapping for Vietnamese Medical NER pipeline.

Schema: 6 target entity types mapped from VietMed-NER 37 BIO tags:
  - CONDITION <- DISEASESYMTOM
  - DRUG <- DRUGCHEMICAL, PREVENTIVEMED
  - BODY_PART <- ORGAN
  - TEST <- DIAGNOSTICS
  - PROCEDURE <- SURGERY, MEDDEVICETECHNIQUE, TREATMENT
  - DOSAGE <- UNITCALIBRATOR

All other tags (AGE, GENDER, DATETIME, OCCUPATION, LOCATION, ORGANIZATION,
FOODDRINK, PERSONALCARE, TRANSPORTATION) are strictly discarded (not kept as OTHER).
"""
from pathlib import Path
from typing import Dict, List, Optional, Set

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Potential locations for model checkpoint
DEFAULT_MODEL_PATHS: List[Path] = [
    PROJECT_ROOT / "Model" / "vihealthbert-ner-vietmed-v2-final",
    PROJECT_ROOT / "Code" / "Model" / "vihealthbert-ner-vietmed-v2-final",
    Path("Model/vihealthbert-ner-vietmed-v2-final"),
    Path("Code/Model/vihealthbert-ner-vietmed-v2-final"),
]

# The 6 target medical entity types (strictly fixed)
TARGET_LABELS: Set[str] = {
    "CONDITION",
    "DRUG",
    "BODY_PART",
    "TEST",
    "PROCEDURE",
    "DOSAGE",
}

# Mapping table from VietMed entity types (without BIO prefix) to Target types
VIETMED_TO_TARGET: Dict[str, str] = {
    # CONDITION
    "DISEASESYMTOM": "CONDITION",
    # DRUG
    "DRUGCHEMICAL": "DRUG",
    "PREVENTIVEMED": "DRUG",
    # BODY_PART
    "ORGAN": "BODY_PART",
    # TEST
    "DIAGNOSTICS": "TEST",
    # PROCEDURE
    "SURGERY": "PROCEDURE",
    "MEDDEVICETECHNIQUE": "PROCEDURE",
    "TREATMENT": "PROCEDURE",
    # DOSAGE
    "UNITCALIBRATOR": "DOSAGE",
}

# Special tokens that must be eliminated before BIO decoding
SPECIAL_TOKENS: Set[str] = {
    "<s>",
    "</s>",
    "<pad>",
    "<unk>",
    "<mask>",
    "[CLS]",
    "[SEP]",
    "[PAD]",
    "[UNK]",
    "[MASK]",
}

# Model sequence limits
# Checkpoint max_position_embeddings = 258.
# Reserving 2 slots for <s> and </s> gives max 256 subtokens.
# We set max chunk subtoken length to 200 for safety and clean sentence boundaries.
MAX_POSITION_EMBEDDINGS: int = 258
MAX_SUBTOKENS_PER_CHUNK: int = 200

# Default log path
DEFAULT_LOG_PATH: Path = PROJECT_ROOT / "logs" / "ner_pipeline.log"


def resolve_model_path(custom_path: Optional[str] = None) -> Path:
    """Find and return valid model checkpoint directory."""
    if custom_path:
        p = Path(custom_path)
        if p.exists() and (p / "config.json").exists():
            return p
        raise FileNotFoundError(f"Model checkpoint not found at specified path: {custom_path}")

    for p in DEFAULT_MODEL_PATHS:
        if p.exists() and (p / "config.json").exists():
            return p

    raise FileNotFoundError(
        f"Model checkpoint vihealthbert-ner-vietmed-v2-final not found in any of: "
        f"{[str(p) for p in DEFAULT_MODEL_PATHS]}"
    )
