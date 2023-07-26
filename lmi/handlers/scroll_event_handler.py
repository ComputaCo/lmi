from abc import ABC
from enum import Enum
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.event_handler import EventHandler


class ScrollEventHandler(EventHandler, LLMCanInteractWithMixin, ABC):
    class ScrollEvent(EventHandler.Event):
        class Direction(Enum):
            UP = "up"
            DOWN = "down"

        class Speed(Enum):
            SLOW = "slow"
            MEDIUM = "medium"
            FAST = "fast"

        direction: Direction
        speed: Speed = Speed.MEDIUM

    def on_scroll(self, event: ScrollEvent):
        pass
