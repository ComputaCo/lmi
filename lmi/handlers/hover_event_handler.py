from abc import ABC
from enum import Enum
from lmi.abstract.llm_interface import LLMCanInteractWithMixin
from lmi.handlers.mouse_event_handler import BaseMouseEventHandler


class HoverEvent(BaseMouseEventHandler.MouseEvent):
    class Duration(Enum):
        SLOW = "slow"
        MEDIUM = "medium"
        FAST = "fast"

    duration: Duration = Duration.MEDIUM


class HoverEventHandler(BaseMouseEventHandler, LLMCanInteractWithMixin, ABC):
    def on_hover(self, event: HoverEvent):
        pass
