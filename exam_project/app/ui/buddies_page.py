"""Buddies page: list, create and edit the reusable teaching configuration.

A Buddy carries the three T's (Traits, Tone, Target) plus the optional course material.
Task is *not* here — it is chosen per message in the chat (ADR-017).
"""

from __future__ import annotations

import streamlit as st

from app.domain.buddy import Buddy
from app.domain.options import MAX_TRAIT_LENGTH, TARGET_OPTIONS, TONE_OPTIONS, TRAIT_OPTIONS
from app.errors import StudyGraphError
from app.ui.clients import Services, get_services
from app.ui.components import buddy_card, inject_css, page_header

CUSTOM = "Custom…"
NO_COURSE = "None"


def _course_choices(services: Services) -> dict[str, str | None]:
    """Display label → course id, with 'None' first (the default, FR-05)."""
    choices: dict[str, str | None] = {NO_COURSE: None}
    for course in services.buddies.list_courses():
        choices[course.name] = course.id
    return choices


def _buddy_form(services: Services, buddy: Buddy | None) -> None:
    choices = _course_choices(services)
    labels = list(choices)
    current_course = next((label for label, value in choices.items() if value == (buddy.course_id if buddy else None)), NO_COURSE)

    with st.form(key=f"buddy-form-{buddy.id if buddy else 'new'}"):
        name = st.text_input("Buddy name", value=buddy.name if buddy else "")
        st.markdown("<div class='sg-caption'>The three T's</div>", unsafe_allow_html=True)

        traits_default = list(buddy.traits) if buddy else ["Patient"]
        known = [trait for trait in traits_default if trait in TRAIT_OPTIONS]
        preselected = st.multiselect("Traits", options=TRAIT_OPTIONS, default=known, help=f"Pick from the list or type your own (max {MAX_TRAIT_LENGTH} characters each).")
        extra_traits = st.text_input("Extra traits (comma separated)", value=", ".join(trait for trait in traits_default if trait not in TRAIT_OPTIONS))

        tone_default = buddy.tone if buddy else TONE_OPTIONS[1]
        tone_choice = st.selectbox("Tone", options=[*TONE_OPTIONS, CUSTOM], index=(TONE_OPTIONS.index(tone_default) if tone_default in TONE_OPTIONS else len(TONE_OPTIONS)))
        tone_custom = st.text_input("Tone (custom)", value="" if tone_default in TONE_OPTIONS else tone_default)

        target_default = buddy.target if buddy else TARGET_OPTIONS[1]
        target_choice = st.selectbox("Target", options=[*TARGET_OPTIONS, CUSTOM], index=(TARGET_OPTIONS.index(target_default) if target_default in TARGET_OPTIONS else len(TARGET_OPTIONS)))
        target_custom = st.text_input("Target (custom)", value="" if target_default in TARGET_OPTIONS else target_default)

        st.markdown("<div class='sg-caption'>Course grounding</div>", unsafe_allow_html=True)
        course_label = st.selectbox(
            "Course material",
            options=labels,
            index=labels.index(current_course),
            help="Selecting a course lets the assistant retrieve from that material. 'None' means general answers with no retrieval.",
        )

        st.caption("Saving updates the reusable Buddy. Conversations that already exist keep the configuration they started with.")
        submitted = st.form_submit_button("Save Buddy", type="primary")

    if not submitted:
        return

    traits = [*preselected, *[part for part in extra_traits.split(",") if part.strip()]]
    tone = tone_custom if tone_choice == CUSTOM else tone_choice
    target = target_custom if target_choice == CUSTOM else target_choice
    try:
        if buddy is None:
            created = services.buddies.create_buddy(name=name, target=target, tone=tone, traits=traits, course_id=choices[course_label])
            st.success(f"Created “{created.name}”.", icon="✅")
        else:
            services.buddies.update_buddy(buddy.id, name=name, target=target, tone=tone, traits=traits, course_id=choices[course_label])
            st.success("Buddy updated. Existing conversations keep their original configuration.", icon="✅")
        st.rerun()
    except StudyGraphError as exc:
        st.error(str(exc), icon="🚫")


def render() -> None:
    services = get_services()
    inject_css()
    page_header("My Study Buddies ✦", "Create, manage and personalise your study companions. Task is chosen per message in the chat.")

    buddies = services.buddies.list_buddies()
    course_names = {course.id: course.name for course in services.buddies.list_courses()}

    if buddies:
        columns = st.columns(2)
        for index, buddy in enumerate(buddies):
            with columns[index % 2]:
                buddy_card(buddy, course_names.get(buddy.course_id or "", ""))
                with st.expander("Edit this Buddy"):
                    _buddy_form(services, buddy)

    st.divider()
    st.subheader("Create a new Buddy")
    _buddy_form(services, None)


if __name__ == "__main__":
    render()
