"""Application configuration, read once from the environment.

Every value that could differ between machines (endpoints, models, ports, paths,
generation and retrieval parameters) lives here and nowhere else. Nothing in ``app/``
may hardcode a model name, URL, port or path.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.errors import ConfigError

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _env_str(name: str, default: str) -> str:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip()


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw.strip())
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer, got {raw!r}") from exc


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw.strip())
    except ValueError as exc:
        raise ConfigError(f"{name} must be a number, got {raw!r}") from exc


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    value = raw.strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise ConfigError(f"{name} must be a boolean (true/false), got {raw!r}")


def _env_path(name: str, default: Path) -> Path:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return Path(raw.strip()).expanduser().resolve()


@dataclass(frozen=True, slots=True)
class Config:
    """Effective application configuration."""

    # Local language model (Ollama)
    ollama_base_url: str
    chat_model: str
    embed_model: str
    embedding_dim: int
    temperature: float
    num_ctx: int
    request_timeout_s: float

    # Retrieval
    top_k: int
    collection_name: str
    course_id: str

    # Vector store (Chroma server)
    chroma_host: str
    chroma_port: int
    chroma_ssl: bool
    chroma_data_path: Path

    # Application data and content
    data_dir: Path
    db_path: Path
    course_material_dir: Path
    prompts_dir: Path

    @property
    def chroma_url(self) -> str:
        """Base URL of the local Chroma server, e.g. ``http://localhost:8000``."""
        scheme = "https" if self.chroma_ssl else "http"
        return f"{scheme}://{self.chroma_host}:{self.chroma_port}"

    def validate(self) -> None:
        """Raise :class:`ConfigError` if any value is outside its allowed range."""
        if not self.chat_model:
            raise ConfigError("STUDYGRAPH_CHAT_MODEL must not be empty")
        if not self.embed_model:
            raise ConfigError("STUDYGRAPH_EMBED_MODEL must not be empty")
        if self.embedding_dim <= 0:
            raise ConfigError("STUDYGRAPH_EMBEDDING_DIM must be positive")
        if self.top_k < 1:
            raise ConfigError("STUDYGRAPH_TOP_K must be at least 1")
        if not 0.0 <= self.temperature <= 2.0:
            raise ConfigError("STUDYGRAPH_TEMPERATURE must be between 0 and 2")
        if self.num_ctx < 256:
            raise ConfigError("STUDYGRAPH_NUM_CTX must be at least 256")
        if self.request_timeout_s <= 0:
            raise ConfigError("STUDYGRAPH_REQUEST_TIMEOUT must be positive")
        if not 1 <= self.chroma_port <= 65535:
            raise ConfigError("STUDYGRAPH_CHROMA_PORT must be a valid TCP port")


def load_config() -> Config:
    """Build a :class:`Config` from the current environment and validate it."""
    config = Config(
        ollama_base_url=_env_str("STUDYGRAPH_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/"),
        chat_model=_env_str("STUDYGRAPH_CHAT_MODEL", "llama3.2:3b"),
        embed_model=_env_str("STUDYGRAPH_EMBED_MODEL", "nomic-embed-text"),
        embedding_dim=_env_int("STUDYGRAPH_EMBEDDING_DIM", 768),
        temperature=_env_float("STUDYGRAPH_TEMPERATURE", 0.2),
        num_ctx=_env_int("STUDYGRAPH_NUM_CTX", 4096),
        request_timeout_s=_env_float("STUDYGRAPH_REQUEST_TIMEOUT", 120.0),
        top_k=_env_int("STUDYGRAPH_TOP_K", 4),
        collection_name=_env_str("STUDYGRAPH_COLLECTION", "llms_for_devs_v1"),
        course_id=_env_str("STUDYGRAPH_COURSE_ID", "llms_for_devs"),
        chroma_host=_env_str("STUDYGRAPH_CHROMA_HOST", "localhost"),
        chroma_port=_env_int("STUDYGRAPH_CHROMA_PORT", 8000),
        chroma_ssl=_env_bool("STUDYGRAPH_CHROMA_SSL", False),
        chroma_data_path=_env_path("STUDYGRAPH_CHROMA_PATH", PROJECT_ROOT / "data" / "chroma"),
        data_dir=_env_path("STUDYGRAPH_DATA_DIR", PROJECT_ROOT / "data"),
        db_path=_env_path("STUDYGRAPH_DB_PATH", PROJECT_ROOT / "data" / "studygraph.db"),
        course_material_dir=_env_path(
            "STUDYGRAPH_COURSE_MATERIAL_DIR",
            PROJECT_ROOT / "docs" / "RAG" / "llm_for_developers",
        ),
        prompts_dir=_env_path("STUDYGRAPH_PROMPTS_DIR", PROJECT_ROOT / "app" / "prompts"),
    )
    config.validate()
    return config


@lru_cache(maxsize=1)
def get_config() -> Config:
    """Return the process-wide configuration (cached)."""
    return load_config()


def reload_config() -> Config:
    """Discard the cached configuration and load it again (used by tests and scripts)."""
    get_config.cache_clear()
    return get_config()
