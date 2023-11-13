from lmi.components.core.TextInput.component import TextInput
from lmi.utils.event_target import (
    CompositeEvent,
    ReversibleEvent,
    ReversibleEventHandler,
)


class TextInputEvent(ReversibleEvent[TextInput]):
    pass


class SetCursorPositionEvent(TextInputEvent):
    cursor_pos: int
    prev_cursor_pos: int = None

    def apply(self):
        self.prev_cursor_pos = self.target.cursor_pos
        self.target.cursor_pos = self.cursor_pos

    def reverse(self):
        self.target.cursor_pos = self.prev_cursor_pos


class SetInsertModeEvent(TextInputEvent):
    new_insert_mode: bool
    prev_insert_mode: bool = None

    def apply(self):
        self.prev_insert_mode = self.target.insert_mode
        self.target.insert_mode = self.new_insert_mode

    def reverse(self):
        self.target.insert_mode = self.prev_insert_mode


class SetTextEvent(TextInputEvent):
    text: str

    prev_text: str or None = None

    def apply(self):
        self.prev_text = self.target.text
        self.target.text = self.text

    def reverse(self):
        self.target.text = self.prev_text


class InsertTextEvent(TextInputEvent, CompositeEvent[TextInput]):
    text: str

    def apply(self):
        self.prev_text = self.target.text

        if self.target.insert_mode and self.target.selected_text is None:
            NormalInsertTextEvent.normal_insert(self)
        elif self.target.insert_mode and self.target.selected_text is not None:
            ReplaceSelectionInsertTextEvent.replace_selection_insert(self)
        else:
            OverwriteInsertTextEvent.overwrite_insert(self)

    def reverse(self):
        self.text_input.text = self.prev_text


class NormalInsertTextEvent(InsertTextEvent):
    def normal_insert(self):
        # insert the text at the cursor pos
        new_text = (
            self.target.text[: self.target.cursor_pos]
            + self.text
            + self.target.text[self.target.cursor_pos :]
        )
        set_text_event = TextInput.SetTextEvent(target=self.target, text=new_text)
        self.do(set_text_event)

        # set the cursor pos to the end of the inserted text
        set_cursor_pos_event = TextInput.SetCursorPositionEvent(
            target=self.target,
            cursor_pos=self.target.cursor_pos + len(self.text),
        )
        self.do(set_cursor_pos_event)


class ReplaceSelectionInsertTextEvent(InsertTextEvent):
    def replace_selection_insert(self):
        # replace the selection with the text
        new_text = (
            self.target.text[: self.target.selected_text_start_idx]
            + self.text
            + self.target.text[self.target.selected_text_end_idx :]
        )
        set_text_event = TextInput.SetTextEvent(target=self.target, text=new_text)
        self.do(set_text_event)

        # clear the selection indeces
        clear_selections_event = ClearSelectionsEvent(target=self.target)
        self.do(clear_selections_event)

        # set the cursor pos to the end of the inserted text
        set_cursor_pos_event = SetCursorPositionEvent(
            target=self.target,
            cursor_pos=self.target.selected_text_start_idx + len(self.text),
        )
        self.do(set_cursor_pos_event)


class OverwriteInsertTextEvent(InsertTextEvent):
    def overwrite_insert(self):
        new_len = self.target.cursor_pos + len(self.text)
        new_text = self.target.text
        new_cursor_pos = self.target.cursor_pos + len(self.text)

        # maybe pad the text with spaces to the length of the cursor pos + inserted text
        # then replace the text starting from the cursor pos with the text
        if new_len > len(self.target.text):
            new_text += " " * (new_len - len(self.target.text))
        new_text = (
            new_text[: self.target.cursor_pos] + self.text + new_text[new_cursor_pos:]
        )
        set_text_event = SetTextEvent(target=self.target, text=new_text)
        self.do(set_text_event)

        # set the cursor pos to the end of the inserted text
        set_cursor_pos_event = SetCursorPositionEvent(
            target=self.target,
            cursor_pos=self.target.cursor_pos + len(self.text),
        )
        self.do(set_cursor_pos_event)


class SelectTextEvent(TextInputEvent):
    start: int
    end: int

    prev_selected_text_start_idx: int or None = None
    prev_selected_text_end_idx: int or None = None

    def apply(self):
        self.prev_selected_text_start_idx = self.target._selected_text_start_idx
        self.prev_selected_text_end_idx = self.target._selected_text_end_idx
        self.target._selected_text_start_idx = self.start
        self.target._selected_text_end_idx = self.end

    def reverse(self):
        self.target._selected_text_start_idx = self.prev_selected_text_start_idx
        self.target._selected_text_end_idx = self.prev_selected_text_end_idx


class ClearSelectionsEvent(SelectTextEvent):
    start = None
    end = None


class DeleteTextEvent(TextInputEvent, CompositeEvent[TextInput]):
    delete_chars_before_cursor: int = 0
    delete_chars_after_cursor: int = 0

    def apply(self):
        # delete the text before and after the cursor
        new_text = (
            self.target.text[: self.target.cursor_pos - self.chars_before_cursor]
            + self.target.text[self.target.cursor_pos + self.chars_after_cursor :]
        )
        set_text_event = SetTextEvent(target=self.target, text=new_text)
        self.do(set_text_event)

        # set the cursor pos to the end of the deleted text
        set_cursor_pos_event = SetCursorPositionEvent(
            target=self.target,
            cursor_pos=self.target.cursor_pos - self.chars_before_cursor,
        )
        self.do(set_cursor_pos_event)
