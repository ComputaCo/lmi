from typing import Callable

from lmi.components.abstract.component import Component
from lmi.utils.misc import PASS


class Button(Component):
    on_click: Callable[[], None] = PASS