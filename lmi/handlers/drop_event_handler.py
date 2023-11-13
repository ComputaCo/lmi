from abc import ABC
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.mouse_event_handler import BaseMouseEventHandler


class DropEvent(BaseMouseEventHandler.MouseEvent):
    obj: object


class DropEventHandler(BaseMouseEventHandler, LLMCanInteractWithMixin, ABC):
    def on_drop(self, event: DropEvent):
        """Triggered on Y when obj is dropped on Y."""
        pass
