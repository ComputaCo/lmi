from __future__ import annotations

from enum import Enum
from typing import Literal
import attr
from abc import abstractmethod


@attr.s(auto_attribs=True, kw_only=True)
class AbstractComponent(ABC, DisplayEventHandler):
    min_size: int = None
    max_size: int = None
    preferred_size: int = None
    flex_factor: float = 1.0  # 0 = fixed, 1 = normal, inf = absorb all difference

    @abstractmethod
    def render(self, size) -> str:
        pass

    @property
    @abstractmethod
    def tools(self) -> list[Tool]:
        pass

    @property
    @abstractmethod
    def visible_components(self) -> list[Component]:
        pass
