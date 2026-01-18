import streamlit as st

from ..config import get_base_url


def render_api_docs(container):
    with container:
        base_url = get_base_url() or "http://your-api-url.com"
        st.subheader("📚 API Docs")

        st.markdown("### Base & Health")
        st.code(f"{base_url}/", language="text")
        st.code(f"{base_url}/health", language="text")

        st.markdown("### Players")
        st.code(f"{base_url}/players", language="text")
        st.code(f"{base_url}/players/{{name}}/stats", language="text")
        st.code(f"{base_url}/players/{{name}}/growth", language="text")
        st.code(f"{base_url}/players/{{name}}/vs-team/{{team}}", language="text")
        st.code(f"{base_url}/players/{{batter}}/vs-bowler/{{bowler}}", language="text")
        st.code(f"{base_url}/players/compare", language="text")
        st.code(f"{base_url}/players/top?limit=10", language="text")
        st.code(f"{base_url}/players/top-sixes?limit=10", language="text")
        st.code(f"{base_url}/players/top-fours?limit=10", language="text")
        st.code(f"{base_url}/players/top-catches?limit=10", language="text")
        st.code(f"{base_url}/players/top-mom?limit=10", language="text")

        st.markdown("### Bowlers")
        st.code(f"{base_url}/bowlers", language="text")
        st.code(f"{base_url}/bowlers/{{name}}/stats", language="text")
        st.code(f"{base_url}/bowlers/compare", language="text")
        st.code(f"{base_url}/bowlers/top?limit=10", language="text")

        st.markdown("### Teams")
        st.code(f"{base_url}/teams/{{name}}/stats", language="text")
        st.code(f"{base_url}/teams/{{team1}}/vs/{{team2}}", language="text")
        st.code(f"{base_url}/teams/compare", language="text")
        st.code(f"{base_url}/teams/{{name}}/all", language="text")
        st.code(f"{base_url}/teams/top-totals", language="text")
        st.code(f"{base_url}/teams/top-chases", language="text")
