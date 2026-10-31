"""Fixtures for integration tests: a real SQLite file in a temporary directory."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from app.adapters.sqlite_store import SqliteStore
from tests.integration.factories import COURSE


@pytest.fixture
def store(tmp_path: Path) -> Iterator[SqliteStore]:
    store = SqliteStore(tmp_path / "studygraph.db")
    store.upsert_course(COURSE)
    yield store
