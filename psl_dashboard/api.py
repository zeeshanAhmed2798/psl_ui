from __future__ import annotations

from urllib.parse import quote

import requests
import streamlit as st

from .config import TEAM_FALLBACK, get_base_url


def _encode(name: str) -> str:
    return quote(name.strip(), safe="")


def encode_value(value: str) -> str:
    return _encode(value)


@st.cache_data(show_spinner=False)
def _cached_request(base_url: str, endpoint: str, method: str, params: dict | None, json_data: dict | None):
    return _make_request(base_url, endpoint, method, params, json_data)


def _make_request(base_url: str, endpoint: str, method: str, params: dict | None, json_data: dict | None):
    url = f"{base_url}{endpoint if endpoint.startswith('/') else '/' + endpoint}"
    response = requests.request(method, url, params=params, json=json_data, timeout=12)
    if response.status_code >= 400:
        raise requests.HTTPError(response.text or response.reason, response=response)
    try:
        return response.json()
    except ValueError:
        return response.text


def fetch_api(
    endpoint: str,
    method: str = "GET",
    params: dict | None = None,
    json_data: dict | None = None,
    use_cache: bool = True,
    suppress_warning: bool = False,
):
    """Fetch data from API with error handling."""
    base_url = get_base_url()
    if not base_url:
        if not suppress_warning:
            st.warning("Configure API_BASE_URL (or PSL_API_BASE env var) before fetching data.")
        return None

    method = method.upper()
    try:
        if method == "GET" and use_cache:
            return _cached_request(base_url, endpoint, method, params, json_data)
        return _make_request(base_url, endpoint, method, params, json_data)
    except requests.HTTPError as http_err:
        status = http_err.response.status_code if http_err.response else ""
        message = http_err.response.text if http_err.response else str(http_err)
        if status and int(status) >= 500:
            if not suppress_warning:
                st.error("API unavailable (server error). Please try again later.")
        elif status == 404:
            if not suppress_warning:
                st.warning("Requested item not found. Check the name or try suggestions.")
        else:
            if not suppress_warning:
                st.error(f"Request failed ({status}): {message}")
    except requests.RequestException as exc:
        if not suppress_warning:
            st.error(f"API request failed: {exc}")
    except Exception as exc:  # noqa: BLE001
        if not suppress_warning:
            st.error(f"Unexpected error: {exc}")
    return None


def list_players() -> list[str]:
    data = fetch_api("/players")
    return sorted(data) if isinstance(data, list) else []


def list_bowlers() -> list[str]:
    data = fetch_api("/bowlers")
    return sorted(data) if isinstance(data, list) else []


def list_teams() -> list[str]:
    # Backend does not expose /teams list; rely on fallback to avoid repeated 404s.
    return TEAM_FALLBACK


def player_endpoint(path: str) -> str:
    return f"/players/{_encode(path)}"


def bowler_endpoint(path: str) -> str:
    return f"/bowlers/{_encode(path)}"


def team_endpoint(path: str) -> str:
    return f"/teams/{_encode(path)}"
