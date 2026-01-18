import pandas as pd
import streamlit as st

from .config import get_base_url


def render_metric_card(label: str, value, help_text: str | None = None):
    display_value = "N/A" if value in (None, "", []) else value
    st.metric(label, display_value, help=help_text)


def render_endpoint_copy(label: str, endpoint: str):
    base_url = get_base_url()
    if not base_url:
        return
    full_url = f"{base_url}{endpoint if endpoint.startswith('/') else '/' + endpoint}"
    st.write(label)
    st.code(full_url, language="text")


def render_comparison_chart(title: str, labels: list[str], values_a: list, values_b: list, name_a: str, name_b: str):
    import plotly.graph_objects as go  # local import to keep module light

    fig = go.Figure()
    fig.add_trace(go.Bar(name=name_a, x=labels, y=values_a))
    fig.add_trace(go.Bar(name=name_b, x=labels, y=values_b))
    fig.update_layout(barmode="group", height=360, title=title)
    st.plotly_chart(fig, use_container_width=True)


def render_table(data, index_label: str = "item"):
    """
    Display a dataframe safely by coercing mixed types to strings if needed.
    Supports:
    - list of dicts
    - dict of dicts (key becomes index_label column)
    - dict of scalars (key/value pairs)
    """
    normalized = data
    if isinstance(data, dict):
        # dict of dicts
        if all(isinstance(v, dict) for v in data.values()):
            normalized = [{index_label: k, **v} for k, v in data.items()]
        else:  # dict of scalars
            normalized = [{index_label: k, "value": v} for k, v in data.items()]
    df = pd.DataFrame(normalized)
    try:
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.dataframe(df.astype(str), use_container_width=True)
