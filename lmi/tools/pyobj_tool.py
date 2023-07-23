from typing import Callable
from gptos.tools.tool import Tool
from gptos.tools.toolbox import Toolbox


class PyObjectTool(Toolbox):
    """Extracts all callable attributes from an object / class / module, wraps them with smart_signature wrappers if needed, and puts them in a toolbox."""

    obj: object

    def __init__(self, obj, **kwargs):
        tools = []
        for attr in dir(obj):
            if isinstance(getattr(obj, attr), Callable):
                tool = getattr(obj, attr)
                if isinstance(tool, Tool):
                    tools.append(tool)
                else:
                    tools.append(Tool.wrap(tool))
        generated_kwargs = dict(
            name=obj.__name__ if hasattr(obj, "__name__") else obj.__class__.__name__,
            description=obj.__doc__,
            tools=tools + kwargs.get("tools", []),
        )
        del kwargs["tools"]
        super().__init__(**generated_kwargs, **kwargs)
