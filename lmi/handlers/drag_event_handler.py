import attr
from lmi.abstract.interactable import LLMCanInteractWithMixin

from lmi.handlers.mouse_event_handler import MouseEventHandler


class DragEventHandler(MouseEventHandler, LLMCanInteractWithMixin):
    @attr.s(auto_attribs=True)
    class DragEvent(MouseEventHandler.MouseEvent):
        obj: object

    def on_drag_start(self, event: DragEvent):
        """Triggered on X when X begins being draged."""
        pass

    def on_drag_end(self, event: DragEvent):
        """Triggered on X when X stops being draged."""
        pass

    @property
    def on_drag_start_tool(self) -> [BaseTool]:
        return ...

    @property
    def on_drag_end_tool(self) -> [BaseTool]:
        return ...

    @property
    def tools(self) -> list:
        return super().tools + [self.start_drag_tool, self.end_drag_tool]
