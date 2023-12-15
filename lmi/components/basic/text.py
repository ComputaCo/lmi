from abc import abstractmethod
from typing import Generator

from langchain.schema import BaseMessage, HumanMessage
from langchain.tools import BaseTool
from reactpy.core.component import (
    Component as reactpy_Component,
    component as reactpy_component,
)

from lmi.components.abstract.component import Component

class Text(Component):
    text: str

    def render_to_messages(self):
        yield from [HumanMessage(content=self.text)]
