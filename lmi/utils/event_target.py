from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel


T_TARGET = TypeVar("T_TARGET", bound="EventTarget")


class Event(Generic[T_TARGET], BaseModel):
    target: T_TARGET

    @abstractmethod
    def apply(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class HasEvents(Generic[T_TARGET], BaseModel, ABC):
    event_idx: int = 0
    events: list[Event[T_TARGET]] = []

    def do(self, event: Event[T_TARGET]):
        self.events = self.events[: self.event_idx] + [event]
        self.event_idx += 1

    def undo(self):
        self.events[self.event_idx - 1].undo()
        self.event_idx -= 1

    def redo(self):
        self.events[self.event_idx].apply()
        self.event_idx += 1


class EventTarget(Generic[T_TARGET], HasEvents[T_TARGET], ABC):
    pass


class CompositeEvent(Generic[T_TARGET], Event[T_TARGET], HasEvents[T_TARGET]):
    def apply(self):
        for event in self.events:
            event.apply()

    def undo(self):
        for event in reversed(self.events):
            event.undo()
