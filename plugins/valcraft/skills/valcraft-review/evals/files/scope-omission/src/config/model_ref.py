from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRef:
    provider: str
    model: str
    base_url: str
    api_key_env: str
