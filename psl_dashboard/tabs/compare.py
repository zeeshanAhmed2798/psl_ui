import streamlit as st

from ..api import encode_value, fetch_api, list_bowlers, list_players, list_teams
from ..components import render_comparison_chart, render_endpoint_copy, render_metric_card
from ..config import PLACEHOLDER_IMAGE
from .bowlers import render_bowler_stats
from .players import render_player_stats


def render_compare(container):
    with container:
        st.subheader("⚖️ Compare")
        sub_tabs = st.tabs(["Players", "Bowlers", "Teams", "Batsman vs Bowler"])

        with sub_tabs[0]:
            player_names = list_players()
            if not player_names:
                st.warning("Player list unavailable.")
            else:
                p1 = st.selectbox("Player 1", player_names, key="cmp_p1")
                p2 = st.selectbox("Player 2", player_names, key="cmp_p2")
                if p1 and p2 and p1 != p2:
                    render_player_comparison(p1, p2)

        with sub_tabs[1]:
            bowler_names = list_bowlers()
            if not bowler_names:
                st.warning("Bowler list unavailable.")
            else:
                b1 = st.selectbox("Bowler 1", bowler_names, key="cmp_b1")
                b2 = st.selectbox("Bowler 2", bowler_names, key="cmp_b2")
                if b1 and b2 and b1 != b2:
                    render_bowler_comparison(b1, b2)

        with sub_tabs[2]:
            team_names = list_teams()
            t1 = st.selectbox("Team 1", team_names, key="cmp_t1")
            t2 = st.selectbox("Team 2", team_names, key="cmp_t2")
            if t1 and t2 and t1 != t2:
                render_team_comparison(t1, t2)

        with sub_tabs[3]:
            player_names = list_players()
            bowler_names = list_bowlers()
            batsman = st.selectbox("Batsman", player_names, key="bat_vs_bowl_bat")
            bowler = st.selectbox("Bowler", bowler_names, key="bat_vs_bowl_bowl")
            if batsman and bowler:
                render_batsman_bowler_h2h(batsman, bowler)


def render_player_comparison(p1: str, p2: str):
    with st.spinner("Comparing players..."):
        data = fetch_api("/players/compare", method="POST", json_data={"players": [p1, p2]}, use_cache=False)
    if not data:
        st.warning("No comparison data available.")
        return

    player_a = data.get("player_a") or data.get("player1") or (data.get("players", [None, None])[0] if isinstance(data.get("players"), list) else None)
    player_b = data.get("player_b") or data.get("player2") or (data.get("players", [None, None])[1] if isinstance(data.get("players"), list) else None)
    if not player_a or not player_b:
        st.warning("Unexpected comparison payload.")
        return

    cols = st.columns(2)
    with cols[0]:
        st.image(PLACEHOLDER_IMAGE, caption=p1, width=120)
        render_metric_card("Runs", player_a.get("runs"))
        render_metric_card("Average", player_a.get("avg"))
        render_metric_card("Strike Rate", player_a.get("strikeRate"))
        render_metric_card("Hundreds", player_a.get("hundreds"))
    with cols[1]:
        st.image(PLACEHOLDER_IMAGE, caption=p2, width=120)
        render_metric_card("Runs", player_b.get("runs"))
        render_metric_card("Average", player_b.get("avg"))
        render_metric_card("Strike Rate", player_b.get("strikeRate"))
        render_metric_card("Hundreds", player_b.get("hundreds"))

    labels = ["Runs", "Average", "Strike Rate", "Hundreds", "Sixes", "Fours"]
    values_a = [
        player_a.get("runs"),
        player_a.get("avg"),
        player_a.get("strikeRate"),
        player_a.get("hundreds"),
        player_a.get("sixes"),
        player_a.get("fours"),
    ]
    values_b = [
        player_b.get("runs"),
        player_b.get("avg"),
        player_b.get("strikeRate"),
        player_b.get("hundreds"),
        player_b.get("sixes"),
        player_b.get("fours"),
    ]
    render_comparison_chart("Batters Comparison", labels, values_a, values_b, p1, p2)
    render_endpoint_copy("Copy comparison endpoint:", "/players/compare")


def render_bowler_comparison(b1: str, b2: str):
    with st.spinner("Comparing bowlers..."):
        data = fetch_api("/bowlers/compare", method="POST", json_data={"bowlers": [b1, b2]}, use_cache=False)
    if not data:
        st.warning("No comparison data available.")
        return

    bowler_a = data.get("bowler_a") or data.get("bowler1") or (data.get("bowlers", [None, None])[0] if isinstance(data.get("bowlers"), list) else None)
    bowler_b = data.get("bowler_b") or data.get("bowler2") or (data.get("bowlers", [None, None])[1] if isinstance(data.get("bowlers"), list) else None)
    if not bowler_a or not bowler_b:
        st.warning("Unexpected comparison payload.")
        return

    cols = st.columns(2)
    with cols[0]:
        st.image(PLACEHOLDER_IMAGE, caption=b1, width=120)
        render_metric_card("Wickets", bowler_a.get("wicket"))
        render_metric_card("Economy", bowler_a.get("economy"))
        render_metric_card("Average", bowler_a.get("average"))
        render_metric_card("Strike Rate", bowler_a.get("strikeRate"))
    with cols[1]:
        st.image(PLACEHOLDER_IMAGE, caption=b2, width=120)
        render_metric_card("Wickets", bowler_b.get("wicket"))
        render_metric_card("Economy", bowler_b.get("economy"))
        render_metric_card("Average", bowler_b.get("average"))
        render_metric_card("Strike Rate", bowler_b.get("strikeRate"))

    labels = ["Wickets", "Economy", "Average", "Strike Rate", "Best Figure"]
    values_a = [
        bowler_a.get("wicket"),
        bowler_a.get("economy"),
        bowler_a.get("average"),
        bowler_a.get("strikeRate"),
        bowler_a.get("best_figure"),
    ]
    values_b = [
        bowler_b.get("wicket"),
        bowler_b.get("economy"),
        bowler_b.get("average"),
        bowler_b.get("strikeRate"),
        bowler_b.get("best_figure"),
    ]
    render_comparison_chart("Bowlers Comparison", labels, values_a, values_b, b1, b2)
    render_endpoint_copy("Copy comparison endpoint:", "/bowlers/compare")


def render_team_comparison(t1: str, t2: str):
    with st.spinner("Comparing teams..."):
        data = fetch_api("/teams/compare", method="POST", json_data={"teams": [t1, t2]}, use_cache=False)
    if not data:
        st.warning("No comparison data available.")
        return

    team_a = data.get("team_a") or data.get("team1") or (data.get("teams", [None, None])[0] if isinstance(data.get("teams"), list) else None)
    team_b = data.get("team_b") or data.get("team2") or (data.get("teams", [None, None])[1] if isinstance(data.get("teams"), list) else None)
    if not team_a or not team_b:
        st.warning("Unexpected comparison payload.")
        return

    cols = st.columns(2)
    for col, team_name, team_data in zip(cols, [t1, t2], [team_a, team_b]):
        with col:
            st.image(PLACEHOLDER_IMAGE, caption=team_name, width=120)
            render_metric_card("Matches", team_data.get("match_played"))
            render_metric_card("Wins", team_data.get("match_won"))
            render_metric_card("Losses", team_data.get("loss"))
            render_metric_card("Titles", team_data.get("titles_won"))

    labels = ["Matches", "Wins", "Losses", "No Results", "Titles"]
    values_a = [
        team_a.get("match_played"),
        team_a.get("match_won"),
        team_a.get("loss"),
        team_a.get("no_results"),
        team_a.get("titles_won"),
    ]
    values_b = [
        team_b.get("match_played"),
        team_b.get("match_won"),
        team_b.get("loss"),
        team_b.get("no_results"),
        team_b.get("titles_won"),
    ]
    render_comparison_chart("Teams Comparison", labels, values_a, values_b, t1, t2)
    render_endpoint_copy("Copy comparison endpoint:", "/teams/compare")


def _fmt(val):
    if isinstance(val, float):
        return round(val, 2)
    return val


def render_batsman_bowler_h2h(batsman: str, bowler: str):
    endpoint = f"/players/{encode_value(batsman)}/vs-bowler/{encode_value(bowler)}"
    st.markdown("##### Head-to-Head: Batter vs Bowler")
    with st.spinner("Fetching batter vs bowler..."):
        data = fetch_api(endpoint, use_cache=False)
    if not data:
        st.info("Head-to-head data unavailable.")
        return

    bat = data.get("batting_view", {})
    bowl = data.get("bowling_view", {})

    cols = st.columns(2)
    with cols[0]:
        st.caption(f"{batsman} batting vs {bowler}")
        render_metric_card("Runs", _fmt(bat.get("runs")))
        render_metric_card("Balls", _fmt(bat.get("balls")))
        render_metric_card("Strike Rate", _fmt(bat.get("strike_rate")))
        render_metric_card("Average", _fmt(bat.get("average")))
        render_metric_card("Fours", _fmt(bat.get("fours")))
        render_metric_card("Sixes", _fmt(bat.get("sixes")))
        render_metric_card("Dismissals", _fmt(bat.get("outs")))
    with cols[1]:
        st.caption(f"{bowler} bowling vs {batsman}")
        render_metric_card("Runs Conceded", _fmt(bowl.get("runs_conceded")))
        render_metric_card("Balls", _fmt(bowl.get("balls")))
        render_metric_card("Wickets", _fmt(bowl.get("wickets")))
        render_metric_card("Economy", _fmt(bowl.get("economy")))
        render_metric_card("Strike Rate", _fmt(bowl.get("strike_rate")))

    render_endpoint_copy("Copy batter vs bowler endpoint:", endpoint)
