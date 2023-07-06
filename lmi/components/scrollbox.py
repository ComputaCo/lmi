from typing import Literal
import attr
from abc import abstractmethod
from gptos.lmi.components.button import Button

from gptos.lmi.components.component import Component
from gptos.lmi.components.text import Text
from gptos.lmi.handlers.scroll_event_handler import ScrollEventHandler
from gptos.lmi.misc.truncation import truncate
from gptos.lmi.utils import normalize
from gptos.tools.tool import Tool


@attr.s(auto_attribs=True)
class Scrollbox(Component):

    children: list[Component]
    position: int = 0
    separator: str = "\n"
    scroll_down_symbol: str = "▼"
    scroll_up_symbol: str = "▲"
    scroll_mode: Literal["block", "character"] = "block"
    shrink_to_fit: bool = False
    _scroll_down_button: Button
    _scroll_up_button: Button

    __rendered_components: list[Component] = attr.ib(init=False, default=[])

    @property
    def tools(self) -> list[Tool]:
        return sum([component.tools for component in self.components], [])

    @property
    def visible_components(self) -> list[Component]:
        return self.__rendered_components

    def __attrs_post_init__(self):
        self.children = [normalize(child) for child in self.children]
        self._scroll_down_button = Button(
            title=self.scroll_down_symbol,
            on_click=lambda: self.scroll(
                ScrollEventHandler.ScrollEvent(
                    ScrollEventHandler.ScrollDirection.DOWN,
                    speed=ScrollEventHandler.ScrollSpeed.SLOW,
                )
            ),
        )
        self._scroll_up_button = Button(
            title=self.scroll_up_symbol,
            on_click=lambda: self.scroll(
                ScrollEventHandler.ScrollEvent(
                    ScrollEventHandler.ScrollDirection.UP,
                    speed=ScrollEventHandler.ScrollSpeed.SLOW,
                )
            ),
        )

    def render(self, size) -> str:
        # determine which children are in the window
        if self.truncation_mode == "block":
            self.__rendered_components = self._components_in_window(
                start=self.position,
                end=self.position + size,
                include_partially_overlapping=False,
            )
            children = self.__rendered_components
        elif self.truncation_mode == "character":
            self.__rendered_components = self._components_in_window(
                start=self.position,
                end=self.position + size,
                include_partially_overlapping=True,
            )
            children = self.children  # since we'll be truncating the concat str later
        # maybe shrink to fit
        if self.shrink_to_fit:
            # decrease overall size to fit the children
            size = self._shrink_to_fit(size, children)
        # add separators to the children
        children_with_separators = list(self._interleave_separators(children))
        # render each child
        renderings = [
            child.render(child.preferred_size) for child in children_with_separators
        ]
        # concat the renderings
        output = "".join(renderings)
        # maybe character truncate the concat
        if self.truncation_mode == "character":
            output = truncate(
                output,
                alignment=self.truncation_alignment,
                size=size,
                trunc_symbol=self.trunc_symbol,
            )
        # return the concat
        return output

    def _components_in_window(self, start, end, include_partially_overlapping):
        char_idx = 0
        components = []
        for component in self.children:
            size = component.preferred_size
            if char_idx >= end:
                break
            if start <= char_idx and char_idx + size <= end:
                components.append(component)
            elif include_partially_overlapping and (
                start < char_idx + size or char_idx < end
            ):
                components.append(component)
            char_idx += size
        return components

    def _maybe_shrink_to_fit(self, size, children):
        if self.shrink_to_fit:
            # maybe decrease size to fit the children
            total_preferred_size = sum(
                [child.preferred_size + len(self.separator) for child in children]
            ) - len(self.separator)
            if total_preferred_size < size:
                # if the total max_size is less than the size, adjust our expected size to the total max_size
                size = total_preferred_size
        return size

    def _interleave_separators(self, children):
        seperator = Text(self.separator)
        for i, child in enumerate(children):
            yield child
            if i != len(children) - 1:
                yield seperator
