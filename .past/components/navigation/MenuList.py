from lmi.components.basic.Button import Button
from lmi.components.Component import Component
from typing import List
from pydantic import BaseModel
from lmi.components.layout.Stack import Stack


class MenuList(Stack):
    menu_items: List[Component]

    open_menu_text: str = "Open Menu"
    close_menu_text: str = "Close Menu"

    selected = False
    on_select: callable = None

    @property
    def children(self) -> list[Component]:
        components = [
            Button(
                text=self.open_menu_text if not self.selected else self.close_menu_text,
                on_click=self.toggle_selected,
            )
        ]
        if self.selected:
            components.extend(self.menu_items)
        return components

    def toggle_selected(self):
        self.selected = not self.selected
        if self.on_select:
            self.on_select(self.selected)
