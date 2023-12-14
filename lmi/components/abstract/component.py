from __future__ import annotations

from abc import ABC, abstractmethod
from langchain.tools import BaseTool

from pydantic import BaseModel, validator

# from reactpy.core.component import Component as reactpy_Component, component as reactpy_component

from lmi.utils.interfaces import (
    LLMCanInteractWithMixin,
    LLMCanViewMixin,
    RendersToReactPyMixin,
)
from lmi.handlers import DisplayEventHandler, EventHandler
from lmi.utils.misc import gen_unique_name


class Component(
    RendersToReactPyMixin,
    LLMCanInteractWithMixin,
    LLMCanViewMixin,
    BaseModel,
    ABC,
):
    name: str | None = None

    @validator("name")
    def check_name(cls, v):
        return v or gen_unique_name(cls.__name__)

    @property
    @abstractmethod
    def children(self) -> list[Component]:
        # declared as property rather than attr because we don't want it in the init
        pass

    def get_child_by_name(self, name: str) -> Component:
        for child in self.children:
            if child.name == name:
                return child
        raise ValueError(f"no child with name {name}")

    visible: bool = True
    disabled: bool = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def toggle_visibility(self):
        match self.visible:
            case True:
                self.hide()
            case False:
                self.show()

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def toggle_disabled(self):
        match self.disabled:
            case True:
                self.enable()
            case False:
                self.disable()

    focused_child: Component | None = None

    def focus_child(self, child: Component):
        self.focused_child = child

    def unfocus_child(self):
        self.focused_child = None

    def toggle_focus(self, child: Component):
        if self.focused_child == child:
            self.unfocus()
        else:
            self.focus(child)

    def shift_focus(self, direction: int = 1):
        if not self.children:
            return
        if self.focused_child is None:
            self.focus_child(self.children[0])
        else:
            idx = self.children.index(self.focused_child)
            self.focus_child(self.children[(idx + direction) % len(self.children)])

    @property
    def llm_tools(self) -> list[BaseTool]:
        tools = []

        # add event-handler specific tools
        for T_event_handler in EventHandler.__subclasses__():
            components_that_handle_T = [
                component
                for component in self.children
                if isinstance(component, T_event_handler)
            ]
            if components_that_handle_T:
                tools.extend(
                    T_event_handler.llm_tools_from_handlers(
                        handlers=components_that_handle_T
                    )
                )

        return tools
