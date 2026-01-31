"""
PSL Analytics Hub - UI Components (Backward Compatible)
========================================================
This module provides backward compatibility by exporting functions
under both old and new names.
"""

import pandas as pd
import streamlit as st

from .config import get_base_url, get_team_logo, get_team_color


def render_metric_card(label: str, value, help_text: str | None = None):
    """Render a metric card with proper formatting."""
    display_value = "N/A" if value in (None, "", []) else value
    st.metric(label, display_value, help=help_text)


def render_team_header(team_name: str, subtitle: str | None = None):
    """Render a team header with logo and name."""
    col1, col2 = st.columns([1, 4])
    
    with col1:
        logo_path = get_team_logo(team_name)
        if logo_path:
            st.image(logo_path, width=100)
        else:
            st.write("🏏")
    
    with col2:
        st.subheader(team_name)
        if subtitle:
            st.caption(subtitle)


def render_team_card(team_name: str, stats: dict | None = None):
    """Render a team card with logo and basic stats."""
    logo_path = get_team_logo(team_name)
    
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if logo_path:
                st.image(logo_path, use_container_width=True)
            else:
                st.markdown("### 🏏")
        
        with col2:
            st.markdown(f"**{team_name}**")
            if stats:
                for key, value in stats.items():
                    st.caption(f"{key}: {value}")


def render_endpoint_copy(label: str, endpoint: str):
    """Render a copyable API endpoint URL."""
    base_url = get_base_url()
    if not base_url:
        st.warning("API base URL not configured")
        return
    
    full_url = f"{base_url}{endpoint if endpoint.startswith('/') else '/' + endpoint}"
    st.write(label)
    st.code(full_url, language="text")


def render_comparison_chart(
    title: str,
    labels: list[str],
    values_a: list,
    values_b: list,
    name_a: str,
    name_b: str,
    color_a: str | None = None,
    color_b: str | None = None,
):
    """Render a grouped bar chart for comparing two entities."""
    import plotly.graph_objects as go
    
    # Use team colors if available
    marker_a = {"color": color_a} if color_a else {}
    marker_b = {"color": color_b} if color_b else {}
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name=name_a, x=labels, y=values_a, marker=marker_a))
    fig.add_trace(go.Bar(name=name_b, x=labels, y=values_b, marker=marker_b))
    
    fig.update_layout(
        barmode="group",
        height=400,
        title=title,
        template="plotly_white",
        showlegend=True,
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_table(data, index_label: str = "item", use_team_colors: bool = False):
    """Display a dataframe safely by coercing mixed types to strings if needed."""
    normalized = data
    
    if isinstance(data, dict):
        # dict of dicts
        if all(isinstance(v, dict) for v in data.values()):
            normalized = [{index_label: k, **v} for k, v in data.items()]
        else:  # dict of scalars
            normalized = [{index_label: k, "value": v} for k, v in data.items()]
    
    df = pd.DataFrame(normalized)
    
    try:
        # Apply styling if team colors requested
        if use_team_colors and "team" in df.columns:
            def highlight_team(row):
                team_name = row.get("team", "")
                color = get_team_color(team_name)
                return [f"background-color: {color}22" for _ in row]  # 22 = 13% opacity
            
            styled_df = df.style.apply(highlight_team, axis=1)
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
    except Exception:
        # Fallback to string conversion
        st.dataframe(df.astype(str), use_container_width=True)


def render_stat_comparison(stat_name: str, value_a, value_b, name_a: str, name_b: str):
    """Render a side-by-side stat comparison."""
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        st.metric(f"{name_a} - {stat_name}", value_a)
    
    with col2:
        # Show difference if numeric
        try:
            diff = float(value_a) - float(value_b)
            st.metric("Difference", f"{diff:+.2f}")
        except (ValueError, TypeError):
            st.metric("Comparison", "—")
    
    with col3:
        st.metric(f"{name_b} - {stat_name}", value_b)


def render_player_image(player_name: str, width: int = 150):
    """Render player image if available."""
    try:
        from .utils import local_image_for_name
    except ImportError:
        # Fallback if local_image_for_name is in helpers
        try:
            from .helpers import local_image_for_name
        except ImportError:
            # If neither works, just show name
            st.markdown(f"👤 **{player_name}**")
            return
    
    image_path = local_image_for_name(player_name)
    if image_path:
        st.image(image_path, width=width, caption=player_name)
    else:
        st.markdown(f"👤 **{player_name}**")