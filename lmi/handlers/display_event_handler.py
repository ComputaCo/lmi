from abc import ABC
from lmi.abstract.interactable import LLMCanInteractWithMixin

from lmi.handlers.event_handler import EventHandler


class DisplayEvent(EventHandler.Event):
    visible: bool


class DisplayEventHandler(EventHandler, LLMCanInteractWithMixin, ABC):
    _visible: bool = False

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value
        event = DisplayEvent(visible=value)
        if value:
            self.on_show(event)
        else:
            self.on_hide(event)

    def on_show(self, event: DisplayEvent):
        """Triggered when a component is starts being shown"""
        pass

    def on_hide(self, event: DisplayEvent):
        """Triggered when a component stops being shown"""
        pass
