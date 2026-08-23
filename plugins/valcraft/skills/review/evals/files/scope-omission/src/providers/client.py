import httpx

from src.config.model_ref import ModelRef


class ProviderClient:
    def __init__(self, ref: ModelRef) -> None:
        self.ref = ref
        self.session = httpx.Client(base_url=ref.base_url)
