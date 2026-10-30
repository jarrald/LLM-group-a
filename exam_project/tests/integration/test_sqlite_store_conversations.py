"""Integration tests: conversations, snapshots and messages."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.adapters.sqlite_store import SqliteStore, new_id, utc_now
from app.domain.conversation import Message, MessageRole, RetrievalStatus, SourceReference
from app.errors import ValidationError
from tests.integration.factories import make_buddy, make_conversation


def test_conversation_keeps_its_snapshot_when_the_buddy_is_edited(store: SqliteStore) -> None:
    buddy = make_buddy(course_id="llms_for_devs")
    store.create_buddy(buddy)
    conversation = make_conversation(buddy)
    store.create_conversation(conversation)

    store.update_buddy(make_buddy(id=buddy.id, name="Exam Coach", course_id=None))

    stored = store.get_conversation(conversation.id)
    assert stored.buddy_snapshot.buddy_name == "Patient Tutor"
    assert stored.buddy_snapshot.course_id == "llms_for_devs"
    assert store.get_buddy(buddy.id).name == "Exam Coach"


def test_conversation_survives_buddy_deletion(store: SqliteStore) -> None:
    buddy = make_buddy()
    store.create_buddy(buddy)
    conversation = make_conversation(buddy)
    store.create_conversation(conversation)

    store.delete_buddy(buddy.id)

    assert store.get_conversation(conversation.id).buddy_snapshot.buddy_name == "Patient Tutor"
    assert store.list_buddies() == []


def test_unknown_conversation_raises_validation_error(store: SqliteStore) -> None:
    with pytest.raises(ValidationError, match="Unknown conversation id"):
        store.get_conversation("nope")


def test_messages_are_returned_in_order(store: SqliteStore) -> None:
    conversation = make_conversation(make_buddy())
    store.create_conversation(conversation)

    for index in range(3):
        store.add_message(
            Message(
                id=new_id(),
                conversation_id=conversation.id,
                role=MessageRole.USER if index % 2 == 0 else MessageRole.ASSISTANT,
                content=f"message {index}",
                created_at=utc_now(),
            )
        )

    assert [message.content for message in store.list_messages(conversation.id)] == ["message 0", "message 1", "message 2"]


def test_message_keeps_retrieval_status_and_sources(store: SqliteStore) -> None:
    buddy = make_buddy(course_id="llms_for_devs")
    store.create_buddy(buddy)
    conversation = make_conversation(buddy)
    store.create_conversation(conversation)
    source = SourceReference(chunk_id="week-1:0003:abcdef", doc_id="week-1", doc_name="Week 1", section="Overfitting", lecture=1, distance=0.53, snippet="Overfitting happens when…")

    store.add_message(
        Message(
            id=new_id(),
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content="An answer grounded in lecture 1.",
            created_at=utc_now(),
            retrieval_status=RetrievalStatus.OK,
            sources=(source,),
            model="llama3.2:3b",
            prompt_version="system_v1",
        )
    )

    stored = store.list_messages(conversation.id)[0]
    assert stored.retrieval_status is RetrievalStatus.OK
    assert stored.retrieval_status.is_grounded is True
    assert stored.sources == (source,)
    assert stored.model == "llama3.2:3b"
    assert stored.prompt_version == "system_v1"


def test_skipped_retrieval_is_not_grounded(store: SqliteStore) -> None:
    conversation = make_conversation(make_buddy())
    store.create_conversation(conversation)

    store.add_message(Message(id=new_id(), conversation_id=conversation.id, role=MessageRole.ASSISTANT, content="General answer.", created_at=utc_now()))

    assert store.list_messages(conversation.id)[0].retrieval_status.is_grounded is False


def test_message_for_unknown_conversation_raises_validation_error(store: SqliteStore) -> None:
    with pytest.raises(ValidationError, match="Cannot save the message"):
        store.add_message(Message(id=new_id(), conversation_id="missing", role=MessageRole.USER, content="hi", created_at=utc_now()))


def test_deleting_a_conversation_removes_its_messages(store: SqliteStore) -> None:
    conversation = make_conversation(make_buddy())
    store.create_conversation(conversation)
    store.add_message(Message(id=new_id(), conversation_id=conversation.id, role=MessageRole.USER, content="hi", created_at=utc_now()))

    store.delete_conversation(conversation.id)

    assert store.list_messages(conversation.id) == []


def test_conversation_list_is_ordered_by_recency(store: SqliteStore) -> None:
    older = make_conversation(make_buddy(), created_at=datetime(2026, 10, 1, tzinfo=timezone.utc), updated_at=datetime(2026, 10, 1, tzinfo=timezone.utc))
    newer = make_conversation(make_buddy(), created_at=datetime(2026, 10, 20, tzinfo=timezone.utc), updated_at=datetime(2026, 10, 20, tzinfo=timezone.utc))
    store.create_conversation(older)
    store.create_conversation(newer)

    assert [conversation.id for conversation in store.list_conversations()] == [newer.id, older.id]


def test_messages_survive_a_reconnect(tmp_path) -> None:
    path = tmp_path / "studygraph.db"
    first = SqliteStore(path)
    conversation = make_conversation(make_buddy())
    first.create_conversation(conversation)
    first.add_message(Message(id=new_id(), conversation_id=conversation.id, role=MessageRole.USER, content="does it persist?", created_at=utc_now()))

    reopened = SqliteStore(path)

    assert [message.content for message in reopened.list_messages(conversation.id)] == ["does it persist?"]
