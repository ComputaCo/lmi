from typing import TypeVar
from lmi.components.AbstractToggleList import AbstractToggleList
from lmi.components.Checkbox import Checkbox
from lmi.components.Collection import Collection
from lmi.components.Component import Component
from pydantic import BaseModel

from lmi.components.Option import Option


T = TypeVar("T")


class OptionList(AbstractToggleList[T]):
    T_toggle = Option

    def _on_change(self, index: int, toggled: bool):
        if toggled:
            # select the component and unselect all other components
            for i, component in enumerate(self.toggle_components):
                if i == index:
                    component.toggle_true()
                else:
                    component.toggle_false()
        else:
            # unselect all components
            for component in self.toggle_components:
                component.toggle_false()
