from abc import ABC
from lmi.abstract.llm_interface import LLMCanInteractWithMixin
from lmi.handlers.event_handler import BaseEventHandler


class FocusEvent(BaseEventHandler.Event):
    focused: bool


class FocusEventHandler(BaseEventHandler, LLMCanInteractWithMixin, ABC):
    _focused: bool = False

    @property
    def focused(self) -> bool:
        return self._focused

    @focused.setter
    def focused(self, value: bool):
        self._focused = value
        event = FocusEvent(focused=value)
        if value:
            self.on_focus(event)
        else:
            self.on_blur(event)

    def on_focus(self, event: FocusEvent):
        pass

    def on_blur(self, event: FocusEvent):
        pass
