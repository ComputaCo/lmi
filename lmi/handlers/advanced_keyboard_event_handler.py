from __future__ import annotations

from abc import abstractmethod
import re

from lmi.consts.keys import FULL_SPECIAL_KEYS
from lmi.handlers.keyboard_event_handler import KeyboardEventHandler


class AdvancedKeyboardEventHandler(KeyboardEventHandler):
    class AdvancedKeyboardEvent(KeyboardEventHandler.KeyboardEvent):
        IS_KEY_COMBO_PATTERN = f"({'|'.join(FULL_SPECIAL_KEYS)}\+)+(A-Z|a-z|0-9)"
        IS_KEY_COMBO_REGEX = re.compile(IS_KEY_COMBO_PATTERN)

        @property
        def is_key_combo(self) -> bool:
            return bool(self.IS_KEY_COMBO_REGEX.match(self.raw_input))

        @property
        def special_keys(self) -> list[str]:
            if not self.is_key_combo:
                return []
            return self.keys[:-1]

        @property
        def keys(self) -> list[str]:
            if not self.is_key_combo:
                return []
            return self.raw_input.split("+")

    key_bindings: dict[
        tuple[str, ...],
        callable[[tuple["AdvancedKeyboardEventHandler", AdvancedKeyboardEvent]]],
    ] = {}

    def on_key_input(self, event: KeyboardEventHandler.KeyboardEvent):
        if event.is_key_combo:
            for keys, callback in self.key_bindings.items():
                if keys == event.keys:
                    callback(self, event)
                    return
        self.default_key_input_binding(event)

    @abstractmethod
    def default_key_input_binding(self, event: KeyboardEventHandler.KeyboardEvent):
        pass
