from __future__ import annotations

from abc import ABC, abstractmethod
from langchain.tools import BaseTool

from pydantic import BaseModel, validator
# from reactpy.core.component import Component as reactpy_Component, component as reactpy_component

from lmi.utils.interfaces import LLMCanInteractWithMixin, LLMCanViewMixin, RendersToReactPyMixin
from lmi.handlers import DisplayEventHandler, EventHandler


class Component(
    RendersToReactPyMixin,
    LLMCanInteractWithMixin,
    LLMCanViewMixin,
    BaseModel,
    ABC,
):
    name: str = None
    
    @validator('name')
    def check_name(cls, v):
        if not v:
            ...  # TODO: find the lowest unused number suffix for this component's type
        return v

    @property
    @abstractmethod
    def children(self) -> list[Component]:
        # this is a property here because we don't want instructor to attempt populating all types of objects
        pass

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
