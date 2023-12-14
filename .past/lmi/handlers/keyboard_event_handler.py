from abc import ABC
from lmi.abstract.llm_interface import LLMCanInteractWithMixin
from lmi.handlers.event_handler import BaseEventHandler


class KeyboardEvent(BaseEventHandler.Event):
    raw_input: str


class KeyboardEventHandler(BaseEventHandler, LLMCanInteractWithMixin, ABC):
    def on_key_input(self, event: KeyboardEvent):
        pass
