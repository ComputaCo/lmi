from typing import Literal, TypeVar
from pydantic import BaseModel
from lmi.components.layout.Collection import Collection
from lmi.components.Component import Component
from lmi.components.layout.Stack import Stack
from lmi.components.basic.Text import Text


T = TypeVar("T")


class UnorderedList(Collection[T]):
    def item_generator(self, index: int, datum: T) -> Component:
        return Text(text=f"- {datum}")
