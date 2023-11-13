from abc import ABC
from enum import Enum
from lmi.abstract.llm_interface import LLMCanInteractWithMixin
from lmi.handlers.event_handler import BaseEventHandler


class ScrollEvent(BaseEventHandler.Event):
    class Direction(Enum):
        UP = "up"
        DOWN = "down"

    class Speed(Enum):
        SLOW = "slow"
        MEDIUM = "medium"
        FAST = "fast"

    direction: Direction
    speed: Speed = Speed.MEDIUM


class ScrollEventHandler(BaseEventHandler, LLMCanInteractWithMixin, ABC):
    def on_scroll(self, event: ScrollEvent):
        pass
