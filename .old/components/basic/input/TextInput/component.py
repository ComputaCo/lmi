from __future__ import annotations
from abc import abstractmethod

import re
from lmi.app import App
from lmi.components.basic.Text import Text
from pydantic import BaseModel
from lmi.components.core.TextInput.events import (
    ClearSelectionsEvent,
    DeleteTextEvent,
    InsertTextEvent,
    SelectTextEvent,
    SetCursorPositionEvent,
    SetInsertModeEvent,
    SetTextEvent,
)
from lmi.handlers.advanced_keyboard_event_handler import AdvancedKeyboardEventHandler

from lmi.utils.event_target import ReversibleEvent, EventTarget, ReversibleEventHandler
from lmi.consts.keys import (
    ALT,
    BACKSPACE,
    CAPS_LOCK,
    CTRL,
    DELETE,
    DOWN,
    END,
    ESC,
    HOME,
    INSERT,
    LEFT,
    PAGE_DOWN,
    PAGE_UP,
    RIGHT,
    SHIFT,
    SUPER,
    TAB,
    UP,
    F1,
    F2,
    F3,
    F4,
    F5,
    F6,
    F7,
    F8,
    F9,
    F10,
    F11,
    F12,
)
from lmi.handlers import KeyboardEventHandler
from lmi.components.Component import Component
from lmi.handlers.focus_event_handler import FocusEventHandler


class TextInput(
    Text,
    AdvancedKeyboardEventHandler,
    KeyboardEventHandler,
    FocusEventHandler,
    EventTarget["TextInput"],
):
    ignore_events = False
    on_change: callable
    before_change: callable  ##### implement this

    _selected_text_start_idx: int or None = None
    _selected_text_end_idx: int or None = None

    @property
    def selected_text_start_idx(self) -> int or None:
        return self._selected_text_start_idx

    @selected_text_start_idx.setter
    def selected_text_start_idx(self, value: int or None):
        self.set_selection_indeces(value, self.selected_text_end_idx)

    @property
    def selected_text_end_idx(self) -> int or None:
        return self._selected_text_end_idx

    @selected_text_end_idx.setter
    def selected_text_end_idx(self, value: int or None):
        self.set_selection_indeces(self.selected_text_start_idx, value)

    @property
    def selected_text(self) -> str or None:
        if self.selected_text_start_idx is None or self.selected_text_end_idx is None:
            return None
        else:
            return self.text[self.selected_text_start_idx : self.selected_text_end_idx]

    def set_selection_indeces(self, start: int, end: int):
        self.do(SelectTextEvent(target=self, start=start, end=end))

    _cursor_pos: int = 0

    @property
    def cursor_pos(self) -> int:
        return self._cursor_pos

    @cursor_pos.setter
    def cursor_pos(self, pos: int):
        self.do(SetCursorPositionEvent(target=self, cursor_pos=pos))

    insert_cursor_char: str = "|"
    overwrite_cursor_char: str = "█"

    _insert_mode: bool = True  # True = insert, False = overwrite

    @property
    def insert_mode(self) -> bool:
        return self._insert_mode

    @insert_mode.setter
    def insert_mode(self, mode: bool):
        self.do(SetInsertModeEvent(target=self, new_insert_mode=mode))

    @property
    def cursor_char(self) -> str:
        match self.inesrt_mode:
            case True:
                return self.insert_cursor_char
            case False:
                return self.overwrite_cursor_char

    @property
    def text_with_cursor_and_highlight(self) -> str:
        return (
            self.text[: self.cursor_pos]
            + self.cursor_char
            + self.text[self.cursor_pos :]
        )

    def llm_render(self) -> str:
        orig_text = self.text
        self.text = self.text_with_cursor_and_highlight
        rendering = super().render_llm()
        self.text = orig_text
        return rendering

    # # The characters that the cursor can jump to
    # JUMP_POS_CHARS = [
    #     " ",
    #     "\n",
    #     "\t",
    #     "\r",
    #     "\v",
    #     "\f",
    #     ".",
    #     ",",
    #     ";",
    #     ":",
    #     "'",
    #     '"',
    #     "(",
    #     ")",
    #     "[",
    #     "]",
    #     "{",
    #     "}",
    #     "<",
    #     ">",
    #     "/",
    #     "\\",
    #     "|",
    #     "-",
    #     "_",
    #     "=",
    #     "+",
    #     "*",
    #     "&",
    #     "^",
    #     "%",
    #     "$",
    #     "#",
    #     "@",
    #     "!",
    #     "?",
    #     "~",
    #     "`",
    # ]
    # # Escape all the characters to make re able to use them
    # ESCAPED_JUMP_POS_CHARS = [re.escape(char) for char in JUMP_POS_CHARS] + [r'\s+']
    # # Join all the characters together inside a character class
    # JUMP_POS_CHARS_PATTERN = "[" + "".join(ESCAPED_JUMP_POS_CHARS) + "]"
    # # Compile the regex
    # JUMP_POS_CHARS_RE = re.compile(JUMP_POS_CHARS_PATTERN)
    JUMP_POS_CHARS_RE = re.compile(r"\W+")

    @property
    def lines(self) -> list[str]:
        return self.text.split("\n")

    @lines.setter
    def lines(self, value: list[str]):
        self.set_text("\n".join(value))

    @property
    def cursor_y(self) -> int:
        return self.text[: self.cursor_pos].count("\n")

    @property
    def cursor_x(self) -> int:
        return self.cursor_pos - self.text[: self.cursor_pos].rfind("\n")

    @cursor_y.setter
    def cursor_y(self, value: int):
        value = min(value, len(self.lines) - 1)
        value = max(value, 0)
        col_offset = self.cursor_x
        line_offset = sum(len(line) + 1 for line in self.lines[:value])
        self.cursor_pos = line_offset + col_offset

    @cursor_x.setter
    def cursor_x(self, value: int):
        value = min(value, len(self.lines[self.cursor_y]))
        value = max(value, 0)
        line_offset = sum(len(line) + 1 for line in self.lines[: self.cursor_y])
        self.cursor_pos = line_offset + value

    @property
    def word_indecies(self) -> list[int]:
        indecies = [0]

        # Get indecies of all the matches
        for match in self.JUMP_POS_CHARS_RE.finditer(self.text):
            indecies.append(match.start())

        # Add the end of the string
        indecies.append(len(self.text))

        return indecies

    @property
    def next_word_index(self) -> int:
        for index in self.word_indecies:
            if index > self.cursor_pos:
                return index
        else:
            return len(self.text)

    @property
    def prev_word_index(self) -> int:
        for index in reversed(self.word_indecies):
            if index < self.cursor_pos:
                return index
        else:
            return 0

    key_bindings = {
        (INSERT,): lambda self, _: self.toggle_insert(),
        (BACKSPACE,): lambda self, _: self.backspace(),
        (CTRL, BACKSPACE): lambda self, _: self.jump_backspace(),
        (DELETE,): lambda self, _: self.delete(),
        (CTRL, DELETE): lambda self, _: self.jump_delete(),
        (LEFT,): lambda self, _: self.move_cursor_left(),
        (RIGHT,): lambda self, _: self.move_cursor_right(),
        (UP,): lambda self, _: self.move_cursor_up(),
        (DOWN,): lambda self, _: self.move_cursor_down(),
        (CTRL, LEFT): lambda self, _: self.jump_cursor_left(),
        (CTRL, RIGHT): lambda self, _: self.jump_cursor_right(),
        (PAGE_UP,): lambda self, _: self.jump_cursor_up(),
        (PAGE_DOWN,): lambda self, _: self.jump_cursor_down(),
        (HOME,): lambda self, _: self.move_cursor_to_home(),
        (END,): lambda self, _: self.move_cursor_to_end(),
        (CTRL, HOME): lambda self, _: self.jump_cursor_to_home(),
        (CTRL, END): lambda self, _: self.jump_cursor_to_end(),
        (TAB,): lambda self, _: self.tab(),
        (ESC,): lambda self, _: self.clear_selections(),
        (CTRL, "a"): lambda self, _: self.select_all(),
        (CTRL, "c"): lambda self, _: self.copy(),
        (CTRL, "x"): lambda self, _: self.cut(),
        (CTRL, "v"): lambda self, _: self.paste(),
        (CTRL, "z"): lambda self, _: self.undo(),
        (CTRL, "y"): lambda self, _: self.redo(),
        (CTRL, UP): lambda self, _: self.move_line_up(),
        (CTRL, DOWN): lambda self, _: self.move_line_down(),
        # (F1,): lambda self, _: True, # reqd to prevent insert operation
        # (F2,): lambda self, _: True, # reqd to prevent insert operation
        # (F3,): lambda self, _: True, # reqd to prevent insert operation
        # (F4,): lambda self, _: True, # reqd to prevent insert operation
        # (F5,): lambda self, _: True, # reqd to prevent insert operation
        # (F6,): lambda self, _: True, # reqd to prevent insert operation
        # (F7,): lambda self, _: True, # reqd to prevent insert operation
        # (F8,): lambda self, _: True, # reqd to prevent insert operation
        # (F9,): lambda self, _: True, # reqd to prevent insert operation
        # (F10,): lambda self, _: True, # reqd to prevent insert operation
        # (F11,): lambda self, _: True, # reqd to prevent insert operation
        # (F12,): lambda self, _: True, # reqd to prevent insert operation
    }

    def toggle_insert(self):
        self.insert_mode = not self.insert_mode

    def backspace(self):
        if self.selected_text is not None:
            self.delete_selection()
            return
        if self.cursor_pos == 0:
            return
        self.delete_text(chars_before=1)

    def jump_backspace(self):
        if self.selected_text is not None:
            self.delete_selection()
            return
        if self.cursor_pos == 0:
            return
        # Delete from cursor pos to the prev word index
        self.delete_text(chars_before=self.cursor_pos - self.prev_word_index)

    def delete(self):
        if self.selected_text is not None:
            self.delete_selection()
            return
        if self.cursor_pos == len(self.text) - 1:
            return

        if self.insert_mode:
            self.delete_text(chars_after=1)
        else:
            # just move the cursor forward
            self.cursor_pos += 1

        self.on_change(self.text)

    def jump_delete(self):
        if self.selected_text is not None:
            self.delete_selection()
            return
        if self.cursor_pos == len(self.text):
            return

        if self.insert_mode:
            # Delete from cursor pos to the next word index
            self.delete_text(chars_after=self.next_word_index - self.cursor_pos)
        else:
            # just move the cursor forward
            self.cursor_pos = self.next_word_index

    def move_cursor_left(self):
        self.cursor_x -= 1

    def move_cursor_right(self):
        self.cursor_x += 1

    def move_cursor_up(self):
        self.cursor_y -= 1

    def move_cursor_down(self):
        self.cursor_y += 1

    def jump_cursor_left(self):
        self.cursor_pos = self.prev_word_index

    def jump_cursor_right(self):
        self.cursor_pos = self.next_word_index

    def jump_cursor_up(self):
        self.cursor_pos -= self.size

    def jump_cursor_down(self):
        self.cursor_pos += self.size

    def move_cursor_to_home(self):
        self.cursor_x = 0

    def move_cursor_to_end(self):
        self.cursor_x = len(self.lines[self.cursor_y])

    def jump_cursor_to_home(self):
        self.cursor_pos = 0

    def jump_cursor_to_end(self):
        self.cursor_pos = len(self.text)

    def tab(self):
        # only one character, so just insert it
        self.insert_text("\t")

    def select_all(self):
        self.set_selection_indeces(0, len(self.text))

    def copy(self):
        App.current().clipboard = self.selected_text

    def cut(self):
        App.current().clipboard = self.selected_text
        self.delete_text(self.selected_text_start_idx, self.selected_text_end_idx)

    def paste(self):
        self.insert_text(App.current().clipboard)

    def insert_text(self, text: str):
        self.do(InsertTextEvent(target=self, text=text))

    def delete_text(self, chars_before: int, chars_after: int):
        self.do(
            DeleteTextEvent(
                target=self,
                delete_chars_before_cursor=chars_before,
                delete_chars_after_cursor=chars_after,
            )
        )

    def delete_selection(self):
        if self.selected_text is None:
            raise ValueError("No text selected")

        self.delete_text(
            chars_before=self.selected_text_start_idx,
            chars_after=self.selected_text_end_idx,
        )

    def clear_selection(self):
        self.do(ClearSelectionsEvent(target=self))

    def move_line_up(self):
        self._swap_lines(self.cursor_y, self.cursor_y - 1)

    def move_line_down(self):
        self._swap_lines(self.cursor_y, self.cursor_y + 1)

    def _swap_lines(self, line1: int, line2: int):
        old_lines = self.lines
        new_lines = old_lines.copy()
        new_lines[line1] = old_lines[line2]
        new_lines[line2] = old_lines[line1]
        self.lines = new_lines

    def set_text(self, text: str):
        self.do(SetTextEvent(target=self, text=text))

    def default_key_binding(
        self, event: AdvancedKeyboardEventHandler.AdvancedKeyboardEvent
    ):
        if event.is_key_combo:
            return  # this is an unhandled key combo
        self.insert_text(event.raw_input)

    def do(self, action: EventTarget.Event):
        x = super().do(action)
        if self.on_change and not self.ignore_events:
            self.on_change(self.text)
        return x
