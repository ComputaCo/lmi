from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Annotated, Callable, ClassVar, Literal, Self, Type, TypeVar, Union

from langchain.tools.base import BaseTool, tool, Tool
from pydantic import BaseModel, BeforeValidator, Field

from lmi.components.abstract.component import Component


class EventHandler(ABC):

    ACTION_VERB: ClassVar[str] = "generic"

    class EventArgs(BaseModel, ABC):
        pass

    @classmethod
    def lc_tool(cls, root: Component) -> BaseTool:
        return Tool.from_function(
            name=f"{cls.ACTION_VERB}",
            description=f"Dispatches {cls.ACTION_VERB} events",
            args_schema=cls,
            function=cls.make_dispatcher(root),
        )

    @abstractmethod
    @classmethod
    def make_dispatcher(cls, root: Component):
        pass


class MouseEventHandler(EventHandler):

    ACTION_VERB: ClassVar[str] = "mouse"

    class MouseEventArgs(EventHandler.EventArgs, ABC):
        pass

    pass


class ClickEventHandler(MouseEventHandler):

    ACTION_VERB: ClassVar[str] = "click"

    on_click: Callable[[OnClickArgs], None]

    class OnClickArgs(MouseEventHandler.MouseEventArgs):
        component_name: str = Field(description="The name of the component to click")

    @classmethod
    def make_dispatcher(cls, root: Component):
        def dispatch(args: cls.OnClickArgs):
            nonlocal root
            receiver = root.get_child_by_name_recursive(args.component_name)
            if not isinstance(receiver, cls):
                raise TypeError(f"component {receiver} cannot handle click events")
            receiver.on_click()

        return dispatch


class AdvancedClickEventHandler(MouseEventHandler):

    ACTION_VERB: ClassVar[str] = "click"

    on_double_click: Callable[[AdvancedOnClickArgs], None]
    on_right_click: Callable[[AdvancedOnClickArgs], None]

    class AdvancedOnClickArgs(ClickEventHandler.OnClickArgs):
        click_type: Literal["single-click", "double-click", "right-click"] = Field(
            "single-click", description="The type of click to perform"
        )

    @classmethod
    def make_dispatcher(cls, root: Component):
        def dispatch(args: cls.AdvancedOnClickArgs):
            nonlocal root
            receiver = root.get_child_by_name_recursive(args.component_name)
            if not isinstance(receiver, cls):
                raise TypeError(f"component {receiver} cannot handle click events")
            receiver.get_focus()
            match args.click_type.strip().lower():
                case "single-click", "single":
                    receiver.on_click()
                case "double-click", "double":
                    receiver.on_double_click()
                case "right-click", "right":
                    receiver.on_right_click()
                case _:
                    raise ValueError(f"click type {args.click_type} not supported")

        return dispatch


class HoverEventHandler(MouseEventHandler):

    ACTION_VERB: ClassVar[str] = "hover"

    on_hover: Callable[[OnHoverArgs], None]
    on_mouse_enter: Callable[[OnHoverArgs], None]
    on_mouse_leave: Callable[[OnHoverArgs], None]

    class OnHoverArgs(MouseEventHandler.MouseEventArgs):
        component_name: str = Field(
            description="The name of the component to hover over"
        )

    @classmethod
    def make_dispatcher(cls, root: Component):
        def dispatch(args: cls.OnHoverArgs):
            nonlocal root
            receiver = root.get_child_by_name_recursive(args.component_name)
            if not isinstance(receiver, cls):
                raise TypeError(f"component {receiver} cannot handle hover events")
            # receiver.get_focus() # FIXME: should we get focus here?
            receiver.on_hover()

        return dispatch


class ScrollEventHandler(MouseEventHandler):

    ACTION_VERB: ClassVar[str] = "scroll"

    on_scroll: Callable[[OnScrollArgs], None]

    class OnScrollArgs(MouseEventHandler.MouseEventArgs):
        component_name: str = Field(description="The name of the component to scroll")
        amount: int = Field(
            description="The amount to scroll. Positive for up, negative for down"
        )

    @classmethod
    def make_dispatcher(cls, root: Component):
        def dispatch(args: cls.OnScrollArgs):
            nonlocal root
            receiver = root.get_child_by_name_recursive(args.component_name)
            if not isinstance(receiver, cls):
                raise TypeError(f"component {receiver} cannot handle scroll events")
            # receiver.get_focus() # should we get focus here?
            receiver.on_scroll(args.amount)

        return dispatch


class KeyboardEventHandler(EventHandler):

    ACTION_VERB: ClassVar[str] = "keyboard"

    class KeyboardEventArgs(EventHandler.EventArgs, ABC):
        pass


class KeyboardInputEventHandler(KeyboardEventHandler):

    ACTION_VERB: ClassVar[str] = "keyboard-input"

    on_keyboard_input: Callable[[OnKeyboardInputArgs], None]

    class OnKeyboardInputArgs(KeyboardEventHandler.KeyboardEventArgs):
        component_name: str = Field(
            description="The name of the component to input text into"
        )
        text: str = Field(description="The text to input")

    @classmethod
    def make_dispatcher(cls, root: Component):
        def dispatch(args: cls.OnKeyboardInputArgs):
            nonlocal root
            receiver = root.get_child_by_name_recursive(args.component_name)
            if not isinstance(receiver, cls):
                raise TypeError(
                    f"component {receiver} cannot handle keyboard input events"
                )
            # receiver.get_focus() # should we get focus here?
            receiver.on_keyboard_input(args.text)

        return dispatch


class KeypressEventHandler(EventHandler):

    ACTION_VERB: ClassVar[str] = "keypress"

    on_key_press: Callable[[OnKeypressArgs], None]
    on_key_release: Callable[[OnKeypressArgs], None]

    keys = (
        [chr(i) for i in range(ord("a"), ord("z") + 1)]
        + [chr(i) for i in range(ord("0"), ord("9") + 1)]
        + [
            "space",
            "enter",
            "backspace",
            "tab",
            "escape",
            "up",
            "down",
            "left",
            "right",
            "ctrl",
            "home",
            "end",
            "pageup",
            "pagedown",
            "insert",
            "delete",
            "f1",
            "f2",
            "f3",
            "f4",
            "f5",
            "f6",
            "f7",
            "f8",
            "f9",
        ]
    )

    class OnKeypressArgs(KeyboardEventHandler.KeyboardEventArgs):
        def check_key_valid(value):
            if value not in KeypressEventHandler.keys:
                raise ValueError(f"{value} is not a valid key")
            return value

        component_name: str = Field(
            description="The name of the component to press the key in"
        )
        key: Annotated[str, BeforeValidator(check_key_valid)] = Field(
            description="The key to press"
        )

    @classmethod
    def make_dispatcher(cls, root: Component):
        def dispatch(args: cls.OnKeypressArgs):
            nonlocal root
            receiver = root.get_child_by_name_recursive(args.component_name)
            if not isinstance(receiver, cls):
                raise TypeError(f"component {receiver} cannot handle keypress events")
            # receiver.get_focus() # should we get focus here?
            receiver.on_key_press(args.key)

        return dispatch
