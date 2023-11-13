from abc import ABC
from lmi.abstract.llm_interface import LLMCanInteractWithMixin
from lmi.handlers.mouse_event_handler import BaseMouseEventHandler, MouseEvent


class DropEvent(MouseEvent):
    obj: object


class DropEventHandler(BaseMouseEventHandler, LLMCanInteractWithMixin, ABC):
    def __init_subclass__(cls) -> None:
        cls.llm_tools.append(Function)
        return super().__init_subclass__()

    def dispatch_drop(self):
        """Dispatches a drop event to the current mouse position."""
        pass

    def on_drop(self, event: DropEvent):
        """Triggered on Y when obj is dropped on Y."""
        pass
