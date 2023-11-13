from abc import abstractmethod
from typing import Generic, List, Callable, TypeVar
from lmi.components.layout.Stack import Stack
from pydantic import BaseModel
from lmi.components.Component import Component

T = TypeVar("T")


class Collection(Generic[T], Stack):
    data: list[T]

    @abstractmethod
    def item_generator(self, index: int, datum: T) -> Component:
        pass

    @property
    def children(self):
        return [
            self.item_generator(index, datum) for index, datum in enumerate(self.data)
        ]
