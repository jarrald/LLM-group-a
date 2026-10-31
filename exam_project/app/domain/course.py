"""Courses: the knowledge base a Buddy can be grounded in."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_COURSE_ID = "llms_for_devs"
DEFAULT_COURSE_NAME = "LLMs for Developers"
DEFAULT_COURSE_DESCRIPTION = "Course lectures, converted to Markdown, indexed for retrieval."


@dataclass(frozen=True, slots=True)
class Course:
    """A course whose material is retrievable."""

    id: str
    name: str
    description: str
    collection_name: str

    @property
    def display_name(self) -> str:
        return self.name
