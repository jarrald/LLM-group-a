"""Embeddings from the local Ollama server.

This module is the single source of embeddings in the application (ADR-004). Chroma's own
embedding function is never used: we compute vectors here and pass them explicitly, so the
model and the dimension are ours to validate.
"""

from __future__ import annotations

import logging

import ollama

from app.config import Config
from app.errors import EmbeddingError, LlmUnavailableError

logger = logging.getLogger(__name__)

BATCH_SIZE = 32


class OllamaEmbedder:
    """Produces embeddings with the configured Ollama embedding model."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._client = ollama.Client(host=config.ollama_base_url, timeout=config.request_timeout_s)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed many texts, in batches, preserving order."""
        vectors: list[list[float]] = []
        for start in range(0, len(texts), BATCH_SIZE):
            batch = texts[start : start + BATCH_SIZE]
            logger.debug("embedding batch %d-%d", start, start + len(batch))
            vectors.extend(self._embed(batch))
        return vectors

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query string."""
        return self._embed([text])[0]

    def _embed(self, texts: list[str]) -> list[list[float]]:
        try:
            response = self._client.embed(model=self._config.embed_model, input=texts)
        except Exception as exc:
            raise LlmUnavailableError(f"Cannot embed with '{self._config.embed_model}' via {self._config.ollama_base_url}: {exc}") from exc

        vectors = [list(vector) for vector in response.embeddings]
        if len(vectors) != len(texts):
            raise EmbeddingError(f"Model '{self._config.embed_model}' returned {len(vectors)} vectors for {len(texts)} inputs")

        for vector in vectors:
            if len(vector) != self._config.embedding_dim:
                raise EmbeddingError(
                    f"Model '{self._config.embed_model}' returns {len(vector)} dimensions but STUDYGRAPH_EMBEDDING_DIM={self._config.embedding_dim}. Fix the configuration and re-index."
                )
        return vectors
