from enum import Enum
from typing_extensions import Literal
import attr

from gptos.lmi.handlers.event_handler import EventHandler
from gptos.lmi.handlers.mouse_event_handler import MouseEventHandler


class ClickEventHandler(MouseEventHandler):
    @attr.s(auto_attribs=True)
    class ClickEvent(MouseEventHandler.MouseEvent):
        class ClickType(Enum):
            SINGLE = "single"
            DOUBLE = "double"

        click_type: ClickType = ClickType.SINGLE

    def click(self, event: ClickEvent):
        pass
