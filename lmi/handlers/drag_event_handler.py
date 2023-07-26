from abc import ABC
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.mouse_event_handler import BaseMouseEventHandler


class DragEventHandler(BaseMouseEventHandler, LLMCanInteractWithMixin, ABC):
    class DragEvent(BaseMouseEventHandler.MouseEvent):
        obj: object

    def on_drag_start(self, event: DragEvent):
        """Triggered on X when X begins being draged."""

    def on_drag_end(self, event: DragEvent):
        """Triggered on X wheMouseEventHandlerd."""
