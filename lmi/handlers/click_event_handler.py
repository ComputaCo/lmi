from abc import ABC
from enum import Enum
from typing_extensions import Literal

from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.mouse_event_handler import BaseMouseEventHandler


class ClickEventHandler(BaseMouseEventHandler, LLMCanInteractWithMixin, ABC):
    class ClickEvent(BaseMouseEventHandler.MouseEvent):
        class ClickType(Enum):
            SINGLE = "single"
            DOUBLE = "double"

        click_type: ClickType = ClickType.SINGLE

    def on_click(self, event: ClickEvent):
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

    def on_single_left_click(self, event: ClickEvent):
        pass

    def on_double_left_click(self, event: ClickEvent):
        pass

    def on_single_middle_click(self, event: ClickEvent):
        pass

    def on_double_middle_click(self, event: ClickEvent):
        pass

    def on_single_right_click(self, event: ClickEvent):
        pass

    def on_double_right_click(self, event: ClickEvent):
        pass
