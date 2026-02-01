"""
PSL Analytics Hub - Configuration
==================================
Central configuration for the PSL Analytics Hub platform.
"""
import os
import re
from pathlib import Path

import streamlit as st

# API Configuration
API_BASE_URL = os.getenv("PSL_API_BASE", "https://psl-stats-api.vercel.app")

# Project branding
PROJECT_NAME = "PSL Analytics Hub"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = "Comprehensive Pakistan Super League statistics, analytics, and insights platform"

# Image paths
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"

# Default placeholder
PLACEHOLDER_IMAGE = str(IMAGES_DIR / "psl_logo.png") if (IMAGES_DIR / "psl_logo.png").exists() else "https://via.placeholder.com/150?text=PSL"

# Team names (exact names as they appear in your data)
TEAM_NAMES = [
    "Islamabad United",
    "Karachi Kings",
    "Lahore Qalandars",
    "Multan Sultans",
    "Peshawar Zalmi",
    "Quetta Gladiators",
]

# Backward compatibility: TEAM_FALLBACK is the same as TEAM_NAMES
TEAM_FALLBACK = TEAM_NAMES

# Team logo mapping (slug -> friendly name)
TEAM_LOGO_MAP = {
    "islamabad_united": "Islamabad United",
    "karachi_kings": "Karachi Kings",
    "lahore_qalandars": "Lahore Qalandars",
    "multan_sultans": "Multan Sultans",
    "peshawar_zalmi": "Peshawar Zalmi",
    "quetta_gladiators": "Quetta Gladiators",
}

# Team colors for visualizations
TEAM_COLORS = {
    "Islamabad United": "#DC1F26",
    "Karachi Kings": "#1C4587",
    "Lahore Qalandars": "#4CAF50",
    "Multan Sultans": "#FFD700",
    "Peshawar Zalmi": "#FFEB3B",
    "Quetta Gladiators": "#9C27B0",
}


def get_base_url() -> str | None:
    """Return sanitized base URL if configured, else None."""
    override = st.session_state.get("api_base_override") or API_BASE_URL
    if not override or "your-api-url" in override:
        return None
    return override.rstrip("/")


def get_psl_logo() -> str | None:
    """Return path to PSL logo if it exists."""
    logo_path = IMAGES_DIR / "psl_logo.png"
    if logo_path.exists():
        return str(logo_path)
    
    # Try alternative names
    for name in ["psl.png", "logo.png", "psl_logo.jpg"]:
        alt_path = IMAGES_DIR / name
        if alt_path.exists():
            return str(alt_path)
    
    return None


def get_team_logo(team_name: str) -> str | None:
    """
    Return path to team logo if it exists.
    
    Args:
        team_name: Team name (e.g., "Islamabad United", "Karachi Kings")
    
    Returns:
        Path to team logo image or None if not found
    """
    if not team_name:
        return None
    
    # Normalize team name to slug
    slug = re.sub(r"[^a-z0-9]+", "_", team_name.lower()).strip("_")
    
    # Try different variations
    possible_names = [
        f"{slug}.png",
        f"{slug}.jpg",
        f"{slug}_logo.png",
        f"{team_name.replace(' ', '_')}.png",
        f"{team_name.replace(' ', '_').lower()}.png",
    ]
    
    for name in possible_names:
        logo_path = IMAGES_DIR / name
        if logo_path.exists():
            return str(logo_path)
    
    return None


def get_all_team_logos() -> dict[str, str]:
    """
    Get all available team logos.
    
    Returns:
        Dictionary mapping team names to their logo paths
    """
    logos = {}
    for team in TEAM_NAMES:
        logo_path = get_team_logo(team)
        if logo_path:
            logos[team] = logo_path
    return logos


def get_team_color(team_name: str) -> str:
    """
    Get team's official color for visualizations.
    
    Args:
        team_name: Team name
    
    Returns:
        Hex color code
    """
    return TEAM_COLORS.get(team_name, "#808080")  # Default to gray


def validate_images_directory() -> dict[str, bool]:
    """
    Validate that images directory exists and check for logo files.
    
    Returns:
        Dictionary with validation status
    """
    return {
        "images_dir_exists": IMAGES_DIR.exists(),
        "psl_logo_exists": get_psl_logo() is not None,
        "team_logos_found": len(get_all_team_logos()),
        "total_teams": len(TEAM_NAMES),
    }


# Backward compatibility function (old name)
def team_logo_path(team: str) -> str | None:
    """Legacy function name for backward compatibility."""
    return get_team_logo(team)