from abc import ABC, abstractmethod

from langchain.tools import BaseTool


class LLMCanInteractWithMixin(ABC):
    @property
    @abstractmethod
    def tools(self) -> list[BaseTool]:
        pass
