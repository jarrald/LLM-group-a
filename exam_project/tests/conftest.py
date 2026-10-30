"""Shared pytest fixtures."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from app.config import PROJECT_ROOT, get_config


@pytest.fixture(autouse=True)
def clear_config_cache() -> Iterator[None]:
    """Make every test start from a freshly loaded configuration."""
    get_config.cache_clear()
    yield
    get_config.cache_clear()


@pytest.fixture
def project_root():
    """Absolute path of the ``exam_project`` directory."""
    return PROJECT_ROOT
