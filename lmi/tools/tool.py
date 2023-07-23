from functools import wraps
from typing import Callable
import attr

import tensorcode as tc


@attr.s(auto_attribs=True, slots=True)
class Tool:

    name: str
    description: str
    fn: Callable[[str], str]

    @property
    def short_description(self):
        return self.description.split("\n")[0]

    def __call__(self, input: str) -> str:
        return self.fn(input)

    @staticmethod
    def wrap(fn):
        # check if fn is already a tool
        if isinstance(fn, Tool):
            return fn

        return Tool(
            name=fn.__name__,
            description=fn.__doc__
            if hasattr(fn, "__doc__") and len(fn.__doc__) > 0
            else tc.text.description(fn),
            fn=tc.text.smart_signature(fn),
        )
