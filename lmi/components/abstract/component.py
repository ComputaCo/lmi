from __future__ import annotations

from abc import ABC, abstractmethod
from langchain.tools import BaseTool

from pydantic import BaseModel

from lmi.utils.interfaces import LLMCanInteractWithMixin, LLMCanViewMixin, RendersToHTMLMixin
from lmi.handlers import DisplayEventHandler, EventHandler


class Component(
    RendersToHTMLMixin,
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

    # FIXME: implement this in the future when component trees become native tc objects
    # def __tensacode_render__(self, modality: tc.Modality):
    #     match modality:
    #         case tc.Modality.text:
    #             return self.render_llm()
    #         case tc.Modality.messages:
    #             return list(self.render_messages_llm())
    #         # Might be useful in the future
    #         # case tc.Modaity.image:
    #         #     ...
    #         case _:
    #             raise ValueError(f"Encoding modality {modality} not supported")

    def on_show(self):
        pass

    def on_hide(self):
        pass
