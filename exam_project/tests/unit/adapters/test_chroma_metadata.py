"""Tests for collection metadata and stale-index detection (ADR-009, ADR-025)."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.adapters.chroma_client import collection_metadata, index_staleness
from app.config import load_config


@dataclass
class FakeCollection:
    """The only part of a Chroma collection these functions read."""

    metadata: dict[str, object] = field(default_factory=dict)
    name: str = "llms_for_devs_v1"


def test_collection_metadata_pins_model_and_chunker() -> None:
    config = load_config()

    metadata = collection_metadata(config)

    assert metadata["embedding_model"] == config.embed_model
    assert metadata["embedding_dim"] == config.embedding_dim
    assert metadata["course_id"] == config.course_id
    assert "corpus_digest" not in metadata, "queries must not need the corpus digest"


def test_collection_metadata_records_the_digest_when_writing_an_index() -> None:
    config = load_config()

    metadata = collection_metadata(config, corpus_digest="abc123")

    assert metadata["corpus_digest"] == "abc123"


def test_index_staleness_is_none_for_the_matching_corpus() -> None:
    collection = FakeCollection(metadata={"corpus_digest": "abc123"})

    assert index_staleness(collection, "abc123") is None  # type: ignore[arg-type]


def test_index_staleness_reports_a_different_corpus() -> None:
    collection = FakeCollection(metadata={"corpus_digest": "abc123"})

    reason = index_staleness(collection, "def456")  # type: ignore[arg-type]

    assert reason is not None
    assert "abc123" in reason and "def456" in reason


def test_index_staleness_reports_an_index_without_a_digest() -> None:
    collection = FakeCollection(metadata={"embedding_model": "nomic-embed-text"})

    reason = index_staleness(collection, "abc123")  # type: ignore[arg-type]

    assert reason is not None
    assert "no corpus digest" in reason
