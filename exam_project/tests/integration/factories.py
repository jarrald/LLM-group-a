"""Shared builders for integration tests."""

from __future__ import annotations

from datetime import datetime, timezone

from app.adapters.sqlite_store import new_id, utc_now
from app.domain.buddy import Buddy, BuddySnapshot
from app.domain.conversation import Conversation
from app.domain.course import Course

COURSE = Course(id="llms_for_devs", name="LLMs for Developers", description="", collection_name="llms_for_devs_v1")


def make_buddy(**overrides: object) -> Buddy:
    now = datetime.now(timezone.utc)
    values = {
        "id": new_id(),
        "name": "Patient Tutor",
        "target": "Beginner with no prior knowledge",
        "tone": "Friendly and conversational",
        "traits": ("Patient", "Supportive"),
        "course_id": None,
        "created_at": now,
        "updated_at": now,
    }
    values.update(overrides)
    return Buddy(**values)  # type: ignore[arg-type]


def make_conversation(buddy: Buddy, **overrides: object) -> Conversation:
    now = utc_now()
    values = {
        "id": new_id(),
        "title": "Fitting a model",
        "buddy_snapshot": BuddySnapshot.from_buddy(buddy),
        "created_at": now,
        "updated_at": now,
    }
    values.update(overrides)
    return Conversation(**values)  # type: ignore[arg-type]
