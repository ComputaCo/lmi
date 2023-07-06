from __future__ import annotations
from math import inf
import re
from typing import Type

import attr
from gptos.lmi.abstractions.abstract_component import AbstractComponent

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
from gptos.utils.sort_heterogenous_numerical_suffix_list import (
    sort_heterogenous_numerical_suffix_list,
)


@attr.s(auto_attribs=True)
class Component(AbstractComponent):

    name: str = attr.ib(default=None)

    __COMPONENT_NAMES: dict[Type, set[str]] = {}

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        if not self.name:
            self.name = self.generate_name()
        elif self.name in self._CLASS_COMPONENT_NAMES:
            self.name = self.generate_name()
        self._CLASS_COMPONENT_NAMES.append(self.name)

    @property
    @classmethod
    def _CLASS_COMPONENT_NAMES(cls) -> set[str]:
        if cls not in Component.__COMPONENT_NAMES:
            Component.__COMPONENT_NAMES[cls] = []
        return cls.__COMPONENT_NAMES[cls]

    @classmethod
    def generate_name(cls):
        for i in range(1, inf):
            name = f"{cls.__name__}{i}"
            if name not in cls._CLASS_COMPONENT_NAMES:
                return name
