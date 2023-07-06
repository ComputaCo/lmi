from enum import Enum
from typing import Literal
import attr
from gptos.lmi.handlers.event_handler import EventHandler


class ScrollEventHandler(EventHandler):
    @attr.s(auto_attribs=True)
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

    def scroll(self, event: ScrollEvent):
        pass
