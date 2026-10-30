"""Retrieval result types: pure, so the graph and prompts never import Chroma."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.conversation import RetrievalStatus, SourceReference


@dataclass(frozen=True, slots=True)
class RetrievedPassage:
    """A retrieved chunk in the shape the prompt needs."""

    chunk_id: str
    doc_name: str
    section: str
    text: str

    def render(self, index: int) -> str:
        heading = f"{self.doc_name} — {self.section}" if self.section else self.doc_name
        return f"[{index}] {heading} (chunk {self.chunk_id})\n{self.text.strip()}"


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    """Outcome of one retrieval call: what was found *and* how it went.

    ``failed`` is never the same as ``empty``: the first means retrieval broke, the second
    means it worked and found nothing relevant (rag-pipeline.md §7).
    """

    status: RetrievalStatus
    passages: tuple[RetrievedPassage, ...] = ()
    sources: tuple[SourceReference, ...] = ()
    error: str | None = None
    top_k: int = 0
    scores: tuple[float, ...] = field(default=())

    @property
    def is_grounded(self) -> bool:
        return self.status is RetrievalStatus.OK

    @property
    def passage_count(self) -> int:
        return len(self.passages)

    @classmethod
    def skipped(cls) -> RetrievalResult:
        """No retrieval was attempted (general conversation)."""
        return cls(status=RetrievalStatus.SKIPPED)

    @classmethod
    def failed(cls, error: str, top_k: int = 0) -> RetrievalResult:
        return cls(status=RetrievalStatus.FAILED, error=error, top_k=top_k)

    @classmethod
    def from_matches(
        cls,
        passages: tuple[RetrievedPassage, ...],
        sources: tuple[SourceReference, ...],
        scores: tuple[float, ...],
        top_k: int,
    ) -> RetrievalResult:
        status = RetrievalStatus.OK if passages else RetrievalStatus.EMPTY
        return cls(status=status, passages=passages, sources=sources, scores=scores, top_k=top_k)
