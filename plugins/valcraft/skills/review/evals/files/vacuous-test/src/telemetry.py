"""Usage-metric emitter."""

_EVENTS: list[tuple[str, dict]] = []


def emit(name: str, payload: dict) -> None:
    """Record one usage metric event."""
    _EVENTS.append((name, payload))
