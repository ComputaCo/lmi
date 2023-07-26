from abc import ABC
from enum import Enum
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.mouse_event_handler import BaseMouseEventHandler


class HoverEventHandler(BaseMouseEventHandler, LLMCanInteractWithMixin, ABC):
    class HoverEvent(BaseMouseEventHandler.MouseEvent):
        class Duration(Enum):
            SLOW = "slow"
            MEDIUM = "medium"
            FAST = "fast"

        duration: Duration = Duration.MEDIUM

    def on_hover(self, event: HoverEvent):
        pass
