"""Use case: manage reusable Buddies and the seeded course."""

from __future__ import annotations

import logging

from app.adapters.sqlite_store import SqliteStore, new_id, utc_now
from app.config import Config
from app.domain.buddy import Buddy, validate_buddy_name, validate_dimension, validate_traits
from app.domain.course import DEFAULT_COURSE_DESCRIPTION, DEFAULT_COURSE_NAME, Course
from app.errors import ValidationError

logger = logging.getLogger(__name__)

DEFAULT_TARGET = "Student familiar with the fundamentals"
DEFAULT_TONE = "Friendly and conversational"
DEFAULT_TRAITS: tuple[str, ...] = ("Patient", "Supportive")


class BuddyService:
    """Everything the UI needs to create, list and edit Buddies."""

    def __init__(self, store: SqliteStore, config: Config) -> None:
        self._store = store
        self._config = config

    @property
    def default_course_id(self) -> str:
        return self._config.course_id

    def seed_defaults(self) -> Course:
        """Ensure the single course and the default Buddy pair exist (FR-05, FR-14).

        The pair mirrors `design/rag-comparison.md` §3: identical Target/Tone/Traits, one
        with the course and one without, so the RAG comparison needs no setup.
        """
        course = Course(
            id=self._config.course_id,
            name=DEFAULT_COURSE_NAME,
            description=DEFAULT_COURSE_DESCRIPTION,
            collection_name=self._config.collection_name,
        )
        self._store.upsert_course(course)
        if not self._store.list_buddies():
            logger.info("seeding the default Buddy pair")
            for name, course_id in (("Patient Tutor", self._config.course_id), ("General Tutor", None)):
                self.create_buddy(name=name, target=DEFAULT_TARGET, tone=DEFAULT_TONE, traits=DEFAULT_TRAITS, course_id=course_id)
        return course

    def list_courses(self) -> list[Course]:
        return self._store.list_courses()

    def list_buddies(self) -> list[Buddy]:
        return self._store.list_buddies()

    def get_buddy(self, buddy_id: str) -> Buddy:
        return self._store.get_buddy(buddy_id)

    def create_buddy(self, *, name: str, target: str, tone: str, traits: list[str] | tuple[str, ...], course_id: str | None = None) -> Buddy:
        validated_course = self._validate_course(course_id)
        now = utc_now()
        buddy = Buddy(
            id=new_id(),
            name=validate_buddy_name(name),
            target=validate_dimension(target, "Target"),
            tone=validate_dimension(tone, "Tone"),
            traits=validate_traits(traits),
            course_id=validated_course,
            created_at=now,
            updated_at=now,
        )
        self._store.create_buddy(buddy)
        logger.info("created buddy %s (%s)", buddy.id, buddy.name)
        return buddy

    def update_buddy(self, buddy_id: str, *, name: str, target: str, tone: str, traits: list[str] | tuple[str, ...], course_id: str | None = None) -> Buddy:
        existing = self._store.get_buddy(buddy_id)
        validated_course = self._validate_course(course_id)
        updated = Buddy(
            id=existing.id,
            name=validate_buddy_name(name),
            target=validate_dimension(target, "Target"),
            tone=validate_dimension(tone, "Tone"),
            traits=validate_traits(traits),
            course_id=validated_course,
            created_at=existing.created_at,
            updated_at=utc_now(),
        )
        self._store.update_buddy(updated)
        return updated

    def delete_buddy(self, buddy_id: str) -> None:
        """Delete the reusable Buddy; existing conversations keep their snapshots."""
        self._store.delete_buddy(buddy_id)

    def _validate_course(self, course_id: str | None) -> str | None:
        if course_id is None or not course_id.strip():
            return None
        known = {course.id for course in self._store.list_courses()}
        if course_id not in known:
            raise ValidationError(f"Unknown course id: {course_id}")
        return course_id
