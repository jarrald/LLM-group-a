"""Chat page: pick a Buddy, start a conversation, ask a question.

Behaviour follows the docs: the Buddy is chosen when a conversation is *created* and its
configuration is frozen in a snapshot (ADR-010), the Task is chosen per message (ADR-017),
and the mode badge plus sources make grounding visible (D-02, D-04).
"""

from __future__ import annotations

import streamlit as st

from app.domain.buddy import Buddy
from app.domain.conversation import Message, MessageRole
from app.domain.options import TASK_PRESETS
from app.errors import StudyGraphError
from app.prompts.builder import TaskSpec
from app.services.chat_service import TurnResult
from app.ui.clients import Services, get_services
from app.ui.components import config_html, inject_css, mode_pill, page_header, retrieval_notice, sources_block

CONVERSATION_KEY = "conversation_id"
INPUT_PLACEHOLDER = "Ask your study buddy…"


def _sidebar(services: Services) -> None:
    with st.sidebar:
        st.markdown("### ✦ StudyGraph")
        st.markdown("<div class='sg-caption'>My study sessions</div>", unsafe_allow_html=True)

        conversations = services.chat.list_conversations()
        if conversations:
            labels = {f"{conversation.title[:34]} · {conversation.id[:4]}": conversation.id for conversation in conversations}
            current = next((label for label, identifier in labels.items() if identifier == st.session_state.get(CONVERSATION_KEY)), None)
            choice = st.selectbox("Conversation", options=list(labels), index=list(labels).index(current) if current else 0, label_visibility="collapsed")
            if st.button("Open conversation", use_container_width=True):
                st.session_state[CONVERSATION_KEY] = labels[choice]
                st.rerun()
        else:
            st.caption("No conversations yet.")

        st.divider()
        st.markdown("<div class='sg-caption'>New conversation</div>", unsafe_allow_html=True)
        buddies = services.buddies.list_buddies()
        if not buddies:
            st.caption("Create a Buddy on the Buddies page first.")
            return
        names = {buddy.name: buddy.id for buddy in buddies}
        buddy_label = st.selectbox("Buddy", options=list(names), label_visibility="collapsed")
        if st.button("Start conversation", type="primary", use_container_width=True):
            buddy: Buddy = services.buddies.get_buddy(names[buddy_label])
            conversation = services.chat.start_conversation(buddy)
            st.session_state[CONVERSATION_KEY] = conversation.id
            st.rerun()
        st.caption("The Buddy's Traits, Tone, Target and course material are frozen for the conversation.")


def _render_message(message: Message) -> None:
    with st.chat_message("user" if message.role is MessageRole.USER else "assistant"):
        st.markdown(message.content)
        if message.role is MessageRole.ASSISTANT:
            retrieval_notice(message.retrieval_status)
            sources_block(message.sources, message.retrieval_status)


def _handle_turn(services: Services, conversation_id: str, question: str, task: TaskSpec) -> None:
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        chunks: list[str] = []

        def on_token(token: str) -> None:
            chunks.append(token)
            placeholder.markdown("".join(chunks) + "▌")

        result: TurnResult | None = None
        try:
            result = services.chat.send_message(conversation_id, question, task=task, on_token=on_token)
        except StudyGraphError as exc:
            placeholder.empty()
            st.error(str(exc), icon="⚠️")
            st.caption("Nothing was saved for that message — start the service and ask again.")

        if result is not None:
            placeholder.markdown(result.assistant_message.content)
            retrieval_notice(result.retrieval.status, result.retrieval.error)
            sources_block(result.assistant_message.sources, result.retrieval.status)
            st.caption(f"Task: {result.prompt.dimensions['Task']} · model `{result.assistant_message.model}` · prompt `{result.assistant_message.prompt_version}`")


def render() -> None:
    services = get_services()
    inject_css()
    _sidebar(services)

    conversation_id = st.session_state.get(CONVERSATION_KEY)
    if not conversation_id:
        page_header("Chat with your buddy", "Pick a Buddy in the sidebar and start a conversation.")
        st.info("Your Buddy decides how the assistant teaches; you choose the task with every message.", icon="💬")
        return

    try:
        conversation = services.chat.get_conversation(conversation_id)
    except StudyGraphError:
        st.session_state.pop(CONVERSATION_KEY, None)
        st.warning("That conversation no longer exists.", icon="🗑️")
        return

    snapshot = conversation.buddy_snapshot
    grounded = snapshot.is_course_grounded

    header, badge = st.columns([4, 1])
    with header:
        st.markdown(f"### {conversation.title}")
        st.markdown(f"<div class='sg-muted'>{snapshot.buddy_name}</div>", unsafe_allow_html=True)
    with badge:
        st.markdown(mode_pill(grounded), unsafe_allow_html=True)

    with st.expander("Active configuration (frozen when the conversation started)"):
        st.markdown(config_html(snapshot, services.course_name), unsafe_allow_html=True)

    messages = services.chat.get_messages(conversation_id)
    if not messages:
        st.info("This conversation is empty. Ask your first question below.", icon="✨")
    for message in messages:
        _render_message(message)

    task_name = st.selectbox("Task for your next message", options=list(TASK_PRESETS), index=0)
    question = st.chat_input(INPUT_PLACEHOLDER)
    if question:
        _handle_turn(services, conversation_id, question, TaskSpec.from_preset(task_name))


if __name__ == "__main__":
    render()
