from typing import Literal, TypeVar
from pydantic import BaseModel
from lmi.components.Collection import Collection
from lmi.components.Component import Component
from lmi.components.Stack import Stack
from lmi.components.Text import Text


T = TypeVar("T")


class UnorderedList(Collection[T]):
    def item_generator(self, index: int, datum: T) -> Component:
        return Text(text=f"- {datum}")
