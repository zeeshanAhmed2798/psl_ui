import pandas as pd
import streamlit as st

from ..api import fetch_api


def render_leaderboards(container):
    with container:
        st.subheader("📊 Leaderboards")
        cols = st.columns(2)
        with cols[0]:
            render_leaderboard(
                title="Top Run Scorers",
                endpoint="/players/top",
                columns=[("batter", "Batter"), ("batsman_runs", "Runs")],
                caption="Sorted by runs",
            )
            render_leaderboard(
                title="Most Sixes",
                endpoint="/players/top-sixes",
                columns=[("batter", "Batter"), ("sixes", "Sixes")],
                caption="Sorted by sixes",
            )
            render_leaderboard(
                title="Most Fours",
                endpoint="/players/top-fours",
                columns=[("batter", "Batter"), ("fours", "Fours")],
                caption="Sorted by fours",
            )
        with cols[1]:
            render_leaderboard(
                title="Top Wicket Takers",
                endpoint="/bowlers/top",
                columns=[("bowler", "Bowler"), ("bowler_wickets", "Wickets")],
                caption="Sorted by wickets",
            )
            render_leaderboard(
                title="Most Catches",
                endpoint="/players/top-catches",
                columns=[("fielder", "Fielder"), ("catches", "Catches")],
                caption="Sorted by catches",
            )
            render_leaderboard(
                title="Most Player of Match",
                endpoint="/players/top-mom",
                columns=[("player_of_match", "Player"), ("awards", "Awards")],
                caption="Sorted by awards",
            )


def render_leaderboard(title: str, endpoint: str, columns: list[tuple[str, str]], caption: str):
    with st.spinner(f"Loading {title.lower()}..."):
        data = fetch_api(endpoint)
    st.markdown(f"#### {title}")
    if not data:
        st.info("No data available.")
        return
    df = pd.DataFrame(data)
    missing = [key for key, _ in columns if key not in df.columns]
    if missing:
        st.info("Unexpected leaderboard format.")
        return
    display_cols = {key: label for key, label in columns}
    st.dataframe(df[list(display_cols.keys())].rename(columns=display_cols), use_container_width=True)
    st.caption(caption)
