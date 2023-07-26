from __future__ import annotations
from abc import ABC
from contextlib import contextmanager

from typing import Self

CONTEXT_MANAGED_STACK = []


class ContextManaged(ABC):
    def __new__(cls) -> Self:
        instance = cls.current() or super().__new__(cls)
        cls._push_to_current(instance)
        return instance

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

    @classmethod
    def current(cls) -> Self:
        # return first instance or subclass of cls in CONTEXT_MANAGED_STACK or else None
        for instance in reversed(CONTEXT_MANAGED_STACK):
            if isinstance(instance, cls):
                return instance
        else:
            return None

    @contextmanager
    def as_current(self) -> Self:
        self._push_to_current(self)
        yield self
        self._pop_from_current()

    @classmethod
    def _push_to_current(cls, instance: Self) -> None:
        CONTEXT_MANAGED_STACK.append(instance)

    @classmethod
    def _pop_from_current(cls) -> Self:
        return CONTEXT_MANAGED_STACK.pop()
