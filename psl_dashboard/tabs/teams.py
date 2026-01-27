import pandas as pd
import streamlit as st

from ..api import encode_value, fetch_api, list_teams, team_endpoint
from ..components import render_endpoint_copy, render_metric_card, render_table
from ..config import PLACEHOLDER_IMAGE
from ..utils import local_image_for_name


def render_teams(container):
    with container:
        st.subheader("🏆 Teams Explorer")
        team_names = list_teams()
        selected_team = st.selectbox("Select team", team_names)
        if selected_team:
            render_team_stats(selected_team)

        st.markdown("#### Head-to-Head")
        col1, col2 = st.columns(2)
        with col1:
            team_a = st.selectbox("Team A", team_names, key="team_a")
        with col2:
            team_b = st.selectbox("Team B", team_names, key="team_b")
        if team_a and team_b and team_a != team_b:
            render_team_head_to_head(team_a, team_b)

        st.markdown("#### Team Highlights")
        cols = st.columns(2)
        with cols[0]:
            st.caption("Most runs scored (team totals)")
            with st.spinner("Highest totals..."):
                totals = fetch_api("/teams/top-totals")
            if totals:
                df_totals = pd.DataFrame(totals)
                if {"batting_team", "total_runs"}.issubset(df_totals.columns):
                    df_totals = df_totals.rename(columns={"batting_team": "Team", "total_runs": "Total Runs"})
                st.dataframe(df_totals, use_container_width=True)
        with cols[1]:
            st.caption("Most runs chased (successful chases)")
            with st.spinner("Best chases..."):
                chases = fetch_api("/teams/top-chases")
            if chases:
                df_chases = pd.DataFrame(chases)
                if {"batting_team", "target"}.issubset(df_chases.columns):
                    df_chases = df_chases.rename(columns={"batting_team": "Team", "target": "Target"})
                st.dataframe(df_chases, use_container_width=True)


def render_team_stats(team: str):
    with st.spinner("Fetching team stats..."):
        stats = fetch_api(f"{team_endpoint(team)}/stats", use_cache=False)

    if not stats:
        st.warning("No data available for this team.")
        return

    overall = stats.get("overall", stats)
    img = local_image_for_name(team, base_dir="images") or PLACEHOLDER_IMAGE
    st.image(img, caption=team, width=120)
    st.subheader(f"Team Stats: {team}")
    metrics = [
        ("Matches", overall.get("match_played")),
        ("Wins", overall.get("match_won")),
        ("No Result", overall.get("no_results")),
        ("Losses", overall.get("loss")),
        ("Titles", overall.get("titles_won")),
    ]
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics):
        with col:
            render_metric_card(label, value)

    vs_data = stats.get("against") or stats.get("againstTeams")
    if vs_data:
        st.markdown("#### Performance vs Opponents")
        render_table(vs_data)

    render_endpoint_copy("Copy team stats endpoint:", f"{team_endpoint(team)}/stats")


def render_team_head_to_head(team_a: str, team_b: str):
    if not team_a or not team_b:
        return
    with st.spinner("Fetching head-to-head..."):
        data = fetch_api(f"/teams/{encode_value(team_a)}/vs/{encode_value(team_b)}", use_cache=False)
    if data:
        st.markdown(f"#### Head-to-Head: {team_a} vs {team_b}")
        render_table([data])
