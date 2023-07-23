from typing import Callable, Type

from lmi.components.form.text import Text


def normalize(component):
    """Converts python-native representations to structured component trees"""

    if isinstance(component, component):
        return component
    elif isinstance(component, (str, bool, int, float)):
        return Text(str(component))
    elif isinstance(component, (list, tuple, set)):
        return Stack(*component)
    elif inspect.is_class(component):
        return Class(component)
    elif inspect_mate.is_module(component)):
        return Module(component)
    elif isinstance(component, Callable):
        return Function(component)
    else:
        return Text(repr(component))
