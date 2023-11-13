from typing import Callable


class Button(Function):
    def __init__(self, title: str, on_click: Callable):
        super.__init__(name=title, fn=on_click)
