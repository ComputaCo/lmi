from __future__ import annotations

from enum import Enum
from typing import Literal
import attr
from abc import abstractmethod
from gptos.lmi.components.component import Component

from gptos.lmi.utils import normalize
from gptos.lmi.misc.alignment import Alignment
from gptos.lmi.handlers.display_event_handler import DisplayEventHandler
from gptos.lmi.handlers.drag_event_handler import DragEventHandler
from gptos.lmi.handlers.drop_event_handler import DropEventHandler
from gptos.lmi.handlers.focus_event_handler import FocusEventHandler
from gptos.lmi.handlers.keyboard_event_handler import KeyboardEventHandler
from gptos.lmi.handlers.mouse_event_handler import MouseEventHandler
from gptos.lmi.handlers.scroll_event_handler import ScrollEventHandler
from gptos.services.keyboard_service import KeyboardService


@attr.s(auto_attribs=True)
class AbstractComponent(Toolbox, DisplayEventHandler):
    preferred_size: int = None
    flex_factor: float = 1.0  # 0 = fixed, 1 = normal, inf = absorb all difference

    @property
    def max_size(self) -> int:
        return self.preferred_size

    @property
    def min_size(self) -> int:
        return self.preferred_size

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
