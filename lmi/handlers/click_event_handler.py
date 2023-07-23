from enum import Enum
from typing_extensions import Literal
import attr

from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.handlers.mouse_event_handler import MouseEventHandler


class ClickEventHandler(MouseEventHandler, LLMCanInteractWithMixin):
    @attr.s(auto_attribs=True)
    class ClickEvent(MouseEventHandler.MouseEvent):
        class ClickType(Enum):
            SINGLE = "single"
            DOUBLE = "double"

        click_type: ClickType = ClickType.SINGLE

    def on_click(self, event: ClickEvent):
        pass

    @property
    def on_click_tool(self) -> [BaseTool]:
        return ...

    @property
    def tools(self) -> list:
        return super().tools + [self.on_click_tool]
