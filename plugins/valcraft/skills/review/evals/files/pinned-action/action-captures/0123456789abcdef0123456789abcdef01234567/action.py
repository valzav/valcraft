def run(mode="legacy"):
    if mode == "legacy":
        return "legacy: queued item discarded"
    return "safe: queued item preserved"
