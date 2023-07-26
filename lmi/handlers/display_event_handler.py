from abc import ABC
from lmi.abstract.interactable import LLMCanInteractWithMixin

from lmi.handlers.event_handler import EventHandler


class DisplayEventHandler(EventHandler, LLMCanInteractWithMixin, ABC):
    class DisplayEvent(EventHandler.Event):
        pass

    _visible: bool = False

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value
        if value:
            self.on_show(self.DisplayEvent())
        else:
            self.on_hide(self.DisplayEvent())

    def on_show(self, event: DisplayEvent):
        """Triggered when a component is starts being shown"""
        pass

    def on_hide(self, event: DisplayEvent):
        """Triggered when a component stops being shown"""
        pass
