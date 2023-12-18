from lmi.components.abstract.component import Component


class Stack(Component):
    items: list[Component] = []

    @property
    def children(self) -> list[Component]:
        return self.items

    @children.setter
    def children(self, value: list[Component]):
        self.items = value
