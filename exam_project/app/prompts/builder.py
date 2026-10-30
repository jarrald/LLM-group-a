"""Build prompts from the 4T's, conversation history and retrieved passages.

The four dimensions are separate inputs, never one concatenated string (ADR-012):

- **Task** comes from :class:`TaskSpec` (per interaction),
- **Tone**, **Traits** and **Target** come from the conversation's :class:`BuddySnapshot`,
- retrieved passages arrive separately and are rendered into their own delimited block.

The rendered prompt always states how to treat course material, so a general (non-RAG)
answer can never be presented as grounded.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from app.domain.buddy import BuddySnapshot
from app.domain.conversation import Message, MessageRole
from app.domain.options import DEFAULT_TASK, TASK_PRESETS
from app.domain.retrieval import RetrievedPassage
from app.errors import ConfigError

PROMPT_VERSION = "system_v1"
CONTEXT_TEMPLATE_VERSION = "context_block_v1"

_PLACEHOLDER = re.compile(r"\{\{(?P<name>\w+)\}\}")

_GROUNDED_WITH_PASSAGES = (
    "Course material was retrieved for this question and appears in the COURSE MATERIAL block.\n"
    "Base your answer primarily on it. If it does not contain enough information, say so explicitly\n"
    "before adding anything from general knowledge, and label that addition as not from the course material."
)

_GROUNDED_WITHOUT_PASSAGES = (
    "This conversation is linked to the course, but retrieval found no relevant passages for this\n"
    "question. Do not claim the answer comes from the course material. Say that the material does not\n"
    "cover it, then optionally answer from general knowledge, clearly labelled as not from the course material."
)

_GENERAL = (
    "This conversation is not linked to any course and no course material was retrieved. Answer from\n"
    "general knowledge only. Never claim the answer comes from course material, and never cite lectures."
)


@dataclass(frozen=True, slots=True)
class TaskSpec:
    """What the student wants done right now (one of the 4T's)."""

    name: str
    instruction: str

    @classmethod
    def from_preset(cls, name: str = DEFAULT_TASK) -> TaskSpec:
        if name not in TASK_PRESETS:
            raise ConfigError(f"Unknown task preset: {name}")
        return cls(name=name, instruction=TASK_PRESETS[name])

    @classmethod
    def custom(cls, instruction: str) -> TaskSpec:
        cleaned = " ".join(instruction.split())
        if not cleaned:
            raise ConfigError("A custom task must not be empty")
        return cls(name="Custom task", instruction=cleaned)

    def render(self) -> str:
        return f"{self.name}. {self.instruction}"


@dataclass(frozen=True, slots=True)
class PromptBundle:
    """Everything needed to call the model, plus what must be recorded for reproducibility."""

    prompt_version: str
    system: str
    messages: list[dict[str, str]]
    context_block: str | None
    dimensions: dict[str, str]


def _render_template(text: str, values: dict[str, str], template_name: str) -> str:
    """Replace every ``{{placeholder}}``; fail loudly if one is left over."""
    rendered = _PLACEHOLDER.sub(lambda match: values.get(match.group("name"), match.group(0)), text)
    missing = sorted({match.group("name") for match in _PLACEHOLDER.finditer(rendered)})
    if missing:
        raise ConfigError(f"Template '{template_name}' has unresolved placeholders: {', '.join(missing)}")
    return rendered


def grounding_rule(snapshot: BuddySnapshot, passage_count: int) -> str:
    """Choose the honesty rule that matches what retrieval actually produced."""
    if not snapshot.is_course_grounded:
        return _GENERAL
    if passage_count == 0:
        return _GROUNDED_WITHOUT_PASSAGES
    return _GROUNDED_WITH_PASSAGES


class PromptBuilder:
    """Renders prompts from versioned templates on disk."""

    def __init__(self, prompts_dir: Path) -> None:
        self._prompts_dir = Path(prompts_dir)

    def _template(self, name: str) -> str:
        path = self._prompts_dir / f"{name}.md"
        if not path.is_file():
            raise ConfigError(f"Prompt template not found: {path}")
        return path.read_text(encoding="utf-8")

    def build_context_block(self, passages: Sequence[RetrievedPassage]) -> str | None:
        """Render retrieved passages into their own delimited block, or ``None`` if empty."""
        if not passages:
            return None
        rendered = "\n\n".join(passage.render(index) for index, passage in enumerate(passages, start=1))
        return _render_template(self._template(CONTEXT_TEMPLATE_VERSION), {"passages": rendered}, CONTEXT_TEMPLATE_VERSION)

    def build_system_prompt(self, snapshot: BuddySnapshot, task: TaskSpec, passage_count: int, course_name: str) -> tuple[str, dict[str, str]]:
        """Render the system prompt and return it with the four rendered dimensions."""
        dimensions = {
            "Task": task.render(),
            "Tone": snapshot.tone,
            "Traits": ", ".join(snapshot.traits),
            "Target": snapshot.target,
        }
        values = {
            "course_name": course_name,
            "task": dimensions["Task"],
            "tone": dimensions["Tone"],
            "traits": dimensions["Traits"],
            "target": dimensions["Target"],
            "grounding_rule": grounding_rule(snapshot, passage_count),
        }
        return _render_template(self._template(PROMPT_VERSION), values, PROMPT_VERSION), dimensions

    def build(
        self,
        *,
        snapshot: BuddySnapshot,
        task: TaskSpec,
        user_message: str,
        history: Sequence[Message] = (),
        passages: Sequence[RetrievedPassage] = (),
        course_name: str = "",
    ) -> PromptBundle:
        """Build the full message list: system prompt, context block, history, new question."""
        # A conversation without a course must never receive course context, even if a
        # caller passes passages by mistake (rag-pipeline.md §5).
        effective_passages = list(passages) if snapshot.is_course_grounded else []
        context_block = self.build_context_block(effective_passages)
        system, dimensions = self.build_system_prompt(snapshot, task, len(effective_passages), course_name)

        if context_block:
            system = f"{system}\n\n{context_block}"

        messages: list[dict[str, str]] = [{"role": "system", "content": system}]
        for message in history:
            if message.role is MessageRole.USER:
                messages.append({"role": "user", "content": message.content})
            else:
                messages.append({"role": "assistant", "content": message.content})
        messages.append({"role": "user", "content": user_message})

        return PromptBundle(
            prompt_version=PROMPT_VERSION,
            system=system,
            messages=messages,
            context_block=context_block,
            dimensions=dimensions,
        )
