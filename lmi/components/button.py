from typing import Callable
from gptos.lmi.components.function import Function


class Button(Function):
    def __init__(self, on_click: Callable, title=None, name=None):
        super.__init__(fn=on_click, text=title, name=name or title)
        # these override the overrides in Function
        if title:
            self.text = title
