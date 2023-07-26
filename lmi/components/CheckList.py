from typing import TypeVar
from lmi.components.AbstractToggleList import AbstractToggleList
from lmi.components.Checkbox import Checkbox
from lmi.components.Collection import Collection
from lmi.components.Component import Component
from pydantic import BaseModel

from lmi.components.Option import Option


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
