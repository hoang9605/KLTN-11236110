"""Cấu hình đọc từ biến môi trường (đặt trong deploy/.env khi chạy docker compose)."""
import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _bool(name, default):
    v = os.environ.get(name)
    return default if v is None else v.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Settings:
    # postgresql+psycopg://user:pass@db:5432/medkg ; mặc định SQLite cho chạy cục bộ / kiểm thử
    database_url: str = field(default_factory=lambda: os.environ.get(
        "DATABASE_URL", f"sqlite:///{(ROOT / 'outputs' / 'server.db').as_posix()}"))
    model_dir: Path = field(default_factory=lambda: Path(os.environ.get("MODEL_DIR", ROOT / "Model")))
    ner_model: str = field(default_factory=lambda: os.environ.get("NER_MODEL", "vihealthbert-ner-vietmed-v2-final"))
    re_model: str = field(default_factory=lambda: os.environ.get("RE_MODEL", "vihealthbert-re-vietmed-811"))
    device: str = field(default_factory=lambda: os.environ.get("DEVICE", "") or None)
    max_chars: int = field(default_factory=lambda: int(os.environ.get("MAX_CHARS", "2000")))
    max_batch: int = field(default_factory=lambda: int(os.environ.get("MAX_BATCH", "20")))
    # nạp sẵn kết quả đã chạy (results.jsonl của scripts/build_kg.py) khi CSDL còn trống
    seed_file: str = field(default_factory=lambda: os.environ.get("SEED_FILE", ""))
    load_models: bool = field(default_factory=lambda: _bool("LOAD_MODELS", True))
    cors_origins: tuple = field(default_factory=lambda: tuple(
        o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()))

    @property
    def ner_path(self):
        return self.model_dir / self.ner_model

    @property
    def re_path(self):
        return self.model_dir / self.re_model


def get_settings():
    return Settings()
