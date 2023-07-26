from contextlib import contextmanager
from typing import Any
from lmi.components.AbstractToggle import AbstractToggle
from lmi.components.Button import Button
from lmi.components.Stack import Stack
from lmi.components.Text import Text
from lmi.handlers.click_event_handler import ClickEventHandler
from pydantic import BaseModel
from lmi.components.Component import Component


class Option(AbstractToggle):
    def select(self):
        self.toggle_true()

    def unselect(self):
        self.toggle_false()
