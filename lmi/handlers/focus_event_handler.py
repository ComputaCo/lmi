import attr
from lmi.abstract.interactable import LLMCanInteractWithMixin

from lmi.handlers.event_handler import EventHandler


class FocusEventHandler(EventHandler, LLMCanInteractWithMixin):
    @attr.s(auto_attribs=True)
    class FocusEvent(EventHandler.Event):
        pass

    def on_focus(self, event: FocusEvent):
        pass

    def on_unfocus(self, event: FocusEvent):
        pass

    @property
    def on_focus_tool(self) -> [BaseTool]:
        return ...

    @property
    def on_unfocus_tool(self) -> [BaseTool]:
        return ...

    @property
    def tools(self) -> list:
        return super().tools + [self.on_focus_tool, self.on_unfocus_tool]
