"""Unit tests for ``app.config`` — defaults, environment overrides and validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.config import get_config, load_config, reload_config
from app.errors import ConfigError


def test_config_defaults_are_local_first() -> None:
    config = load_config()

    assert config.ollama_base_url == "http://127.0.0.1:11434"
    assert config.chroma_url == "http://localhost:8000"
    assert config.chat_model
    assert config.embed_model
    assert config.top_k == 4
    assert config.course_id == "llms_for_devs"
    assert config.collection_name.startswith("llms_for_devs")


def test_config_defaults_keep_all_data_inside_the_project(project_root: Path) -> None:
    config = load_config()

    assert config.data_dir == project_root / "data"
    assert config.db_path == project_root / "data" / "studygraph.db"
    assert config.chroma_data_path == project_root / "data" / "chroma"
    assert config.db_path.is_absolute()
    assert config.prompts_dir == project_root / "app" / "prompts"


def test_config_reads_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUDYGRAPH_OLLAMA_URL", "http://127.0.0.1:11500/")
    monkeypatch.setenv("STUDYGRAPH_CHAT_MODEL", "qwen2.5:7b")
    monkeypatch.setenv("STUDYGRAPH_EMBED_MODEL", "mxbai-embed-large")
    monkeypatch.setenv("STUDYGRAPH_EMBEDDING_DIM", "1024")
    monkeypatch.setenv("STUDYGRAPH_TOP_K", "8")
    monkeypatch.setenv("STUDYGRAPH_TEMPERATURE", "0.0")
    monkeypatch.setenv("STUDYGRAPH_CHROMA_PORT", "8123")

    config = load_config()

    assert config.ollama_base_url == "http://127.0.0.1:11500"
    assert config.chat_model == "qwen2.5:7b"
    assert config.embed_model == "mxbai-embed-large"
    assert config.embedding_dim == 1024
    assert config.top_k == 8
    assert config.temperature == 0.0
    assert config.chroma_url == "http://localhost:8123"


def test_config_chroma_url_uses_https_when_ssl_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUDYGRAPH_CHROMA_SSL", "true")

    assert load_config().chroma_url == "https://localhost:8000"


def test_config_blank_environment_variable_falls_back_to_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUDYGRAPH_CHAT_MODEL", "   ")

    assert load_config().chat_model == "llama3.2:3b"


def test_config_rejects_top_k_below_one(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUDYGRAPH_TOP_K", "0")

    with pytest.raises(ConfigError, match="STUDYGRAPH_TOP_K"):
        load_config()


def test_config_rejects_non_integer_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUDYGRAPH_TOP_K", "four")

    with pytest.raises(ConfigError, match="must be an integer"):
        load_config()


def test_config_rejects_temperature_out_of_range(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUDYGRAPH_TEMPERATURE", "3.5")

    with pytest.raises(ConfigError, match="STUDYGRAPH_TEMPERATURE"):
        load_config()


def test_config_rejects_invalid_boolean(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUDYGRAPH_CHROMA_SSL", "maybe")

    with pytest.raises(ConfigError, match="must be a boolean"):
        load_config()


def test_get_config_caches_until_reloaded(monkeypatch: pytest.MonkeyPatch) -> None:
    first = get_config()

    monkeypatch.setenv("STUDYGRAPH_TOP_K", "9")
    assert get_config() is first, "get_config() must be cached"

    reloaded = reload_config()
    assert reloaded.top_k == 9
