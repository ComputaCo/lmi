from abc import ABC
from enum import Enum
from typing import Callable
from typing_extensions import Literal
from lmi.abstract.llm_interface import LLMCanInteractWithMixin

from lmi.handlers.mouse_event_handler import BaseMouseEventHandler, MouseEvent


class ClickEvent(MouseEvent):
    class ClickType(Enum):
        SINGLE = "single"
        DOUBLE = "double"

    click_type: ClickType = ClickType.SINGLE


class ClickEventHandler(BaseMouseEventHandler, LLMCanInteractWithMixin, ABC):
    mouse: Mouse

    def dispatch_click(self):
        """Dispatches a click event to the current mouse position."""
        pass

    def default_on_click(self, event: ClickEvent):
        match event.button, event.click_type:
            case ClickEventHandler.ClickEvent.Buttons.LEFT, ClickEventHandler.ClickEvent.ClickType.SINGLE:
                self.on_single_left_click(event)
            case ClickEventHandler.ClickEvent.Buttons.LEFT, ClickEventHandler.ClickEvent.ClickType.DOUBLE:
                self.on_double_left_click(event)
            case ClickEventHandler.ClickEvent.Buttons.MIDDLE, ClickEventHandler.ClickEvent.ClickType.SINGLE:
                self.on_single_middle_click(event)
            case ClickEventHandler.ClickEvent.Buttons.MIDDLE, ClickEventHandler.ClickEvent.ClickType.DOUBLE:
                self.on_double_middle_click(event)
            case ClickEventHandler.ClickEvent.Buttons.RIGHT, ClickEventHandler.ClickEvent.ClickType.SINGLE:
                self.on_single_right_click(event)
            case ClickEventHandler.ClickEvent.Buttons.RIGHT, ClickEventHandler.ClickEvent.ClickType.DOUBLE:
                self.on_double_right_click(event)

    on_click = default_on_click
    on_single_left_click: Callable[[ClickEvent], None]
    on_double_left_click: Callable[[ClickEvent], None]
    on_single_middle_click: Callable[[ClickEvent], None]
    on_double_middle_click: Callable[[ClickEvent], None]
    on_single_right_click: Callable[[ClickEvent], None]
    on_double_right_click: Callable[[ClickEvent], None]
