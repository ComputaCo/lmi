from functools import lru_cache
from pathlib import Path
import pickle
from types import ModuleType
import attr

from gptos.tools.tool import PyObjectTool, Tool
from gptos.lmi.components.description import Description


@attr.s(auto_attribs=True, slots=True)
class Object(Description.variant(object)):

    __pyobj_tool: PyObjectTool

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        if self.name is None and hasattr(self.obj, "__name__"):
            self.name = self.obj.__name__
        self.__pyobj_tool = PyObjectTool(self.clazz)

    def loader(self, path: Path = None):
        with open(path, "rb") as f:
            return pickle.load(f)

    @property
    @lru_cache()
    def tools(self) -> list[Tool]:
        return [self.__pyobj_tool]
