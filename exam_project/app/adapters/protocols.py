"""Small protocols so the graph and services can be tested with fakes."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol

from app.domain.retrieval import RetrievalResult


class ChatModel(Protocol):
    """A local text-generation model."""

    @property
    def model_name(self) -> str:
        """Identifier recorded on every generated message."""
        ...

    def complete(self, messages: list[dict[str, str]]) -> str:
        """Return the assistant's reply for a full message list."""
        ...

    def stream(self, messages: list[dict[str, str]]) -> Iterator[str]:
        """Yield the reply piece by piece, for streaming UIs."""
        ...


class Retriever(Protocol):
    """A retrieval backend for course material."""

    def retrieve(self, query: str, top_k: int | None = None) -> RetrievalResult:
        """Return passages plus how the retrieval went. Never raises on a backend failure."""
        ...
