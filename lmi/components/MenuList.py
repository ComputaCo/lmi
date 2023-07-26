from lmi.components.Button import Button
from lmi.components.Component import Component
from typing import List
from pydantic import BaseModel
from lmi.components.Stack import Stack


class MenuList(Stack):
    menu_items: List[Component]

    text: str

    selected = False

    @property
    def components(self) -> list[Component]:
        components = [Button(text=self.text, on_click=self.toggle_selected)]
        if self.selected:
            components.extend(self.menu_items)
        return components

    def toggle_selected(self):
        self.selected = not self.selected
