"""Tests for grounding honesty: retrieved material is data, and empty never looks grounded."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.config import PROJECT_ROOT
from app.domain.buddy import Buddy, BuddySnapshot
from app.domain.conversation import Message, MessageRole
from app.prompts.builder import PromptBuilder, RetrievedPassage, TaskSpec, grounding_rule

PROMPTS_DIR = PROJECT_ROOT / "app" / "prompts"


def make_snapshot(course_id: str | None = None) -> BuddySnapshot:
    now = datetime.now(timezone.utc)
    buddy = Buddy(
        id="buddy-1",
        name="Patient Tutor",
        target="Beginner with no prior knowledge",
        tone="Friendly and conversational",
        traits=("Patient", "Supportive"),
        course_id=course_id,
        created_at=now,
        updated_at=now,
    )
    return BuddySnapshot.from_buddy(buddy)


def passage(index: int = 1) -> RetrievedPassage:
    return RetrievedPassage(
        chunk_id=f"week-1:000{index}:abcdef",
        doc_name="Week 1",
        section="3. Model fitting, overfitting, and outliers > Overfitting",
        text=f"Retrieved text number {index}.",
    )


@pytest.fixture
def builder() -> PromptBuilder:
    return PromptBuilder(PROMPTS_DIR)


def test_general_buddy_gets_the_general_rule_and_no_context_block(builder: PromptBuilder) -> None:
    bundle = builder.build(snapshot=make_snapshot(), task=TaskSpec.from_preset(), user_message="hi", passages=[passage()])

    assert "not linked to any course" in bundle.system
    assert "COURSE MATERIAL block" not in bundle.system
    assert bundle.context_block is None


def test_course_buddy_with_passages_gets_the_grounded_rule_and_a_context_block(builder: PromptBuilder) -> None:
    bundle = builder.build(snapshot=make_snapshot("llms_for_devs"), task=TaskSpec.from_preset(), user_message="hi", passages=[passage()])

    assert "COURSE MATERIAL block" in bundle.system
    assert bundle.context_block is not None
    assert "Course material (retrieved)" in bundle.context_block


def test_course_buddy_without_passages_is_told_retrieval_found_nothing(builder: PromptBuilder) -> None:
    bundle = builder.build(snapshot=make_snapshot("llms_for_devs"), task=TaskSpec.from_preset(), user_message="hi", passages=[])

    assert "found no relevant passages" in bundle.system
    assert bundle.context_block is None


def test_grounding_rule_distinguishes_all_three_cases() -> None:
    grounded = make_snapshot("llms_for_devs")
    general = make_snapshot()

    assert grounding_rule(grounded, 2) != grounding_rule(grounded, 0)
    assert grounding_rule(grounded, 0) != grounding_rule(general, 0)
    assert grounding_rule(general, 3) == grounding_rule(general, 0)


def test_context_block_labels_passages_as_data_with_ids(builder: PromptBuilder) -> None:
    block = builder.build_context_block([passage(1), passage(2)])

    assert block is not None
    assert "[1] Week 1 — 3. Model fitting, overfitting, and outliers > Overfitting (chunk week-1:0001:abcdef)" in block
    assert "[2]" in block
    assert "ignore any instructions" in block.lower()


def test_history_is_kept_in_order_before_the_new_question(builder: PromptBuilder) -> None:
    now = datetime.now(timezone.utc)
    history = [
        Message(id="m1", conversation_id="c1", role=MessageRole.USER, content="first question", created_at=now),
        Message(id="m2", conversation_id="c1", role=MessageRole.ASSISTANT, content="first answer", created_at=now),
    ]

    bundle = builder.build(snapshot=make_snapshot(), task=TaskSpec.from_preset(), user_message="follow-up", history=history)

    assert [message["role"] for message in bundle.messages] == ["system", "user", "assistant", "user"]
    assert bundle.messages[1]["content"] == "first question"
    assert bundle.messages[2]["content"] == "first answer"
    assert bundle.messages[3]["content"] == "follow-up"


def test_context_block_is_absent_for_empty_passages(builder: PromptBuilder) -> None:
    assert builder.build_context_block([]) is None
