import attr

from lmi.components.core.python.function import Function


@attr.s(auto_attribs=True)
class Select(Function):
    options: list[str]
