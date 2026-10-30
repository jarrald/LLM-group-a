"""State passed through the chat graph."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypedDict

from app.domain.buddy import BuddySnapshot
from app.domain.conversation import Message
from app.domain.retrieval import RetrievalResult
from app.prompts.builder import PromptBundle, TaskSpec


class StudyGraphState(TypedDict, total=False):
    """Inputs and outputs of one chat turn.

    Nodes return partial updates: only the keys they produce.
    """

    snapshot: BuddySnapshot
    task: TaskSpec
    user_message: str
    history: list[Message]

    #: When set, the generate node streams tokens to this callback as well as returning
    #: the full answer (used by the Streamlit chat).
    on_token: Callable[[str], None]

    retrieval: RetrievalResult
    prompt: PromptBundle
    answer: str
    model: str
