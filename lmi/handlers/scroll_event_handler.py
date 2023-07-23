from enum import Enum
from typing import Literal
import attr
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.event_handler import EventHandler


class ScrollEventHandler(EventHandler, LLMCanInteractWithMixin):
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

    def on_scroll(self, event: ScrollEvent):
        pass

    @property
    def on_scroll_tool(self) -> [BaseTool]:
        return ...

    @property
    def tools(self) -> list:
        return super().tools + [self.on_scroll_tool]
