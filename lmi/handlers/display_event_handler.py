import attr
from lmi.abstract.interactable import LLMCanInteractWithMixin

from lmi.handlers.event_handler import EventHandler


class DisplayEventHandler(EventHandler, LLMCanInteractWithMixin):
    @attr.s(auto_attribs=True)
    class DisplayEvent(EventHandler.Event):
        pass

    def on_show(self, event: DisplayEvent):
        """Triggered when a component is starts being shown"""
        pass

    def on_hide(self, event: DisplayEvent):
        """Triggered when a component stops being shown"""
        pass

    @property
    def on_show_tool(self) -> [BaseTool]:
        return ...

    @property
    def on_hide_tool(self) -> [BaseTool]:
        return ...

    @property
    def tools(self) -> list:
        return super().tools + [self.on_show_tool, self.on_hide_tool]
