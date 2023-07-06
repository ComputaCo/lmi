from functools import lru_cache
import attr
from gptos.tools.tool import Tool, Toolbox
from gptos.lmi.components.stack import Stack


@attr.s(auto_attribs=True)
class Group(Stack):
    """
    Provides a scope for grouping components together.
    """

    description: str

    @property
    @lru_cache()
    def tools(self) -> list[Tool]:
        tools = super().tools
        toolbox = Toolbox(name=self.name, description=self.description, tools=tools)
        return [toolbox]
