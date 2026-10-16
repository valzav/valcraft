"""Shared input validation helpers."""


def require_non_empty(value: str, field: str) -> str:
    """Return `value` unchanged, or raise ValueError naming `field`.

    A value made only of whitespace counts as empty; the returned value is never trimmed.
    """
    if value.strip() == "":
        raise ValueError(f"{field} must not be empty")
    return value
