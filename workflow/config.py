"""Configuration loading and validation for the multi-LLM workflow.

Hard requirement 1 (multiple local endpoints + config-based routing) is
implemented here: every role resolves to an endpoint URL plus a model, and the
binding can be changed via ``config.yaml`` or environment variables -- without
touching any code.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import yaml

DEFAULT_CONFIG_PATHS = ("config.yaml", "config.yml")


class ConfigError(Exception):
    """Raised when the workflow configuration is missing or invalid."""


@dataclass
class RoleConfig:
    name: str
    endpoint_name: str
    endpoint_url: str
    model: str
    temperature: float = 0.2
    num_predict: int = 4096


@dataclass
class WorkflowSettings:
    worker_count: int = 2
    max_retries: int = 1
    request_timeout_seconds: int = 900
    workspace_dir: str = "workspace"


@dataclass
class AppConfig:
    endpoints: Dict[str, str]
    roles: Dict[str, RoleConfig]
    workflow: WorkflowSettings
    source: str


def _env_name(name: str, suffix: str) -> str:
    """Turn a name like ``tech_lead`` into ``TECH_LEAD_<SUFFIX>``."""
    prefix = re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")
    return f"{prefix}_{suffix}"


def _find_config(path: Optional[str]) -> Optional[Path]:
    if path:
        candidate = Path(path)
        return candidate if candidate.is_file() else None
    for name in DEFAULT_CONFIG_PATHS:
        candidate = Path(name)
        if candidate.is_file():
            return candidate
    return None


def _endpoint_url(name: str, spec: object) -> str:
    if isinstance(spec, str):
        url = spec
    elif isinstance(spec, dict):
        url = spec.get("url") or ""
    else:
        url = ""
    if not url:
        raise ConfigError(f"endpoint '{name}' is missing a 'url'")
    return os.environ.get(_env_name(name, "URL"), url).rstrip("/")


def load_config(path: Optional[str] = None) -> AppConfig:
    """Load and validate configuration from ``config.yaml`` (or ``path``)."""
    cfg_path = _find_config(path)
    if cfg_path is None:
        hint = path or " or ".join(DEFAULT_CONFIG_PATHS)
        raise ConfigError(f"configuration file not found: {hint}")

    raw = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}

    endpoints: Dict[str, str] = {}
    for name, spec in (raw.get("endpoints") or {}).items():
        endpoints[str(name)] = _endpoint_url(str(name), spec)
    if not endpoints:
        raise ConfigError("no 'endpoints' defined in configuration")
    if len(set(endpoints.values())) < 2:
        raise ConfigError(
            "at least two distinct endpoint URLs are required "
            "(Hard Requirement 1: multiple local endpoints)"
        )

    roles_raw = raw.get("roles") or {}
    if not roles_raw:
        raise ConfigError("no 'roles' defined in configuration")

    roles: Dict[str, RoleConfig] = {}
    for name, spec in roles_raw.items():
        if not isinstance(spec, dict):
            raise ConfigError(f"role '{name}' must be a mapping")
        endpoint_name = str(spec.get("endpoint") or "")
        if endpoint_name not in endpoints:
            raise ConfigError(f"role '{name}' references unknown endpoint '{endpoint_name}'")
        model = str(spec.get("model") or "")
        if not model:
            raise ConfigError(f"role '{name}' is missing a 'model'")

        url = os.environ.get(
            _env_name(str(name), "ENDPOINT"), endpoints[endpoint_name]
        ).rstrip("/")
        model = os.environ.get(_env_name(str(name), "MODEL"), model)

        roles[str(name)] = RoleConfig(
            name=str(name),
            endpoint_name=endpoint_name,
            endpoint_url=url,
            model=model,
            temperature=float(spec.get("temperature", 0.2)),
            num_predict=int(spec.get("num_predict", 4096)),
        )

    wf = raw.get("workflow") or {}
    settings = WorkflowSettings(
        worker_count=int(os.environ.get("WORKER_COUNT", wf.get("worker_count", 2))),
        max_retries=int(
            os.environ.get("WORKFLOW_MAX_RETRIES", wf.get("max_retries", 1))
        ),
        request_timeout_seconds=int(
            os.environ.get("WORKFLOW_TIMEOUT_SECONDS", wf.get("request_timeout_seconds", 900))
        ),
        workspace_dir=str(wf.get("workspace_dir", "workspace")),
    )
    if settings.worker_count < 1:
        raise ConfigError("workflow.worker_count must be at least 1 (recommended: 2)")
    if settings.max_retries < 0:
        raise ConfigError("workflow.max_retries must be >= 0")

    return AppConfig(
        endpoints=endpoints,
        roles=roles,
        workflow=settings,
        source=str(cfg_path),
    )
