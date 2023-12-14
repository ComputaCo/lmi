from abc import ABC, abstractmethod
from typing import Generator
from langchain.schema import BaseMessage
from langchain.tools import BaseTool


class LLMCanViewMixin(ABC):
    @abstractmethod
    def render_llm(self) -> str:
        pass

    @abstractmethod
    def render_messages_llm(self) -> Generator[BaseMessage, None, None]:
        pass


class LLMCanInteractWithMixin(ABC):
    @property
    @abstractmethod
    def llm_tools(self) -> list[BaseTool]:
        pass


class RendersToHTMLMixin(ABC):
    @abstractmethod
    def render_html(self) -> reactpy.Component:
        pass
