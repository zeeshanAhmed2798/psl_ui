import pandas as pd
import streamlit as st

from ..api import bowler_endpoint, fetch_api, list_bowlers
from ..components import render_endpoint_copy, render_metric_card, render_table
from ..config import PLACEHOLDER_IMAGE
from ..utils import fuzzy_search, local_image_for_name


def render_bowlers(container):
    with container:
        st.subheader("🎯 Bowlers Explorer")
        bowler_names = list_bowlers()
        selected = st.selectbox("Select bowler", bowler_names) if bowler_names else ""
        target_name = selected

        if target_name:
            render_bowler_stats(target_name, bowler_names)
        elif not bowler_names:
            st.info("Bowler list unavailable. Configure API and try again.")


def render_bowler_stats(name: str, available_names: list[str]):
    with st.spinner("Fetching bowler stats..."):
        stats = fetch_api(f"{bowler_endpoint(name)}/stats", use_cache=False)

    if not stats:
        suggestions = fuzzy_search(name, available_names)
        if suggestions:
            st.info(f"Did you mean: {', '.join(suggestions)}?")
        else:
            st.warning("No data available for this bowler.")
        return

    overall = stats.get("overall") or stats.get("all") or stats
    img_path = local_image_for_name(name, base_dir="downloads_psl_players") or PLACEHOLDER_IMAGE
    st.image(img_path, caption=name, width=120)
    st.subheader(f"Overall Bowling Stats: {name}")
    metrics = [
        ("Innings", overall.get("innings")),
        ("Wickets", overall.get("wicket")),
        ("Economy", overall.get("economy")),
        ("Average", overall.get("average")),
        ("Strike Rate", overall.get("strikeRate")),
        ("Best Figure", overall.get("best_figure")),
        ("3W+", overall.get("three_w")),
        ("Fours Conceded", overall.get("fours")),
        ("Sixes Conceded", overall.get("sixes")),
        ("Player of Match", overall.get("mom")),
    ]
    for chunk_start in range(0, len(metrics), 5):
        cols = st.columns(5)
        for col, (label, value) in zip(cols, metrics[chunk_start : chunk_start + 5]):
            with col:
                render_metric_card(label, value)

    vs_teams = stats.get("against") or stats.get("againstTeams")
    if vs_teams:
        st.markdown("#### Bowling vs Teams")
        render_table(vs_teams, index_label="team")

    render_endpoint_copy("Copy bowler stats endpoint:", f"{bowler_endpoint(name)}/stats")
