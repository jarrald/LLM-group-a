"""Chroma server client and the course collection.

The application always talks to a running Chroma server (ADR-003) via ``HttpClient``.
Tests use ``EphemeralClient``; nothing here opens a ``PersistentClient`` on the server's
data directory.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import chromadb

from app.adapters.chunker import CHUNKER_VERSION
from app.config import Config
from app.errors import RetrievalError

if TYPE_CHECKING:
    from chromadb.api.models.Collection import Collection

logger = logging.getLogger(__name__)

CHROMA_START_HINT = r"chroma run --path .\data\chroma"


def get_chroma_client(config: Config) -> Any:
    """Return a client for the local Chroma server, or raise :class:`RetrievalError`."""
    try:
        client = chromadb.HttpClient(host=config.chroma_host, port=config.chroma_port, ssl=config.chroma_ssl)
        client.heartbeat()
    except Exception as exc:
        raise RetrievalError(f"Cannot reach the Chroma server at {config.chroma_url}: {exc}. Start it with: {CHROMA_START_HINT}") from exc
    return client


def collection_metadata(config: Config, chunker_version: str = CHUNKER_VERSION, corpus_digest: str | None = None) -> dict[str, str | int]:
    """Metadata that pins what an index was built with (ADR-009, ADR-025).

    ``corpus_digest`` is only passed when an index is written, because computing it means
    chunking the whole corpus; queries therefore never pay for it.
    """
    metadata: dict[str, str | int] = {
        "course_id": config.course_id,
        "embedding_model": config.embed_model,
        "embedding_dim": config.embedding_dim,
        "chunker_version": chunker_version,
    }
    if corpus_digest:
        metadata["corpus_digest"] = corpus_digest
    return metadata


def index_staleness(collection: Collection, corpus_digest: str) -> str | None:
    """Explain why ``collection`` no longer matches the corpus, or return ``None`` if it does."""
    stored = (collection.metadata or {}).get("corpus_digest")
    if not stored:
        return "the collection records no corpus digest, so it was built before digests were introduced (or by an older checkout)"
    if str(stored) != corpus_digest:
        return f"the collection holds chunks from different material (digest {stored}, corpus {corpus_digest})"
    return None


def validate_collection_metadata(collection: Collection, config: Config, chunker_version: str = CHUNKER_VERSION) -> None:
    """Raise :class:`RetrievalError` if the index was built with different settings."""
    stored = collection.metadata or {}
    expected = collection_metadata(config, chunker_version)
    mismatched = {key: (stored.get(key), value) for key, value in expected.items() if str(stored.get(key)) != str(value)}
    if mismatched:
        details = ", ".join(f"{key}: stored={old!r} expected={new!r}" for key, (old, new) in mismatched.items())
        raise RetrievalError(f"Collection '{collection.name}' does not match the current configuration ({details}). Re-index with: uv run python .\\scripts\\ingest.py --recreate")


def get_or_create_course_collection(client: Any, config: Config, chunker_version: str = CHUNKER_VERSION) -> Collection:
    """Open the course collection, creating it with pinned metadata if needed."""
    collection = client.get_or_create_collection(
        name=config.collection_name,
        metadata=collection_metadata(config, chunker_version),
        embedding_function=None,
    )
    validate_collection_metadata(collection, config, chunker_version)
    return collection


def get_course_collection(client: Any, config: Config, chunker_version: str = CHUNKER_VERSION) -> Collection:
    """Open an existing course collection for querying; fail clearly if it is missing."""
    try:
        collection = client.get_collection(name=config.collection_name, embedding_function=None)
    except Exception as exc:
        raise RetrievalError(f"Collection '{config.collection_name}' is not available: {exc}. Index the course material with: uv run python .\\scripts\\ingest.py") from exc
    validate_collection_metadata(collection, config, chunker_version)
    return collection
