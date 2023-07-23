import attr
from lmi.abstract.interactable import LLMCanInteractWithMixin

from lmi.handlers.mouse_event_handler import MouseEventHandler


class DropEventHandler(MouseEventHandler, LLMCanInteractWithMixin):
    @attr.s(auto_attribs=True)
    class DropEvent(MouseEventHandler.MouseEvent):
        obj: object

    def on_drop(self, event: DropEvent):
        """Triggered on Y when obj is dropped on Y."""
        pass

    @property
    def on_drop_tool(self) -> [BaseTool]:
        return ...

    @property
    def tools(self) -> list:
        return super().tools + [self.on_drop_tool]
