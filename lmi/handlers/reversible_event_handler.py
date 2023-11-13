from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

from lmi.handlers.event_handler import BaseEvent, BaseEventHandler


T_TARGET = TypeVar("T_TARGET", bound="ReversibleEventHandler")


class HasEvents(Generic[T_TARGET], BaseModel, ABC):
    event_idx: int = 0
    events: list[ReversibleEventHandler.ReversibleEvent[T_TARGET]] = []

    def do(self, event: ReversibleEventHandler.ReversibleEvent[T_TARGET]):
        self.events = self.events[: self.event_idx] + [event]
        self.event_idx += 1

    def undo(self):
        self.events[self.event_idx - 1].reverse()
        self.event_idx -= 1

    def redo(self):
        self.events[self.event_idx].apply()
        self.event_idx += 1


class ReversibleEvent(Generic[T_TARGET], BaseEvent):
    target: T_TARGET

    @abstractmethod
    def apply(self):
        pass

    @abstractmethod
    def reverse(self):
        pass


class CompositeReversibleEvent(
    Generic[T_TARGET], ReversibleEvent[T_TARGET], HasEvents[T_TARGET]
):
    def apply(self):
        for event in self.events:
            event.apply()

    def reverse(self):
        for event in reversed(self.events):
            event.reverse()


class ReversibleEventHandler(
    Generic[T_TARGET], HasEvents[T_TARGET], BaseEventHandler, ABC
):
    event_idx: int = 0
    events: list[ReversibleEvent[T_TARGET]] = []

    def do(self, event: ReversibleEvent[T_TARGET]):
        self.events = self.events[: self.event_idx] + [event]
        self.event_idx += 1

    def undo(self):
        self.events[self.event_idx - 1].reverse()
        self.event_idx -= 1

    def redo(self):
        self.events[self.event_idx].apply()
        self.event_idx += 1
