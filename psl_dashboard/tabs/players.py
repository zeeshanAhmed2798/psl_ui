import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ..api import fetch_api, list_players, player_endpoint
from ..components import render_endpoint_copy, render_metric_card, render_table
from ..config import PLACEHOLDER_IMAGE
from ..utils import fuzzy_search, normalize_name


def render_players(container):
    with container:
        st.subheader("🏏 Players Explorer")
        player_names = list_players()
        query = st.text_input("Search player name")
        selected = st.selectbox("Select from list", player_names) if player_names else ""
        suggestions = fuzzy_search(query, player_names) if query else []
        suggestion_choice = None
        if suggestions:
            st.info(f"Did you mean: {', '.join(suggestions)}?")
            suggestion_choice = st.selectbox("Suggested names", suggestions, key="player_suggestion")

        target_name = suggestion_choice or normalize_name(query) or selected

        if target_name:
            render_player_stats(target_name, player_names)
        elif not player_names:
            st.info("Player list unavailable. Configure API and try again.")


def render_player_stats(name: str, available_names: list[str]):
    with st.spinner("Fetching player stats..."):
        stats = fetch_api(f"{player_endpoint(name)}/stats", use_cache=False)

    if not stats:
        suggestions = fuzzy_search(name, available_names)
        if suggestions:
            st.info(f"Did you mean: {', '.join(suggestions)}?")
        else:
            st.warning("No data available for this player.")
        return

    overall = stats.get("overall") or stats.get("all") or stats
    st.image(PLACEHOLDER_IMAGE, caption=name, width=120)
    st.subheader(f"Overall Stats: {name}")
    metrics = [
        ("Runs", overall.get("runs")),
        ("Innings", overall.get("innings")),
        ("Average", overall.get("avg")),
        ("Strike Rate", overall.get("strikeRate")),
        ("Hundreds", overall.get("hundreds")),
        ("Highest Score", overall.get("highestScore")),
        ("Fours", overall.get("fours")),
        ("Sixes", overall.get("sixes")),
        ("Not Out", overall.get("notOut")),
        ("Player of Match", overall.get("mom")),
    ]
    for chunk_start in range(0, len(metrics), 5):
        cols = st.columns(5)
        for col, (label, value) in zip(cols, metrics[chunk_start : chunk_start + 5]):
            with col:
                render_metric_card(label, value)

    vs_teams = stats.get("against") or stats.get("againstTeams")
    if vs_teams:
        st.markdown("#### Performance vs Teams")
        render_table(vs_teams, index_label="team")

    with st.spinner("Fetching growth data..."):
        growth = fetch_api(f"{player_endpoint(name)}/growth")
    if growth:
        st.markdown("#### Season Growth")
        df_growth = pd.DataFrame(growth)
        x_field = "season" if "season" in df_growth.columns else "year" if "year" in df_growth.columns else None
        y_field = "runs" if "runs" in df_growth.columns else None
        if x_field and y_field:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_growth[x_field], y=df_growth[y_field], mode="lines+markers", name="Runs"))
            fig.update_layout(height=320, xaxis_title="Season", yaxis_title="Runs")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Growth data structure is unavailable for charting.")

    render_endpoint_copy("Copy player stats endpoint:", f"{player_endpoint(name)}/stats")
