from typing import TypeVar
from lmi.components.core.AbstractToggleList import AbstractToggleList
from lmi.components.core.Checkbox import Checkbox
from lmi.components.layout.Collection import Collection
from lmi.components.Component import Component
from pydantic import BaseModel

from lmi.components.core.Option import Option


T = TypeVar("T")


class CheckList(AbstractToggleList[T]):
    T_toggle = Checkbox

    def _on_change(self, index: int, toggled: bool):
        if toggled:
            # select the component
            self.toggle_components[index].toggle_true()
        else:
            # unselect the component
            self.toggle_components[index].toggle_false()
