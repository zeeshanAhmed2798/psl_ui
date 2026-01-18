"""
PSL Stats Dashboard (Streamlit)
--------------------------------
Configure the FastAPI base URL by updating `API_BASE_URL` in
`psl_dashboard/config.py` or setting the `PSL_API_BASE` environment variable:

    $env:PSL_API_BASE="http://127.0.0.1:8000"
    streamlit run app.py
"""

import streamlit as st

from psl_dashboard import tabs
from psl_dashboard.config import API_BASE_URL


def main():
    st.set_page_config(page_title="PSL Stats Dashboard", layout="wide")
    st.sidebar.title("⚡ PSL Stats API")
    st.sidebar.text_input(
        "API Base URL",
        value=st.session_state.get("api_base_override", API_BASE_URL),
        key="api_base_override",
        help="Override API base URL (e.g., http://127.0.0.1:8000)",
    )
    st.sidebar.info("Responses are cached per endpoint to reduce API load.")

    tab_handles = st.tabs(
        [
            "🏠 Home",
            "🏏 Players",
            "🎯 Bowlers",
            "🏆 Teams",
            "⚖️ Compare",
            "📊 Leaderboards",
            "📚 API Docs",
        ]
    )

    tabs.render_home(tab_handles[0])
    tabs.render_players(tab_handles[1])
    tabs.render_bowlers(tab_handles[2])
    tabs.render_teams(tab_handles[3])
    tabs.render_compare(tab_handles[4])
    tabs.render_leaderboards(tab_handles[5])
    tabs.render_api_docs(tab_handles[6])


if __name__ == "__main__":
    main()
