from contextlib import contextmanager
from typing import Any
from lmi.components.core.AbstractToggle import AbstractToggle
from lmi.components.basic.Button import Button
from lmi.components.layout.Stack import Stack
from lmi.components.basic.Text import Text
from lmi.handlers.click_event_handler import ClickEventHandler
from pydantic import BaseModel
from lmi.components.Component import Component


class Checkbox(AbstractToggle):
    def check(self):
        self.toggle_true()

    def uncheck(self):
        self.toggle_false()
