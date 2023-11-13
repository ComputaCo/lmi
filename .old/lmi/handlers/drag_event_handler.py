from abc import ABC
from lmi.abstract.llm_interface import LLMCanInteractWithMixin
from lmi.handlers.mouse_event_handler import BaseMouseEventHandler


class DragEvent(BaseMouseEventHandler.MouseEvent):
    obj: object


class DragEventHandler(BaseMouseEventHandler, LLMCanInteractWithMixin, ABC):
    def on_drag_start(self, event: DragEvent):
        """Triggered on X when X begins being draged."""

    def on_drag_end(self, event: DragEvent):
        """Triggered on X wheMouseEventHandlerd."""
