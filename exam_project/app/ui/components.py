"""Presentation helpers shared by the pages.

The look deliberately follows the draw.io mocks (dark cards, rounded corners, a purple
accent, a "buddy preview" configuration card), while the behaviour follows the docs.
"""

from __future__ import annotations

import html

import streamlit as st

from app.domain.buddy import Buddy, BuddySnapshot
from app.domain.conversation import RetrievalStatus, SourceReference

_CSS = """
<style>
.sg-card {border:1px solid #2b3150; border-radius:16px; padding:16px 18px; background:#151b2e; margin-bottom:14px;}
.sg-card h4 {margin:0 0 2px 0; font-size:1.05rem;}
.sg-muted {color:#9aa0bd; font-size:0.86rem; line-height:1.45;}
.sg-pill {display:inline-block; padding:3px 11px; border-radius:999px; font-size:0.78rem; font-weight:600;}
.sg-grounded {background:#17352a; color:#6ee7b7; border:1px solid #2f6b4f;}
.sg-general {background:#262b42; color:#c7cbe3; border:1px solid #3c4260;}
.sg-config {background:#1a2038; border-radius:12px; padding:12px 14px; font-size:0.85rem; color:#cdd2ea; line-height:1.6;}
.sg-config b {color:#a9b0d6;}
.sg-caption {color:#8b91b4; font-size:0.8rem; text-transform:uppercase; letter-spacing:.08em;}
</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str) -> None:
    st.markdown(f"## {title}")
    st.markdown(f"<div class='sg-muted'>{html.escape(subtitle)}</div>", unsafe_allow_html=True)


def mode_pill(is_grounded: bool) -> str:
    if is_grounded:
        return "<span class='sg-pill sg-grounded'>📚 Course-grounded</span>"
    return "<span class='sg-pill sg-general'>🧠 General</span>"


def course_label(snapshot: BuddySnapshot, course_name: str) -> str:
    return course_name if snapshot.course_id else "None"


def config_html(snapshot: BuddySnapshot, course_name: str) -> str:
    traits = ", ".join(snapshot.traits) or "—"
    return (
        "<div class='sg-config'>"
        f"<b>Traits</b> {html.escape(traits)}<br>"
        f"<b>Tone</b> {html.escape(snapshot.tone)}<br>"
        f"<b>Target</b> {html.escape(snapshot.target)}<br>"
        f"<b>Course material</b> {html.escape(course_label(snapshot, course_name))}"
        "</div>"
    )


def buddy_card(buddy: Buddy, course_name: str) -> None:
    """One buddy summary card, as in the mocks."""
    grounded = buddy.is_course_grounded
    st.markdown(
        "<div class='sg-card'>"
        f"<h4>🧠 {html.escape(buddy.name)}</h4>"
        f"<div class='sg-muted'>{html.escape(buddy.tone)}</div>"
        f"<div style='margin:10px 0 4px 0'>{mode_pill(grounded)}</div>"
        f"<div class='sg-muted'>Traits: {html.escape(', '.join(buddy.traits))}</div>"
        f"<div class='sg-muted'>Target: {html.escape(buddy.target)}</div>"
        f"<div class='sg-muted'>Course material: {html.escape(course_name if grounded else 'None')}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def retrieval_notice(status: RetrievalStatus, error: str | None = None) -> None:
    """Tell the student exactly what retrieval did — never imply grounding when there is none."""
    if status is RetrievalStatus.EMPTY:
        st.warning("The course material does not cover this question — the answer below is not grounded in it.", icon="📄")
    elif status is RetrievalStatus.FAILED:
        st.error(f"Retrieval failed, so this answer is not grounded in the course material. {error or ''}".strip(), icon="⚠️")
    elif status is RetrievalStatus.SKIPPED:
        st.caption("General answer — this Buddy is not linked to course material.")


def sources_block(sources: tuple[SourceReference, ...], status: RetrievalStatus) -> None:
    """Show retrieved passages, only when retrieval actually delivered some."""
    if not sources:
        return
    label = f"Sources ({len(sources)})" if status.is_grounded else "Retrieved material (not used)"
    with st.expander(label):
        for index, source in enumerate(sources, start=1):
            distance = f"{source.distance:.3f}" if source.distance is not None else "—"
            st.markdown(f"**{index}. {source.label()}**  \n<span class='sg-muted'>chunk `{source.chunk_id}` · distance {distance}</span>", unsafe_allow_html=True)
            if source.snippet:
                st.caption(source.snippet)
