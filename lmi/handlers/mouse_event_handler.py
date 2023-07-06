from abc import ABC
from enum import Enum
from typing_extensions import Literal
import attr

from gptos.lmi.handlers.event_handler import EventHandler


class MouseEventHandler(EventHandler, ABC):
    @attr.s(auto_attribs=True)
    class MouseEvent(EventHandler.Event):
        class Buttons(Enum):
            LEFT = "left"
            MIDDLE = "middle"
            RIGHT = "right"

        button: Buttons = Buttons.LEFT
