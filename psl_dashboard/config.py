import os
import re
from pathlib import Path

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

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"


def get_base_url() -> str | None:
    """Return sanitized base URL if configured, else None."""
    override = st.session_state.get("api_base_override") or API_BASE_URL
    if not override or "your-api-url" in override:
        return None
    return override.rstrip("/")


def team_logo_path(team: str) -> str | None:
    """Return a local logo path for a team if available."""
    if not team:
        return None
    slug = re.sub(r"[^a-z0-9]+", "_", team.casefold()).strip("_")
    candidate = IMAGES_DIR / f"{slug}.png"
    if candidate.exists():
        return str(candidate)
    return None
