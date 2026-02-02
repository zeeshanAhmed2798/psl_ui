"""
PSL Analytics Hub - Main Dashboard Application
===============================================
Comprehensive Pakistan Super League statistics, analytics, and insights platform.

Features:
- Player statistics and comparisons
- Bowler analytics
- Team performance metrics
- Interactive visualizations
- Real-time API integration

Configure the FastAPI base URL by setting the `PSL_API_BASE` environment variable:
    $env:PSL_API_BASE="http://127.0.0.1:8000"
    streamlit run app.py
"""

import streamlit as st
from pathlib import Path

from psl_dashboard import tabs
from psl_dashboard.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_DESCRIPTION,
    API_BASE_URL,
    get_psl_logo,
    validate_images_directory,
)


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=PROJECT_NAME,
        page_icon="🏏",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/yourusername/PSL-Analytics-Hub',
            'Report a bug': 'https://github.com/yourusername/PSL-Analytics-Hub/issues',
            'About': f"{PROJECT_NAME} v{PROJECT_VERSION}\n\n{PROJECT_DESCRIPTION}"
        }
    )


def render_sidebar():
    """Render sidebar with branding and configuration."""
    # Display PSL logo if available
    logo_path = get_psl_logo()
    if logo_path:
        st.sidebar.image(logo_path, use_container_width=True)
    
    # Project title
    st.sidebar.title(f"⚡ {PROJECT_NAME}")
    st.sidebar.caption(f"v{PROJECT_VERSION}")
    
    # API Configuration
    st.sidebar.subheader("⚙️ Configuration")
    st.sidebar.text_input(
        "API Base URL",
        value=st.session_state.get("api_base_override", API_BASE_URL),
        key="api_base_override",
        help="Override API base URL (e.g., http://127.0.0.1:8000)",
    )
    
    # Information
    with st.sidebar.expander("ℹ️ About"):
        st.write(PROJECT_DESCRIPTION)
        
        # Validation info
        validation = validate_images_directory()
        st.write("**Assets Status:**")
        st.write(f"✅ Images directory: {'Found' if validation['images_dir_exists'] else '❌ Missing'}")
        st.write(f"✅ PSL logo: {'Found' if validation['psl_logo_exists'] else '❌ Missing'}")
        st.write(f"✅ Team logos: {validation['team_logos_found']}/{validation['total_teams']}")
    
    st.sidebar.info("💡 Responses are cached per endpoint to reduce API load.")
    
    # Footer
    st.sidebar.divider()
    st.sidebar.caption("Built with FastAPI, Streamlit & ❤️")


def main():
    """Main application entry point."""
    setup_page_config()
    
    # Render sidebar
    render_sidebar()
    
    # Main header
    st.title(f"🏏 {PROJECT_NAME}")
    st.markdown(f"*{PROJECT_DESCRIPTION}*")
    st.divider()
    
    # Create tabs
    tab_handles = st.tabs([
        "🏠 Home",
        "🏏 Players",
        "🎯 Bowlers",
        "🏆 Teams",
        "⚖️ Compare",
        "📊 Leaderboards",
        "📚 API Docs",
    ])
    
    # Render tab content
    tabs.render_home(tab_handles[0])
    tabs.render_players(tab_handles[1])
    tabs.render_bowlers(tab_handles[2])
    tabs.render_teams(tab_handles[3])
    tabs.render_compare(tab_handles[4])
    tabs.render_leaderboards(tab_handles[5])
    tabs.render_api_docs(tab_handles[6])

if __name__ == "__main__":
    main()