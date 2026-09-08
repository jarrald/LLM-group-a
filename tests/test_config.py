from pathlib import Path

import pytest

from workflow.config import AppConfig, ConfigError, load_config

ROOT = Path(__file__).resolve().parents[1]


def test_load_default_config():
    cfg = load_config(str(ROOT / "config.yaml"))
    assert isinstance(cfg, AppConfig)
    assert {"architect", "tech_lead", "worker"} <= set(cfg.roles)
    assert len(set(cfg.endpoints.values())) >= 2
    assert cfg.workflow.worker_count >= 2


def test_env_role_model_and_endpoint_override(monkeypatch):
    monkeypatch.setenv("ARCHITECT_MODEL", "codellama:7b")
    monkeypatch.setenv("TECH_LEAD_ENDPOINT", "http://127.0.0.1:9999")
    cfg = load_config(str(ROOT / "config.yaml"))
    assert cfg.roles["architect"].model == "codellama:7b"
    assert cfg.roles["tech_lead"].endpoint_url == "http://127.0.0.1:9999"


def test_env_endpoint_url_override(monkeypatch):
    monkeypatch.setenv("OLLAMA_B_URL", "http://127.0.0.1:11500")
    cfg = load_config(str(ROOT / "config.yaml"))
    assert cfg.endpoints["ollama_b"] == "http://127.0.0.1:11500"
    assert cfg.roles["tech_lead"].endpoint_url == "http://127.0.0.1:11500"


def test_unknown_endpoint_reference(tmp_path):
    p = tmp_path / "config.yaml"
    p.write_text(
        "endpoints:\n  a:\n    url: http://x:1\n  b:\n    url: http://x:2\n"
        "roles:\n  r:\n    endpoint: missing\n    model: m\n",
        encoding="utf-8",
    )
    with pytest.raises(ConfigError):
        load_config(str(p))


def test_missing_config(tmp_path):
    with pytest.raises(ConfigError):
        load_config(str(tmp_path / "nope.yaml"))


def test_single_endpoint_rejected(tmp_path):
    p = tmp_path / "config.yaml"
    p.write_text(
        "endpoints:\n  a:\n    url: http://x:1\nroles:\n  r:\n    endpoint: a\n    model: m\n",
        encoding="utf-8",
    )
    with pytest.raises(ConfigError):
        load_config(str(p))
