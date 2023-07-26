from abc import ABC
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.event_handler import EventHandler


class FocusEventHandler(EventHandler, LLMCanInteractWithMixin, ABC):
    class FocusEvent(EventHandler.Event):
        pass

    _focused: bool = False

    @property
    def focused(self) -> bool:
        return self._focused

    @focused.setter
    def focused(self, value: bool):
        self._focused = value
        if value:
            self.on_focus(self.FocusEvent())
        else:
            self.on_blur(self.FocusEvent())

    def on_focus(self, event: FocusEvent):
        pass

    def on_blur(self, event: FocusEvent):
        pass
