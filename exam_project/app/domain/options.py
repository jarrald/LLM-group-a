"""Option lists shown in the Buddy form.

These are *suggestions*, not closed lists: the UI also accepts free text (buddy-design.md
§4). Task presets are data, never code paths (ADR-012).
"""

from __future__ import annotations

TARGET_OPTIONS: tuple[str, ...] = (
    "Beginner with no prior knowledge",
    "Student familiar with the fundamentals",
    "Advanced student",
    "Student preparing for an examination",
)

TONE_OPTIONS: tuple[str, ...] = (
    "Formal and academic",
    "Friendly and conversational",
    "Encouraging and supportive",
    "Concise and direct",
)

TRAIT_OPTIONS: tuple[str, ...] = (
    "Patient",
    "Analytical",
    "Critical",
    "Supportive",
    "Socratic",
    "Detail-oriented",
)

# Task is per interaction, not part of the Buddy (buddy-design.md §3.1).
TASK_PRESETS: dict[str, str] = {
    "Explain a concept": "Explain the requested concept clearly, building from what the student already knows.",
    "Summarise": "Summarise the material concisely, keeping the course's own terminology.",
    "Generate practice questions": "Generate practice questions with answers, increasing in difficulty.",
    "Quiz me": "Ask one question at a time and wait for the student's answer before continuing.",
    "Compare two approaches": "Compare the two approaches on the dimensions that matter, with a short conclusion.",
    "Review my answer": "Review the student's answer, state what is correct, and correct what is wrong.",
}

DEFAULT_TASK = "Explain a concept"

MAX_TRAITS = 6
MAX_TRAIT_LENGTH = 40
MAX_BUDDY_NAME_LENGTH = 60
