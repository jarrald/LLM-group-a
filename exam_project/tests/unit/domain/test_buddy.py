"""Tests for Buddy validation and the immutable snapshot."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.domain.buddy import SNAPSHOT_VERSION, Buddy, BuddySnapshot, validate_buddy_name, validate_dimension, validate_traits
from app.errors import ValidationError


def make_buddy(**overrides: object) -> Buddy:
    now = datetime.now(timezone.utc)
    values = {
        "id": "buddy-1",
        "name": "Patient Tutor",
        "target": "Beginner with no prior knowledge",
        "tone": "Friendly and conversational",
        "traits": ("Patient", "Supportive"),
        "course_id": "llms_for_devs",
        "created_at": now,
        "updated_at": now,
    }
    values.update(overrides)
    return Buddy(**values)  # type: ignore[arg-type]


def test_validate_buddy_name_collapses_whitespace() -> None:
    assert validate_buddy_name("  Patient   Tutor ") == "Patient Tutor"


def test_validate_buddy_name_rejects_empty() -> None:
    with pytest.raises(ValidationError, match="must not be empty"):
        validate_buddy_name("   ")


def test_validate_buddy_name_rejects_too_long() -> None:
    with pytest.raises(ValidationError, match="at most"):
        validate_buddy_name("x" * 61)


def test_validate_traits_deduplicates_case_insensitively() -> None:
    assert validate_traits(["Patient", "patient", " Analytical "]) == ("Patient", "Analytical")


def test_validate_traits_requires_at_least_one() -> None:
    with pytest.raises(ValidationError, match="at least one trait"):
        validate_traits(["  ", ""])


def test_validate_traits_rejects_too_many() -> None:
    with pytest.raises(ValidationError, match="at most"):
        validate_traits([f"trait {index}" for index in range(7)])


def test_validate_dimension_rejects_empty() -> None:
    with pytest.raises(ValidationError, match="Tone must not be empty"):
        validate_dimension(" ", "Tone")


def test_snapshot_copies_every_dimension() -> None:
    snapshot = BuddySnapshot.from_buddy(make_buddy())

    assert snapshot.snapshot_version == SNAPSHOT_VERSION
    assert snapshot.buddy_name == "Patient Tutor"
    assert snapshot.target == "Beginner with no prior knowledge"
    assert snapshot.tone == "Friendly and conversational"
    assert snapshot.traits == ("Patient", "Supportive")
    assert snapshot.course_id == "llms_for_devs"
    assert snapshot.is_course_grounded is True


def test_snapshot_marks_no_course_as_not_grounded() -> None:
    snapshot = BuddySnapshot.from_buddy(make_buddy(course_id=None))

    assert snapshot.is_course_grounded is False


def test_snapshot_json_round_trip() -> None:
    snapshot = BuddySnapshot.from_buddy(make_buddy())

    restored = BuddySnapshot.from_json(snapshot.to_json())

    assert restored == snapshot


def test_editing_a_buddy_does_not_change_an_existing_snapshot() -> None:
    buddy = make_buddy()
    snapshot = BuddySnapshot.from_buddy(buddy)

    edited = make_buddy(name="Exam Coach", tone="Concise and direct", traits=("Critical",), course_id=None)

    assert snapshot.buddy_name == "Patient Tutor"
    assert snapshot.tone == "Friendly and conversational"
    assert snapshot.traits == ("Patient", "Supportive")
    assert snapshot.course_id == "llms_for_devs"
    assert edited.name == "Exam Coach"
