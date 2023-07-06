from enum import Enum, auto
import math
import attr
from abc import abstractmethod

import roman1

from gptos.lmi.misc.truncation import truncate
from gptos.lmi.components.component import Component
from gptos.lmi.components.flexbox import FlexBox


@attr.s(auto_attribs=True)
class NumberedList(Stack):
    class NumberingStyle(Enum):
        NUMBERS = auto()
        ROMAN_NUMERALS = auto()
        LOWERCASE_LETTERS = auto()
        CAPITAL_LETTERS = auto()

        @staticmethod
        def __iter__(self):
            if self is NumberedList.NumberingStyle.NUMBERS:
                return iter(iter(range(math.inf)))
            elif self is NumberedList.NumberingStyle.ROMAN_NUMERALS:
                return iter(map(roman.toRoman, range(math.inf)))
            elif self is NumberedList.NumberingStyle.LOWERCASE_LETTERS:

                def to_alpha(n):
                    if n < 26:
                        return chr(n + ord("a"))
                    else:
                        return to_alpha(n // 26 - 1) + to_alpha(n % 26)

                return iter(map(to_alpha, range(math.inf)))
            elif self is NumberedList.NumberingStyle.CAPITAL_LETTERS:

                def to_Alpha(n):
                    if n < 26:
                        return chr(n + ord("A"))
                    else:
                        return to_Alpha(n // 26 - 1) + to_Alpha(n % 26)

                return iter(map(to_Alpha, range(math.inf)))
            else:
                raise ValueError("Invalid NumberingStyle")

    format_string = r"{bullet}. {item}"
    numbering_style: NumberingStyle = NumberingStyle.NUMBERS

    def render(self, size) -> str:
        output = ""
        for bullet, child in zip(self.numbering_style, self.children):
            output += self.format_string.format(
                bullet=bullet, item=child.render(child.preferred_size)
            )
        return truncate(output, self.truncation_alignment, size)
