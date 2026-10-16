"""Shared input validation helpers."""


def require_non_empty(value: str, field: str) -> str:
    """Return `value` unchanged, or raise ValueError naming `field`.

    The returned value is never trimmed.
    """
    if value == "":
        raise ValueError(f"{field} must not be empty")
    return value
