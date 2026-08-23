import os
import tomllib

from src.config.model_ref import ModelRef


def load_model_reference(path: str) -> ModelRef:
    with open(path, "rb") as f:
        raw = tomllib.load(f)["model"]
    ref = ModelRef(raw["provider"], raw["model"], raw["base_url"], raw["api_key_env"])
    if ref.api_key_env not in os.environ:
        raise RuntimeError(f"{ref.api_key_env} is not set")
    return ref
