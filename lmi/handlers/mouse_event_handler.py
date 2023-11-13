from abc import ABC
from enum import Enum
from typing_extensions import Literal
from lmi.abstract.interactable import LLMCanInteractWithMixin

from lmi.handlers.event_handler import EventHandler


class MouseEvent(EventHandler.Event):
    class Buttons(Enum):
        LEFT = "left"
        MIDDLE = "middle"
        RIGHT = "right"

    button: Buttons = Buttons.LEFT


class BaseMouseEventHandler(EventHandler, LLMCanInteractWithMixin, ABC):
    pass
