"""Per-workspace API request counting."""

_COUNTERS: dict[str, dict[str, int]] = {}

WINDOW_SECONDS = 60


def record_request(workspace_id: str, now: int) -> int:
    """Increment and return this workspace's request count for the current window."""
    window_start = now - (now % WINDOW_SECONDS)
    counter = _COUNTERS.get(workspace_id)
    if counter is None or counter["window_start"] != window_start:
        counter = {"window_start": window_start, "count": 0}
        _COUNTERS[workspace_id] = counter
    counter["count"] += 1
    return counter["count"]
