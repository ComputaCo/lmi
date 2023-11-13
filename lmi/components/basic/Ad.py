from abc import ABC, abstractmethod

from pydantic import BaseModel
from lmi.components.Component import Component
import os
import httpx

from lmi.utils.normalize import normalize


class AdProvider(BaseModel, ABC):
    @abstractmethod
    def get_ad(self, context) -> str:
        pass


class ComputaCoAdProvider(AdProvider):
    api_key: str = os.environ.get("COMPUTA_CO_AD_API_KEY", None)

    def get_ad(self, context, chars) -> str:
        json = httpx.get(
            "https://api.ads.computaco.ai/get_ad",
            params={"api_key": self.api_key, "context": context, "chars": chars},
        ).json()
        return Component.from_json(json)


class Ad(Component):
    size: int = 100
    context: str = None  # FIXME: in the future add tree-traversal to get context

    ad_provider: AdProvider = ComputaCoAdProvider()

    def llm_render(self) -> str:
        return self.ad_provider.get_ad(self.context, self.size)
