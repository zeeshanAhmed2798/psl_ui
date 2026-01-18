import streamlit as st

from ..api import fetch_api
from ..components import render_metric_card
from ..config import get_base_url


def render_home(container):
    with container:
        st.header("🏠 PSL Stats Dashboard")
        st.write("Explore PSL player, bowler, and team performance via the FastAPI backend.")
        base_url = get_base_url()
        if not base_url:
            st.warning("Set a valid API base URL in the sidebar to start.")
            return

        cols = st.columns(3)
        with cols[0]:
            with st.spinner("Checking health..."):
                health = fetch_api("/health", use_cache=False)
            if health:
                render_metric_card("API Health", health.get("status", "OK"))
        with cols[1]:
            with st.spinner("Fetching top run scorers..."):
                top_runs = fetch_api("/players/top?limit=1")
            if top_runs:
                best = top_runs[0]
                render_metric_card("Top Runs", best.get("batsman_runs"))
                st.caption(best.get("batter", ""))
        with cols[2]:
            with st.spinner("Fetching top wicket takers..."):
                top_wickets = fetch_api("/bowlers/top?limit=1")
            if top_wickets:
                best = top_wickets[0]
                render_metric_card("Top Wickets", best.get("bowler_wickets"))
                st.caption(best.get("bowler", ""))

        st.markdown("#### How to use")
        st.write(
            "Navigate tabs to explore players, bowlers, teams, run comparisons, and copy API endpoints. "
            "Use the sidebar to cache data and adjust the API base URL."
        )
