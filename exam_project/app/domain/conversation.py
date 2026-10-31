"""Conversations, messages and retrieval provenance."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from app.domain.buddy import BuddySnapshot
from app.errors import ValidationError

MAX_MESSAGE_LENGTH = 4000


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


class RetrievalStatus(StrEnum):
    """How retrieval went for one assistant message.

    ``failed`` must never be reported as ``empty``: only ``ok`` means the answer is
    grounded in course material (NFR-04, rag-pipeline.md §7).
    """

    OK = "ok"
    EMPTY = "empty"
    FAILED = "failed"
    SKIPPED = "skipped"

    @property
    def is_grounded(self) -> bool:
        return self is RetrievalStatus.OK


def validate_message_content(content: str) -> str:
    """Return the trimmed message text or raise :class:`ValidationError`."""
    cleaned = content.strip()
    if not cleaned:
        raise ValidationError("The message must not be empty")
    if len(cleaned) > MAX_MESSAGE_LENGTH:
        raise ValidationError(f"The message must be at most {MAX_MESSAGE_LENGTH} characters")
    return cleaned


@dataclass(frozen=True, slots=True)
class SourceReference:
    """A retrieved chunk, kept so the UI can show and the exam can demonstrate grounding."""

    chunk_id: str
    doc_id: str
    doc_name: str
    section: str
    lecture: int | None = None
    distance: float | None = None
    snippet: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "doc_name": self.doc_name,
            "section": self.section,
            "lecture": self.lecture,
            "distance": self.distance,
            "snippet": self.snippet,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> SourceReference:
        lecture = payload.get("lecture")
        distance = payload.get("distance")
        return cls(
            chunk_id=str(payload["chunk_id"]),
            doc_id=str(payload["doc_id"]),
            doc_name=str(payload["doc_name"]),
            section=str(payload.get("section", "")),
            lecture=None if lecture is None else int(str(lecture)),
            distance=None if distance is None else float(str(distance)),
            snippet=str(payload.get("snippet", "")),
        )

    def label(self) -> str:
        """Human-readable citation, e.g. ``Week 1 — 3. Model fitting > Overfitting``."""
        parts = [self.doc_name]
        if self.section:
            parts.append(self.section)
        return " — ".join(parts)


@dataclass(frozen=True, slots=True)
class Conversation:
    """A chat session with the Buddy snapshot it was created from."""

    id: str
    title: str
    buddy_snapshot: BuddySnapshot
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class Message:
    """One stored message, with provenance for assistant answers."""

    id: str
    conversation_id: str
    role: MessageRole
    content: str
    created_at: datetime
    retrieval_status: RetrievalStatus = RetrievalStatus.SKIPPED
    sources: tuple[SourceReference, ...] = ()
    model: str | None = None
    prompt_version: str | None = None
    retrieval_top_k: int | None = None


def sources_to_json(sources: tuple[SourceReference, ...]) -> str:
    return json.dumps([source.to_dict() for source in sources], ensure_ascii=False)


def sources_from_json(raw: str | None) -> tuple[SourceReference, ...]:
    if not raw:
        return ()
    return tuple(SourceReference.from_dict(item) for item in json.loads(raw))
