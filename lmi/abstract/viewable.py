from abc import ABC, abstractmethod
from typing import Generator
from langchain.schema import BaseMessage


class LLMCanViewMixin(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def render_messages(self) -> Generator[BaseMessage, None, None]:
        pass
