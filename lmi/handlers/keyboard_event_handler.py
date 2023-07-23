import attr
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.event_handler import EventHandler


class KeyboardEventHandler(EventHandler, LLMCanInteractWithMixin):
    @attr.s(auto_attribs=True)
    class KeyboardEvent(EventHandler.Event):
        keys: list[str] = attr.ib([])

        @property
        def key(self):
            if len(self.keys) == 0:
                return None
            return filter(lambda key: len(key) == 1, self.keys)[0]

    def on_key_input(self, event: KeyboardEvent):
        pass

    @property
    def on_key_input_tool(self) -> [BaseTool]:
        return ...

    @property
    def tools(self) -> list:
        return super().tools + [self.on_key_input_tool]
