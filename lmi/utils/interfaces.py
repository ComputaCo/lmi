from abc import ABC, abstractmethod
from typing import Generator

from reactpy.core.component import Component as reactpy_Component, component as reactpy_component
from langchain.schema import BaseMessage
from langchain.tools import BaseTool


class LLMCanViewMixin(ABC):
    @abstractmethod
    def render_llm(self) -> str:
        raise NotImplementedError("`render_llm` not implemented")

    @abstractmethod
    def render_messages_llm(self) -> Generator[BaseMessage, None, None]:
        raise NotImplementedError("`render_messages_llm` not implemented")


class LLMCanInteractWithMixin(ABC):
    @property
    @abstractmethod
    def llm_tools(self) -> list[BaseTool]:
        raise NotImplementedError("`llm_tools` not implemented")


class RendersToReactPyMixin(ABC):
    @abstractmethod
    @reactpy_component
    def render_reactpy(self) -> reactpy_Component:
        raise NotImplementedError("`render_reactpy` not implemented")
