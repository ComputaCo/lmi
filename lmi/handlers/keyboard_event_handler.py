from abc import ABC
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.event_handler import EventHandler


class KeyboardEvent(EventHandler.Event):
    raw_input: str


class KeyboardEventHandler(EventHandler, LLMCanInteractWithMixin, ABC):
    def on_key_input(self, event: KeyboardEvent):
        pass
