"""Tests for the 4T prompt builder: dimensions stay separate and visible."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.config import PROJECT_ROOT
from app.domain.buddy import Buddy, BuddySnapshot
from app.errors import ConfigError
from app.prompts.builder import PROMPT_VERSION, PromptBuilder, TaskSpec

PROMPTS_DIR = PROJECT_ROOT / "app" / "prompts"


def make_snapshot(**overrides: object) -> BuddySnapshot:
    now = datetime.now(timezone.utc)
    values = {
        "id": "buddy-1",
        "name": "Patient Tutor",
        "target": "Beginner with no prior knowledge",
        "tone": "Friendly and conversational",
        "traits": ("Patient", "Supportive"),
        "course_id": None,
        "created_at": now,
        "updated_at": now,
    }
    values.update(overrides)
    return BuddySnapshot.from_buddy(Buddy(**values))  # type: ignore[arg-type]


@pytest.fixture
def builder() -> PromptBuilder:
    return PromptBuilder(PROMPTS_DIR)


def test_system_prompt_contains_all_four_dimensions(builder: PromptBuilder) -> None:
    bundle = builder.build(snapshot=make_snapshot(), task=TaskSpec.from_preset("Explain a concept"), user_message="What is overfitting?")

    assert set(bundle.dimensions) == {"Task", "Tone", "Traits", "Target"}
    assert bundle.dimensions["Tone"] == "Friendly and conversational"
    assert bundle.dimensions["Traits"] == "Patient, Supportive"
    assert bundle.dimensions["Target"] == "Beginner with no prior knowledge"

    for value in ("Explain a concept", "Friendly and conversational", "Patient, Supportive", "Beginner with no prior knowledge"):
        assert value in bundle.system
    for heading in ("# Task", "# Tone", "# Traits", "# Target"):
        assert heading in bundle.system


def test_changing_one_dimension_leaves_the_others_untouched(builder: PromptBuilder) -> None:
    baseline = builder.build(snapshot=make_snapshot(), task=TaskSpec.from_preset("Explain a concept"), user_message="hi")
    changed = builder.build(snapshot=make_snapshot(tone="Concise and direct"), task=TaskSpec.from_preset("Explain a concept"), user_message="hi")

    assert changed.dimensions["Tone"] == "Concise and direct"
    assert changed.dimensions["Traits"] == baseline.dimensions["Traits"]
    assert changed.dimensions["Target"] == baseline.dimensions["Target"]
    assert changed.dimensions["Task"] == baseline.dimensions["Task"]


def test_task_changes_without_changing_the_buddy(builder: PromptBuilder) -> None:
    snapshot = make_snapshot()

    explain = builder.build(snapshot=snapshot, task=TaskSpec.from_preset("Explain a concept"), user_message="hi")
    quiz = builder.build(snapshot=snapshot, task=TaskSpec.from_preset("Quiz me"), user_message="hi")

    assert explain.dimensions["Task"] != quiz.dimensions["Task"]
    assert explain.dimensions["Tone"] == quiz.dimensions["Tone"]
    assert explain.dimensions["Traits"] == quiz.dimensions["Traits"]
    assert explain.dimensions["Target"] == quiz.dimensions["Target"]


def test_missing_dimension_is_visible_in_the_rendered_prompt(tmp_path: Path) -> None:
    """A template that forgets a dimension cannot silently look complete."""
    (tmp_path / "system_v1.md").write_text("Task: {{task}}\nTone: {{tone}}\n", encoding="utf-8")
    (tmp_path / "context_block_v1.md").write_text("{{passages}}\n", encoding="utf-8")

    bundle = PromptBuilder(tmp_path).build(snapshot=make_snapshot(), task=TaskSpec.from_preset(), user_message="hi")

    assert "Target" not in bundle.system
    assert "Beginner with no prior knowledge" not in bundle.system


def test_prompt_version_is_exposed(builder: PromptBuilder) -> None:
    bundle = builder.build(snapshot=make_snapshot(), task=TaskSpec.from_preset(), user_message="hi")

    assert bundle.prompt_version == PROMPT_VERSION == "system_v1"


def test_missing_template_raises_config_error(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="Prompt template not found"):
        PromptBuilder(tmp_path).build(snapshot=make_snapshot(), task=TaskSpec.from_preset(), user_message="hi")


def test_unresolved_placeholder_raises_config_error(tmp_path: Path) -> None:
    (tmp_path / "system_v1.md").write_text("Task: {{task}}\nUnknown: {{mystery}}\n", encoding="utf-8")
    (tmp_path / "context_block_v1.md").write_text("{{passages}}\n", encoding="utf-8")

    with pytest.raises(ConfigError, match="unresolved placeholders: mystery"):
        PromptBuilder(tmp_path).build(snapshot=make_snapshot(), task=TaskSpec.from_preset(), user_message="hi")


def test_task_spec_rejects_unknown_preset() -> None:
    with pytest.raises(ConfigError, match="Unknown task preset"):
        TaskSpec.from_preset("Do my homework")


def test_task_spec_custom_instruction() -> None:
    spec = TaskSpec.custom("  compare   two approaches ")

    assert spec.instruction == "compare two approaches"
    assert spec.name == "Custom task"
