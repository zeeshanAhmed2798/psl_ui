import os

import streamlit as st

API_BASE_URL = os.getenv("PSL_API_BASE", "http://127.0.0.1:8000")
PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=PSL"
TEAM_FALLBACK = [
    "Islamabad United",
    "Karachi Kings",
    "Lahore Qalandars",
    "Multan Sultans",
    "Peshawar Zalmi",
    "Quetta Gladiators",
]


def get_base_url() -> str | None:
    """Return sanitized base URL if configured, else None."""
    override = st.session_state.get("api_base_override") or API_BASE_URL
    if not override or "your-api-url" in override:
        return None
    return override.rstrip("/")
