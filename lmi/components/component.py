from __future__ import annotations
from math import inf
import re
from typing import Type

import attr

from lmi.utils import normalize
from lmi.misc.alignment import Alignment
from lmi.commponents.abstract_component import AbstractComponent
from lmi.handlers.display_event_handler import DisplayEventHandler
from lmi.handlers.drag_event_handler import DragEventHandler
from lmi.handlers.drop_event_handler import DropEventHandler
from lmi.handlers.focus_event_handler import FocusEventHandler
from lmi.handlers.keyboard_event_handler import KeyboardEventHandler
from lmi.handlers.mouse_event_handler import MouseEventHandler
from lmi.handlers.scroll_event_handler import ScrollEventHandler
from lmi.utils.name_generator import UniqueNameMixin
from services.keyboard_service import KeyboardService
from utils.sort_heterogenous_numerical_suffix_list import (
    sort_heterogenous_numerical_suffix_list,
)


@attr.s(auto_attribs=True)
class Component(AbstractComponent, UniqueNameMixin):

    name: str = attr.ib(default=None)

    @property
    def max_size(self) -> int:
        return self.preferred_size

    @property
    def min_size(self) -> int:
        return self.preferred_size

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def render(self, size) -> str:
        return ""
