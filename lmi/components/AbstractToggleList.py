from abc import abstractmethod
from typing import Generic, TypeVar
from lmi.components.AbstractToggle import AbstractToggle
from lmi.components.Checkbox import Checkbox
from lmi.components.Collection import Collection
from lmi.components.Component import Component
from pydantic import BaseModel

from lmi.components.Option import Option


T = TypeVar("T")


class AbstractToggleList(Generic[T], Collection[tuple[str, T]]):
    T_toggle: type[AbstractToggle]

    def item_generator(self, index: int, datum: T) -> Component:
        return self.T_toggle(
            text=str(datum),
            toggled=index == self.selected,
            on_change=lambda toggled: self.on_change(index, toggled),
        )

    @property
    def toggle_components(self) -> list[Option]:
        return [
            component
            for component in self.components
            if isinstance(component, AbstractToggle)
        ]

    @property
    def elem_titles(self) -> list[str]:
        return [text for text, _ in self.data]

    @property
    def elem_states(self) -> list[T]:
        return [state for _, state in self.data]

    def on_change(self, index: int, toggled: bool):
        self.data[index][1] = toggled
        self._on_change(index, toggled)

    @abstractmethod
    def _on_change(self, index: int, toggled: bool):
        pass
