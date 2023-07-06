import itertools
from typing import Literal
import attr
from gptos.lmi.components.text import Text
from gptos.tools.tool import Tool
from gptos.lmi.components.component import Component
from gptos.lmi.misc.alignment import Alignment
from gptos.lmi.misc.truncation import TRUNC_SYMBOL, truncate
from gptos.lmi.utils import normalize


@attr.s(auto_attribs=True)
class Flexbox(Component):
    children: list[Component] = []
    separator: str = "\n"
    trunc_symbol: str = TRUNC_SYMBOL
    truncation_alignment: Alignment = Alignment.LEFT
    truncation_mode: Literal["block", "character"] = "block"
    shrink_to_fit: bool = False

    __rendered_components: list[Component] = attr.ib(init=False, default=[])

    @property
    def tools(self) -> list[Tool]:
        return sum([component.tools for component in self.components], [])

    @property
    def visible_components(self) -> list[Component]:
        return (
            self.__rendered_components
            if len(self.__rendered_components) != 0
            else self.children
        )

    @property
    def preferred_size(self) -> int:
        return sum(
            child.preferred_size for child in self._interleave_separators(self.children)
        )

    @property
    def flex_factor(self) -> float:
        return (
            sum(
                child.flex_factor * child.preferred_size
                for child in self._interleave_separators(self.children)
            )
            / self.preferred_size
        )

    @property
    def max_size(self) -> int:
        return sum(child.max_size for child in self._interleave_separators(self.children))

    @property
    def min_size(self) -> int:
        return sum(child.min_size for child in self._interleave_separators(self.children))

    def __attrs_post_init__(self):
        self.children = [normalize(child) for child in self.children]

    def render(self, size) -> str:
        children = self.children.copy()
        # maybe block truncate children
        if self.truncation_mode == "block":
            children = self._block_truncate(size, children)
        self.__rendered_components = children
        # maybe shrink to fit
        if self.shrink_to_fit:
            # decrease overall size to fit the children
            size = self._shrink_to_fit(size, children)
        # add separators to the children
        children_with_separators = list(self._interleave_separators(children))
        # now its time to render children to fit the size
        child_sizes = self._determine_child_sizes(size, children_with_separators)
        # render each child
        renderings = [
            child.render(size)
            for child, size in zip(children_with_separators, child_sizes)
        ]
        # concat the renderings
        concat = "".join(renderings)
        # maybe character truncate the concat
        if self.truncation_mode == "character":
            concat = truncate(
                concat,
                alignment=self.truncation_alignment,
                size=size,
                trunc_symbol=self.trunc_symbol,
            )
        # return the concat
        return concat

    def _block_truncate(self, size, children):
        # remove children until the total min_size is less than the size

        # place this component where the truncation occurs
        trunc_component = Text(self.trunc_symbol)

        def total_min_size():
            return sum(
                [child.min_size + len(self.separator) for child in children]
            ) - len(self.separator)

        if self.truncation_alignment == Alignment.LEFT:
            # remove children from the left until the total min_size is less than the size
            while total_min_size() > size:
                # temporarily remove the truncation symbol
                children.remove(trunc_component)
                # remove the first child
                children.pop(0)
                # add the truncation symbol to the left
                children.insert(0, trunc_component)

        elif self.truncation_alignment == Alignment.RIGHT:
            # remove children from the right until the total min_size is less than the size
            while total_min_size() > size:
                # temporarily remove the truncation symbol
                children.remove(trunc_component)
                # remove the last child
                children.pop(-1)
                # make the truncation symbol be on the right
                children.append(trunc_component)

        elif self.truncation_alignment == Alignment.CENTER:
            # remove children from the center until the total min_size is less than the size
            while total_size := total_min_size() > size:
                # temporarily remove the truncation symbol
                children.remove(trunc_component)
                # remove the middle child
                middle_index = total_size // 2
                index = 0
                for i, child in enumerate(children):
                    index += child.min_size + len(self.separator)
                    if index >= middle_index:
                        # remove the middle child
                        children.pop(i)
                        # insert the truncation symbol in the middle
                        children.insert(i, trunc_component)
                        break

        else:
            raise ValueError(f"Invalid truncation alignment: {self.truncation_alignment}")

        return children

    def _shrink_to_fit(self, size, children):

        # maybe decrease size to fit the children
        total_max_size = sum(
            [child.max_size + len(self.separator) for child in children]
        ) - len(self.separator)
        if total_max_size < size:
            # if the total max_size is less than the size, adjust our expected size to the total max_size
            size = total_max_size

        return size

    def _interleave_separators(self, children):
        seperator = Text(self.separator)
        for i, child in enumerate(children):
            yield child
            if i != len(children) - 1:
                yield seperator

    def _determine_child_sizes(
        total_size_target: int, components: list[Component]
    ) -> list[int]:
        total_preferred_size = sum(resizable.preferred_size for resizable in components)
        total_flex_factor = sum(resizable.flex_factor for resizable in components)

        remaining_size = total_size_target - total_preferred_size

        if remaining_size < 0:
            raise ValueError(
                "Total preferred size of Resizables is greater than total_size."
            )

        # handle 0 flex cases
        if total_flex_factor == 0:
            # no flex, return preferred_size's
            return [component.preferred_size for component in components]

        sizes = []
        for component in components:
            size_share = remaining_size * (component.flex_factor / total_flex_factor)
            size = component.preferred_size + size_share
            sizes.append(round(size))

        # Ensure the sum of actual sizes equals total_size, rounding errors might cause a difference
        size_difference = sum(sizes) - total_size_target
        if size_difference > 0:
            # find most flexible component and reduce its size
            most_flexible_index = max(
                range(len(components)), key=lambda i: components[i].flex_factor
            )
            sizes[most_flexible_index] -= size_difference

        return sizes
