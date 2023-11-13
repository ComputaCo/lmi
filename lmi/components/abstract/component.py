from __future__ import annotations
from abc import abstractmethod
from math import inf
import re
from typing import Type

import attr
from lmi.abstract.llm_interface import LLMCanInteractWithMixin, LLMCanViewMixin

from lmi.utils import normalize
from lmi.handlers.display_event_handler import DisplayEventHandler
from lmi.handlers.drag_event_handler import DragEventHandler
from lmi.handlers.drop_event_handler import DropEventHandler
from lmi.handlers.focus_event_handler import FocusEventHandler
from lmi.handlers.keyboard_event_handler import KeyboardEventHandler
from lmi.handlers.mouse_event_handler import BaseMouseEventHandler
from lmi.handlers.scroll_event_handler import ScrollEventHandler
from lmi.utils.name_generator import HasUniqueNameMixin


@attr.s(auto_attribs=True, kw_only=True)
class Component(
    DisplayEventHandler, LLMCanInteractWithMixin, LLMCanViewMixin, HasUniqueNameMixin
):
    name: str
    size: int

    @property
    @abstractmethod
    def components(self) -> list[Component]:
        pass

    @property
    def visible_components(self) -> list[Component]:
        return self.components
