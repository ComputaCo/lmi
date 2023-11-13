from contextlib import contextmanager
from typing import Any
from lmi.components.basic.Button import Button
from lmi.components.layout.Stack import Stack
from lmi.components.basic.Text import Text
from lmi.handlers.click_event_handler import ClickEventHandler
from pydantic import BaseModel
from lmi.components.Component import Component


class AbstractToggle(Button, ClickEventHandler):
    toggled = False

    ignore_events = False  # set to avoid chain-reaction of events
    on_change: callable[[bool], Any] = None

    selectable = False

    @contextmanager
    def ignore_events(self):
        self.ignore_events = True
        yield
        self.ignore_events = False

    @property
    def text_with_toggle(self) -> str:
        return f"[{'x' if self.toggled else ' '}] {self._orig_text}"

    def on_single_left_click(self, event: ClickEventHandler.ClickEvent):
        self.toggle()

    def toggle(self):
        if self.toggled:
            self.toggle_false()
        else:
            self.toggle_true()

    def toggle_true(self):
        self.toggled = True
        if self.on_change and not self.ignore_events:
            self.on_change(self.toggled)

    def toggle_false(self):
        self.toggled = False
        if self.on_change and not self.ignore_events:
            self.on_change(self.toggled)

    def children(self) -> list[Component]:
        return [Text(size=self.size, text=self.text_with_toggle)]
