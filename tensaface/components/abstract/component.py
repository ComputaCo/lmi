from __future__ import annotations

from abc import ABC, abstractmethod
from langchain.tools import BaseTool

from pydantic import BaseModel

from tensaface._internal.llm_interface import LLMCanInteractWithMixin, LLMCanViewMixin
from tensaface.handlers import DisplayEventHandler, EventHandler


class Component(
    DisplayEventHandler,
    LLMCanInteractWithMixin,
    LLMCanViewMixin,
    BaseModel,
    ABC,
):
    name: str
    hidden = False

    @property
    @abstractmethod
    def children(self) -> list[Component]:
        pass

    def get_child_by_name(self, name: str) -> Component:
        for child in self.children:
            if child.name == name:
                return child
        raise ValueError(f"No child with name {name}")

    @property
    def llm_tools(self) -> list[BaseTool]:
        tools = []

        # add event-handler specific tools
        for T_event_handler in EventHandler.__subclasses__():
            t_components = [
                component
                for component in self.children
                if isinstance(component, T_event_handler)
            ]
            if t_components:
                tool = T_event_handler.llm_tool(components=t_components)
                tools.append(tool)

        return tools

    def on_show(self):
        pass

    def on_hide(self):
        pass
