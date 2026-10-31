"""StudyGraph Streamlit entry point.

Three pages (ADR-018): Chat, Buddies, About. Pages are thin: they read state, call a
service from ``app/services`` and render (``40-stack-and-architecture.md``).
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="StudyGraph", page_icon="✦", layout="wide")

pages = [
    # The default page is served at "/", so it must not declare a url_path of its own.
    st.Page("ui/chat_page.py", title="Chat", icon="💬", default=True),
    st.Page("ui/buddies_page.py", title="Buddies", icon="🧠", url_path="buddies"),
    st.Page("ui/about_page.py", title="About", icon="ℹ️", url_path="about"),
]

navigation = st.navigation(pages, position="sidebar")
navigation.run()
