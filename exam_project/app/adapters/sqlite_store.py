"""SQLite persistence for Buddies, conversations and messages.

Rules (see ``40-stack-and-architecture.md``): foreign keys on, WAL journal, one short-lived
connection per operation, explicit transactions, UTC ISO-8601 timestamps, and the Buddy
snapshot stored as JSON with its version.
"""

from __future__ import annotations

import json
import logging
import sqlite3
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from app.domain.buddy import Buddy, BuddySnapshot
from app.domain.conversation import Conversation, Message, MessageRole, RetrievalStatus, sources_from_json, sources_to_json
from app.domain.course import Course
from app.errors import PersistenceError, ValidationError

logger = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS courses (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    description     TEXT NOT NULL DEFAULT '',
    collection_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS buddies (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    target      TEXT NOT NULL,
    tone        TEXT NOT NULL,
    traits      TEXT NOT NULL,
    course_id   TEXT REFERENCES courses(id),
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conversations (
    id               TEXT PRIMARY KEY,
    title            TEXT NOT NULL,
    buddy_id         TEXT,
    buddy_snapshot   TEXT NOT NULL,
    snapshot_version INTEGER NOT NULL,
    course_id        TEXT,
    created_at       TEXT NOT NULL,
    updated_at       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id               TEXT PRIMARY KEY,
    conversation_id  TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role             TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content          TEXT NOT NULL,
    created_at       TEXT NOT NULL,
    sequence         INTEGER NOT NULL,
    retrieval_status TEXT NOT NULL DEFAULT 'skipped'
                     CHECK (retrieval_status IN ('ok', 'empty', 'failed', 'skipped')),
    sources          TEXT,
    model            TEXT,
    prompt_version   TEXT,
    retrieval_top_k  INTEGER
);

CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages (conversation_id, sequence);
CREATE INDEX IF NOT EXISTS idx_conversations_updated ON conversations (updated_at DESC);
"""


def new_id() -> str:
    """A unique identifier for stored rows."""
    return uuid.uuid4().hex


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SqliteStore:
    """Repository for all application data. One instance per process is enough."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialise()

    def initialise(self) -> None:
        try:
            with self._connect() as connection:
                connection.execute("PRAGMA journal_mode = WAL")
                connection.executescript(_SCHEMA)
                self._apply_additive_migrations(connection)
        except sqlite3.Error as exc:
            raise PersistenceError(f"Cannot initialise the database at {self.path}: {exc}") from exc

    @staticmethod
    def _apply_additive_migrations(connection: sqlite3.Connection) -> None:
        """Add columns that were introduced after the first schema, without touching data."""
        existing = {row["name"] for row in connection.execute("PRAGMA table_info(messages)").fetchall()}
        if "retrieval_top_k" not in existing:
            connection.execute("ALTER TABLE messages ADD COLUMN retrieval_top_k INTEGER")
            logger.info("migrated: added messages.retrieval_top_k")

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    # --- courses -------------------------------------------------------------------

    def upsert_course(self, course: Course) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO courses (id, name, description, collection_name) VALUES (?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET name = excluded.name, description = excluded.description, collection_name = excluded.collection_name",
                (course.id, course.name, course.description, course.collection_name),
            )

    def list_courses(self) -> list[Course]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM courses ORDER BY name").fetchall()
        return [Course(id=row["id"], name=row["name"], description=row["description"], collection_name=row["collection_name"]) for row in rows]

    # --- buddies -------------------------------------------------------------------

    def create_buddy(self, buddy: Buddy) -> None:
        with self._connect() as connection:
            try:
                connection.execute(
                    "INSERT INTO buddies (id, name, target, tone, traits, course_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (buddy.id, buddy.name, buddy.target, buddy.tone, json.dumps(list(buddy.traits)), buddy.course_id, buddy.created_at.isoformat(), buddy.updated_at.isoformat()),
                )
            except sqlite3.IntegrityError as exc:
                raise ValidationError(f"Cannot save the Buddy: {exc}") from exc

    def update_buddy(self, buddy: Buddy) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE buddies SET name = ?, target = ?, tone = ?, traits = ?, course_id = ?, updated_at = ? WHERE id = ?",
                (buddy.name, buddy.target, buddy.tone, json.dumps(list(buddy.traits)), buddy.course_id, buddy.updated_at.isoformat(), buddy.id),
            )
            if cursor.rowcount == 0:
                raise ValidationError(f"Unknown Buddy id: {buddy.id}")

    def get_buddy(self, buddy_id: str) -> Buddy:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM buddies WHERE id = ?", (buddy_id,)).fetchone()
        if row is None:
            raise ValidationError(f"Unknown Buddy id: {buddy_id}")
        return self._row_to_buddy(row)

    def list_buddies(self) -> list[Buddy]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM buddies ORDER BY updated_at DESC").fetchall()
        return [self._row_to_buddy(row) for row in rows]

    def delete_buddy(self, buddy_id: str) -> None:
        """Delete a Buddy; conversations keep their snapshots (FR-10)."""
        with self._connect() as connection:
            connection.execute("DELETE FROM buddies WHERE id = ?", (buddy_id,))

    @staticmethod
    def _row_to_buddy(row: sqlite3.Row) -> Buddy:
        return Buddy(
            id=row["id"],
            name=row["name"],
            target=row["target"],
            tone=row["tone"],
            traits=tuple(json.loads(row["traits"])),
            course_id=row["course_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    # --- conversations -------------------------------------------------------------

    def create_conversation(self, conversation: Conversation) -> None:
        snapshot = conversation.buddy_snapshot
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO conversations (id, title, buddy_id, buddy_snapshot, snapshot_version, course_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    conversation.id,
                    conversation.title,
                    snapshot.buddy_id,
                    snapshot.to_json(),
                    snapshot.snapshot_version,
                    snapshot.course_id,
                    conversation.created_at.isoformat(),
                    conversation.updated_at.isoformat(),
                ),
            )

    def get_conversation(self, conversation_id: str) -> Conversation:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,)).fetchone()
        if row is None:
            raise ValidationError(f"Unknown conversation id: {conversation_id}")
        return self._row_to_conversation(row)

    def list_conversations(self) -> list[Conversation]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM conversations ORDER BY updated_at DESC").fetchall()
        return [self._row_to_conversation(row) for row in rows]

    def delete_conversation(self, conversation_id: str) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))

    @staticmethod
    def _row_to_conversation(row: sqlite3.Row) -> Conversation:
        return Conversation(
            id=row["id"],
            title=row["title"],
            buddy_snapshot=BuddySnapshot.from_json(row["buddy_snapshot"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    # --- messages ------------------------------------------------------------------

    def add_message(self, message: Message) -> None:
        """Append a message to its conversation and bump the conversation's timestamp."""
        with self._connect() as connection:
            try:
                sequence_row = connection.execute(
                    "SELECT COALESCE(MAX(sequence), 0) + 1 FROM messages WHERE conversation_id = ?",
                    (message.conversation_id,),
                ).fetchone()
                connection.execute(
                    "INSERT INTO messages (id, conversation_id, role, content, created_at, sequence, retrieval_status, sources, model, prompt_version, retrieval_top_k) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        message.id,
                        message.conversation_id,
                        message.role.value,
                        message.content,
                        message.created_at.isoformat(),
                        int(sequence_row[0]),
                        message.retrieval_status.value,
                        sources_to_json(message.sources),
                        message.model,
                        message.prompt_version,
                        message.retrieval_top_k,
                    ),
                )
                connection.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (message.created_at.isoformat(), message.conversation_id))
            except sqlite3.IntegrityError as exc:
                raise ValidationError(f"Cannot save the message: {exc}") from exc

    def list_messages(self, conversation_id: str) -> list[Message]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM messages WHERE conversation_id = ? ORDER BY sequence", (conversation_id,)).fetchall()
        return [self._row_to_message(row) for row in rows]

    @staticmethod
    def _row_to_message(row: sqlite3.Row) -> Message:
        return Message(
            id=row["id"],
            conversation_id=row["conversation_id"],
            role=MessageRole(row["role"]),
            content=row["content"],
            created_at=datetime.fromisoformat(row["created_at"]),
            retrieval_status=RetrievalStatus(row["retrieval_status"]),
            sources=sources_from_json(row["sources"]),
            model=row["model"],
            prompt_version=row["prompt_version"],
            retrieval_top_k=None if row["retrieval_top_k"] is None else int(row["retrieval_top_k"]),
        )
