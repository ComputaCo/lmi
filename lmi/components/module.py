from functools import lru_cache
from pathlib import Path
from types import ModuleType
import attr
import importlib.util

from gptos.tools.tool import PyObjectTool, Tool
from gptos.lmi.components.description import Description


@attr.s(auto_attribs=True, slots=True)
class Module(Description.variant(ModuleType)):

    __pyobj_tool: PyObjectTool

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        if self.name is None and hasattr(self.obj, "__name__"):
            self.name = self.obj.__name__
        self.__pyobj_tool = PyObjectTool(self.clazz)

    def loader(self, path: Path = None):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @property
    @lru_cache()
    def tools(self) -> list[Tool]:
        return [self.__pyobj_tool]
