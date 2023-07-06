from typing import Callable, Type
from gptos.lmi.components.component import Component
from gptos.lmi.components.stack import Stack
from gptos.lmi.components.text import Text


def normalize(Component):
    if isinstance(Component, Component):
        return Component
    elif isinstance(Component, (str, bool, int, float)):
        return Text(str(Component))
    elif isinstance(Component, (list, tuple, set)):
        return Stack(*Component)
    elif isinstance(Component, Callable):
        return Function(Component)
    elif isinstance(Component, Type):
        return Class(Component)
    elif isinstance(Component, module):
        return Module(Component)
    else:
        return Text(repr(Component))
