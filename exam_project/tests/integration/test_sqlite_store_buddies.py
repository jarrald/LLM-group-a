"""Integration tests: courses and Buddies survive a reconnect."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.adapters.sqlite_store import SqliteStore
from app.errors import ValidationError
from tests.integration.factories import COURSE, make_buddy


def test_course_is_seeded_once(store: SqliteStore) -> None:
    store.upsert_course(COURSE)

    assert [course.id for course in store.list_courses()] == ["llms_for_devs"]


def test_buddy_round_trip(store: SqliteStore) -> None:
    buddy = make_buddy(course_id="llms_for_devs")

    store.create_buddy(buddy)

    assert store.get_buddy(buddy.id) == buddy
    assert [stored.id for stored in store.list_buddies()] == [buddy.id]


def test_update_buddy_changes_the_reusable_configuration(store: SqliteStore) -> None:
    buddy = make_buddy()
    store.create_buddy(buddy)

    store.update_buddy(make_buddy(id=buddy.id, name="Exam Coach", traits=("Critical",)))

    assert store.get_buddy(buddy.id).name == "Exam Coach"
    assert store.get_buddy(buddy.id).traits == ("Critical",)


def test_update_unknown_buddy_raises_validation_error(store: SqliteStore) -> None:
    with pytest.raises(ValidationError, match="Unknown Buddy id"):
        store.update_buddy(make_buddy(id="missing"))


def test_unknown_buddy_raises_validation_error(store: SqliteStore) -> None:
    with pytest.raises(ValidationError, match="Unknown Buddy id"):
        store.get_buddy("does-not-exist")


def test_buddies_survive_a_reconnect(tmp_path: Path) -> None:
    path = tmp_path / "studygraph.db"
    first = SqliteStore(path)
    buddy = make_buddy()
    first.create_buddy(buddy)

    reopened = SqliteStore(path)

    assert reopened.get_buddy(buddy.id).name == "Patient Tutor"


def test_buddy_with_unknown_course_is_rejected(store: SqliteStore) -> None:
    with pytest.raises(ValidationError, match="Cannot save the Buddy"):
        store.create_buddy(make_buddy(course_id="not-a-course"))
