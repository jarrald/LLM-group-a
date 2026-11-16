"""StudyGraph Streamlit entry point.

Three pages (ADR-018): Chat, Buddies, About. Pages are thin: they read state, call a
service from ``app/services`` and render (``40-stack-and-architecture.md``).
"""

from __future__ import annotations

import streamlit as st

# 1. Konfigurer vinduet, før Streamlit tegner indhold på siden.
st.set_page_config(page_title="StudyGraph", page_icon="✦", layout="wide")

# 2. Registrer siderne; selve chatlogikken ligger i services og grafen.
pages = [
    # Standardsiden bruger "/" og skal derfor ikke have sin egen url_path.
    st.Page("ui/chat_page.py", title="Chat", icon="💬", default=True),
    st.Page("ui/buddies_page.py", title="Buddies", icon="🧠", url_path="buddies"),
    st.Page("ui/about_page.py", title="About", icon="ℹ️", url_path="about"),
]

# 3. Kør den valgte side. Streamlit gentager dette ved brugerinteraktioner.
navigation = st.navigation(pages, position="sidebar")
navigation.run()
