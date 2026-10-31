"""The Buddy aggregate: a reusable teaching configuration and its immutable snapshot.

A Buddy is the *reusable* configuration. A conversation stores a :class:`BuddySnapshot`
so that editing the Buddy never changes an existing conversation (FR-08, ADR-010).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime

from app.domain.options import MAX_BUDDY_NAME_LENGTH, MAX_TRAIT_LENGTH, MAX_TRAITS
from app.errors import ValidationError

SNAPSHOT_VERSION = 1


def validate_buddy_name(name: str) -> str:
    """Return a normalised Buddy name or raise :class:`ValidationError`."""
    cleaned = " ".join(name.split())
    if not cleaned:
        raise ValidationError("Buddy name must not be empty")
    if len(cleaned) > MAX_BUDDY_NAME_LENGTH:
        raise ValidationError(f"Buddy name must be at most {MAX_BUDDY_NAME_LENGTH} characters")
    return cleaned


def validate_traits(traits: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    """Return normalised, de-duplicated traits or raise :class:`ValidationError`."""
    cleaned: list[str] = []
    for trait in traits:
        value = " ".join(str(trait).split())
        if not value:
            continue
        if len(value) > MAX_TRAIT_LENGTH:
            raise ValidationError(f"Trait '{value[:20]}…' is longer than {MAX_TRAIT_LENGTH} characters")
        if value.casefold() not in {existing.casefold() for existing in cleaned}:
            cleaned.append(value)
    if not cleaned:
        raise ValidationError("A Buddy needs at least one trait")
    if len(cleaned) > MAX_TRAITS:
        raise ValidationError(f"A Buddy can have at most {MAX_TRAITS} traits")
    return tuple(cleaned)


def validate_dimension(value: str, field_name: str) -> str:
    """Return a normalised Tone/Target value or raise :class:`ValidationError`."""
    cleaned = " ".join(value.split())
    if not cleaned:
        raise ValidationError(f"{field_name} must not be empty")
    return cleaned


@dataclass(frozen=True, slots=True)
class Buddy:
    """A reusable teaching configuration."""

    id: str
    name: str
    target: str
    tone: str
    traits: tuple[str, ...]
    course_id: str | None
    created_at: datetime
    updated_at: datetime

    @property
    def is_course_grounded(self) -> bool:
        return self.course_id is not None


@dataclass(frozen=True, slots=True)
class BuddySnapshot:
    """The configuration a conversation was created with."""

    snapshot_version: int
    buddy_id: str
    buddy_name: str
    target: str
    tone: str
    traits: tuple[str, ...]
    course_id: str | None

    @classmethod
    def from_buddy(cls, buddy: Buddy) -> BuddySnapshot:
        return cls(
            snapshot_version=SNAPSHOT_VERSION,
            buddy_id=buddy.id,
            buddy_name=buddy.name,
            target=buddy.target,
            tone=buddy.tone,
            traits=buddy.traits,
            course_id=buddy.course_id,
        )

    @property
    def is_course_grounded(self) -> bool:
        """Course grounding is decided by this field only — never by the Buddy's name."""
        return self.course_id is not None

    def to_json(self) -> str:
        return json.dumps(
            {
                "snapshot_version": self.snapshot_version,
                "buddy_id": self.buddy_id,
                "buddy_name": self.buddy_name,
                "target": self.target,
                "tone": self.tone,
                "traits": list(self.traits),
                "course_id": self.course_id,
            },
            ensure_ascii=False,
            sort_keys=True,
        )

    @classmethod
    def from_json(cls, raw: str) -> BuddySnapshot:
        payload = json.loads(raw)
        return cls(
            snapshot_version=int(payload["snapshot_version"]),
            buddy_id=str(payload["buddy_id"]),
            buddy_name=str(payload["buddy_name"]),
            target=str(payload["target"]),
            tone=str(payload["tone"]),
            traits=tuple(str(trait) for trait in payload.get("traits", [])),
            course_id=None if payload.get("course_id") is None else str(payload["course_id"]),
        )
