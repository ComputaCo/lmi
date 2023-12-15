from abc import ABC, abstractmethod
from langchain.tools import BaseTool
from pydantic import BaseModel
from lmi.components.abstract.component import Component


class Peripheral(BaseModel, ABC):
    @abstractmethod
    def lc_tools(self, component: Component) -> list[BaseTool]:
        pass
