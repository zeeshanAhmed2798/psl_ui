from difflib import get_close_matches


def normalize_name(name: str) -> str:
    """Normalize whitespace/case for better matching."""
    return " ".join(name.split()).strip()


def fuzzy_search(query: str, options: list[str], n: int = 5, cutoff: float = 0.6) -> list[str]:
    """Return closest matches for search queries."""
    if not query or not options:
        return []
    return get_close_matches(query, options, n=n, cutoff=cutoff)
