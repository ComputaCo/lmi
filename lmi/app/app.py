from langchain.tools import BaseTool
from pydantic import BaseModel

from lmi.components.Component import Component
from lmi.utils.context_managed import ContextManaged


class App(Component, BaseModel, ContextManaged):
    clipboard: str or None = None

    @property
    def _hover_tool(self):
        pass  # TODO: implement

    @property
    def _type_tool(self):
        pass  # TODO: implement

    @property
    def _click_tool(self):
        pass  # TODO: implement

    @property
    def _scroll_tool(self):
        pass  # TODO: implement

    @property
    def _drag_tool(self):
        pass  # TODO: implement

    @property
    def _drop_tool(self):
        pass  # TODO: implement

    @property
    def llm_tools(self) -> list[BaseTool]:
        return [child.llm_tools for child in self.visible_children] + [
            self._hover_tool,
            self._type_tool,
            self._click_tool,
            self._scroll_tool,
            self._drag_tool,
            self._drop_tool,
        ]

    def serve(self, host, port):
        pass

    def run(self, agent):
        pass

    def cli(self):
        pass
