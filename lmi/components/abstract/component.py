from __future__ import annotations
from abc import abstractmethod
from math import inf
import re
from typing import Type

import attr
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.abstract.viewable import LLMCanViewMixin

from lmi.utils import normalize
from lmi.misc.alignment import Alignment
from lmi.handlers.display_event_handler import DisplayEventHandler
from lmi.handlers.drag_event_handler import DragEventHandler
from lmi.handlers.drop_event_handler import DropEventHandler
from lmi.handlers.focus_event_handler import FocusEventHandler
from lmi.handlers.keyboard_event_handler import KeyboardEventHandler
from lmi.handlers.mouse_event_handler import MouseEventHandler
from lmi.handlers.scroll_event_handler import ScrollEventHandler
from lmi.utils.name_generator import HasUniqueNameMixin


@attr.s(auto_attribs=True, kw_only=True)
class Component(
    DisplayEventHandler, LLMCanInteractWithMixin, LLMCanViewMixin, HasUniqueNameMixin
):
    preferred_size: int = None
    flex_factor: float = 1.0  # 0 = fixed, 1 = normal, inf = absorb all difference

    @property
    def min_size(self) -> int:
        return self.preferred_size

    @property
    def max_size(self) -> int:
        return self.preferred_size

    # TODO: move these to abstract layout component
    # @property
    # @abstractmethod
    # def components(self) -> list[Component]:
    #     pass

    # @property
    # def visible_components(self) -> list[Component]:
    #     return self.components
