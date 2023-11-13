from abc import ABC
from typing import Type


class HasUniqueNameMixin(ABC):
    name: str
    __COMPONENT_NAMES: dict[Type, set[str]] = {}

    def __init__(self):
        if not self.name:
            self.name = self.generate_name()
        elif self.name in self._CLASS_COMPONENT_NAMES:
            self.name = self.generate_name()
        self._CLASS_COMPONENT_NAMES.append(self.name)

    @property
    @classmethod
    def _CLASS_COMPONENT_NAMES(cls) -> set[str]:
        if cls not in HasUniqueNameMixin.__COMPONENT_NAMES:
            HasUniqueNameMixin.__COMPONENT_NAMES[cls] = []
        return HasUniqueNameMixin.__COMPONENT_NAMES[cls]

    @classmethod
    def generate_name(cls):
        for i in range(1, 1_000_000_000):
            name = f"{cls.__name__}{i}"
            if name not in cls._CLASS_COMPONENT_NAMES:
                return name
        else:
            raise Exception("You need to assign a custom name to this instance")
