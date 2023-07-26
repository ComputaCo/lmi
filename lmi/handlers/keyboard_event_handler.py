from abc import ABC
from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.event_handler import EventHandler


class KeyboardEventHandler(EventHandler, LLMCanInteractWithMixin, ABC):
    class KeyboardEvent(EventHandler.Event):
        raw_input: str

    def on_key_input(self, event: KeyboardEvent):
        pass
