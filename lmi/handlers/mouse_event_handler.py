from abc import ABC
from enum import Enum
from typing_extensions import Literal
from lmi.abstract.llm_interface import LLMCanInteractWithMixin

from lmi.handlers.event_handler import BaseEvent, BaseEventHandler


class MouseEvent(BaseEvent):
    class Buttons(Enum):
        LEFT = "left"
        MIDDLE = "middle"
        RIGHT = "right"

    button: Buttons = Buttons.LEFT

class 
    location: tuple[int, int] = (0, 0)  # TODO: how will i handle location???


class BaseMouseEventHandler(BaseEventHandler, LLMCanInteractWithMixin, ABC):
    pass
