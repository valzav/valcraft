"""Document slug generation."""


def slugify(title: str) -> str:
    """Return a lowercase hyphenated slug for a document title."""
    normalized = " ".join(title.split())
    if not normalized:
        raise ValueError("title must not be empty")
    return normalized.lower().replace(" ", "-")
