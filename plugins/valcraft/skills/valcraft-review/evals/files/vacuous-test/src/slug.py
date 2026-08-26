"""Document slug generation."""

from telemetry import emit


def slugify(title: str) -> str:
    """Return a lowercase hyphenated slug for a document title."""
    normalized = " ".join(title.split())
    if not normalized:
        raise ValueError("title must not be empty")
    emit("slug.generated", {"length": len(normalized)})
    return normalized.lower().replace(" ", "-")
