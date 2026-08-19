"""Retention-window parsing."""


def parse_window(value: str) -> int:
    """Convert a strict positive hour or day window to seconds."""
    if len(value) < 2 or not value[:-1].isdigit() or value != value.strip():
        raise ValueError(f"invalid retention window: {value!r}")
    count = int(value[:-1])
    factors = {"h": 60 * 60, "d": 24 * 60 * 60}
    if count <= 0 or value[-1] not in factors:
        raise ValueError(f"invalid retention window: {value!r}")
    return count * factors[value[-1]]
