from __future__ import annotations

from typing import Callable, Self, Type, TypeVar, Union

from langchain.tools.base import BaseTool

from lmi.components.abstract.component import Component

from langchain.tools.base import BaseTool

from lmi.components.abstract.component import Component


class EventHandler(Component):
    @classmethod
    def llm_tools_from_handlers(cls, handlers: list[Self]) -> list[BaseTool]:
        return []


class MouseEventHandler(EventHandler):
    pass


class ClickEventHandler(MouseEventHandler):
    on_click: Callable[[], None]

    @classmethod
    def llm_tools_from_handlers(cls, handlers: list[Self]) -> BaseTool:
        def click(name):
            component = cls.get_child_by_name(handlers, name)
            component.on_click()

        return BaseTool(
            name="click",
            description="clicks the component",
            args=["name"],
            func=click,
        )


# Not sure what the use case is for this:
# class HoverEventHandler(EventHandler):
#     on_hover: Callable[[], None]
#     on_mouse_enter: Callable[[], None]
#     on_mouse_leave: Callable[[], None]


class KeyboardEventHandler(EventHandler):
    on_input: Callable[[str], None]

    @classmethod
    def llm_tools_from_handlers(cls, handlers: list[Self]) -> BaseTool:
        def type(name):
            component = cls.get_child_by_name(handlers, name)
            component.on_input()

        return BaseTool(
            name="click",
            description="clicks the component",
            args=["name"],
            func=type,
        )


class KeypressEventHandler(EventHandler):
    on_key_press: Callable[[str], None]
    on_key_release: Callable[[str], None]

    @classmethod
    def llm_tools_from_handlers(cls, handlers: list[Self]) -> list[BaseTool]:
        return []


class ScrollEventHandler(EventHandler):
    # even though scroll is usually implement via a mouse, this needn't be the case
    on_scroll: Callable[[int], None]

    @classmethod
    def llm_tools_from_handlers(cls, handlers: list[Self]) -> list[BaseTool]:
        return []
