"""Use case: one chat turn, from the user's message to a stored, sourced answer."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.adapters.sqlite_store import SqliteStore, new_id, utc_now
from app.config import Config
from app.domain.buddy import Buddy
from app.domain.conversation import Conversation, Message, MessageRole, RetrievalStatus, validate_message_content
from app.domain.retrieval import RetrievalResult
from app.prompts.builder import PromptBundle, TaskSpec

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class TurnResult:
    """What one chat turn produced, for the UI and for the evaluation."""

    conversation_id: str
    user_message: Message
    assistant_message: Message
    prompt: PromptBundle
    retrieval: RetrievalResult

    @property
    def is_grounded(self) -> bool:
        return self.retrieval.status is RetrievalStatus.OK


class ChatService:
    """Runs the graph and persists both messages with their provenance."""

    def __init__(self, store: SqliteStore, graph: Any, config: Config) -> None:
        self._store = store
        self._graph = graph
        self._config = config

    def start_conversation(self, buddy: Buddy, title: str | None = None) -> Conversation:
        """Create a conversation and freeze the Buddy configuration into a snapshot."""
        from app.domain.buddy import BuddySnapshot

        now = utc_now()
        conversation = Conversation(
            id=new_id(),
            title=title or f"Chat with {buddy.name}",
            buddy_snapshot=BuddySnapshot.from_buddy(buddy),
            created_at=now,
            updated_at=now,
        )
        self._store.create_conversation(conversation)
        logger.info("started conversation %s from buddy %s", conversation.id, buddy.id)
        return conversation

    def list_conversations(self) -> list[Conversation]:
        return self._store.list_conversations()

    def get_conversation(self, conversation_id: str) -> Conversation:
        return self._store.get_conversation(conversation_id)

    def get_messages(self, conversation_id: str) -> list[Message]:
        return self._store.list_messages(conversation_id)

    def send_message(self, conversation_id: str, content: str, task: TaskSpec | None = None, on_token: Callable[[str], None] | None = None) -> TurnResult:
        """Run one turn. Messages are stored only after the answer succeeded, so a failed
        turn leaves the conversation exactly as it was and can simply be retried.

        ``on_token`` streams the answer to a UI callback; the stored message is identical
        either way.
        """
        cleaned = validate_message_content(content)
        conversation = self._store.get_conversation(conversation_id)
        history = self._store.list_messages(conversation_id)

        state: dict[str, object] = {
            "snapshot": conversation.buddy_snapshot,
            "task": task or TaskSpec.from_preset(),
            "user_message": cleaned,
            "history": history,
        }
        if on_token is not None:
            state["on_token"] = on_token
        final_state: dict[str, object] = self._graph.invoke(state)

        prompt = final_state["prompt"]
        answer = str(final_state["answer"])
        retrieval = final_state.get("retrieval") or RetrievalResult.skipped()
        assert isinstance(prompt, PromptBundle)
        assert isinstance(retrieval, RetrievalResult)

        user_message = Message(id=new_id(), conversation_id=conversation_id, role=MessageRole.USER, content=cleaned, created_at=utc_now())
        assistant_message = Message(
            id=new_id(),
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=answer,
            created_at=utc_now(),
            retrieval_status=retrieval.status,
            sources=retrieval.sources if retrieval.is_grounded else (),
            model=str(final_state.get("model") or self._config.chat_model),
            prompt_version=prompt.prompt_version,
            retrieval_top_k=retrieval.top_k or None,
        )
        self._store.add_message(user_message)
        self._store.add_message(assistant_message)

        return TurnResult(
            conversation_id=conversation_id,
            user_message=user_message,
            assistant_message=assistant_message,
            prompt=prompt,
            retrieval=retrieval,
        )
