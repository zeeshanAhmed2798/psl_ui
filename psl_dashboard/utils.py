from difflib import get_close_matches


def normalize_name(name: str) -> str:
    """Normalize whitespace/case for better matching."""
    return " ".join(name.split()).strip()


def fuzzy_search(query: str, options: list[str], n: int = 5, cutoff: float = 0.6) -> list[str]:
    """Return closest matches for search queries."""
    if not query or not options:
        return []
    return get_close_matches(query, options, n=n, cutoff=cutoff)


def local_image_for_name(name: str, base_dir: str = "downloads_psl_players") -> str | None:
    """
    Return a filesystem path to a local image for the given name if it exists.
    Tries multiple slugs and extensions; also searches an optional secondary directory (images).
    """
    from pathlib import Path
    import re

    if not name:
        return None

    root = Path(__file__).resolve().parent.parent
    search_dirs = [root / base_dir, root / "images"]
    candidates = []

    stripped = " ".join(name.split()).strip()
    if stripped:
        lower = stripped.lower()
        title = stripped.title()
        # Basic slug with underscores and alnum-only
        simple_slug = re.sub(r"[^a-z0-9]+", "_", lower).strip("_")
        title_slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
        raw_slug = stripped.replace(" ", "_")
        for slug in {simple_slug, title_slug, raw_slug, lower.replace(" ", "_"), title.replace(" ", "_")}:
            for ext in ("jpg", "png", "jpeg", "webp"):
                candidates.append(f"{slug}.{ext}")

    for img_dir in search_dirs:
        if not img_dir.exists():
            continue
        for cand in candidates:
            path = img_dir / cand
            if path.exists():
                return path.as_posix()
    return None
