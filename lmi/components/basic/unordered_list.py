from enum import Enum, auto
import math
import attr
from abc import abstractmethod
from lmi.components.layout.flexbox import Flexbox

import roman


@attr.s(auto_attribs=True)
class UnorderedList(Flexbox):

    # FIXME: merge this with ordered_list.py

    bullet = "- "
    format_string = r"{bullet}{item}\n"

    def render(self, size) -> str:
        output = ""
        for bullet, child in zip(self.numbering_style, self.children):
            output += self.format_string.format(
                bullet=bullet, item=child.render(child.preferred_size)
            )
        return super()._render_text(output, size)
