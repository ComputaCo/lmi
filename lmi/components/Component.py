from __future__ import annotations

from abc import abstractmethod
from typing import Any, Generator
from langchain.schema import BaseMessage
from pydantic import BaseModel

from lmi.abstract.interactable import LLMCanInteractWithMixin
from lmi.abstract.viewable import LLMCanViewMixin
from langchain.tools import BaseTool
from lmi.handlers.advanced_keyboard_event_handler import AdvancedKeyboardEventHandler
from lmi.handlers.click_event_handler import ClickEventHandler

from lmi.handlers.display_event_handler import DisplayEventHandler
from lmi.handlers.drag_event_handler import DragEventHandler
from lmi.handlers.drop_event_handler import DropEventHandler
from lmi.handlers.event_handler import EventHandler
from lmi.handlers.focus_event_handler import FocusEventHandler
from lmi.handlers.hover_event_handler import HoverEventHandler
from lmi.handlers.keyboard_event_handler import KeyboardEventHandler
from lmi.handlers.mouse_event_handler import BaseMouseEventHandler
from lmi.handlers.scroll_event_handler import ScrollEventHandler
from lmi.utils.json_serializable import JSONSerializable
from lmi.utils.name_generator import HasUniqueNameMixin


class Component(
    DisplayEventHandler,
    LLMCanInteractWithMixin,
    LLMCanViewMixin,
    HasUniqueNameMixin,
    JSONSerializable,
    BaseModel,
):
    size: int = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_init()

    def post_init(self):
        pass

    @property
    def components(self) -> list[Component]:
        return []

    @property
    def visible_components(self) -> list[Component]:
        return self.components

    def render(self) -> str:
        return "\n".join([component.render() for component in self.visible_components])

    def render_messages(self) -> Generator[BaseMessage, None, None]:
        for component in self.visible_components:
            yield from component.render_messages()

    @property
    def tools(self) -> list[BaseTool]:
        return [tool for component in self.components for tool in component.tools]

    # def __instancecheck__(self, instance: Any) -> bool:
    #     for component in self.components:
    #         for event_handler in component.event_handlers:
    #             if issubclass(instance, EventHandler):
    #                 return True

    # ScrollEventHandler,
    # DragEventHandler,
    # DropEventHandler,
    # HoverEventHandler,
    # ClickEventHandler,
    # BaseMouseEventHandler,
    # AdvancedKeyboardEventHandler,
    # KeyboardEventHandler,
    # FocusEventHandler,
    # DisplayEventHandler,
    # EventHandler,


"""        
SO, instead of subclassing event handlers, I should just make a handle method that recieves Event objects and does something with them.
Events may also be undo-able, so this unifies text editing events with GUI-like events.

I may find a framework that does this, but I doubt it. I think I'm going to have to make it myself.

"""
