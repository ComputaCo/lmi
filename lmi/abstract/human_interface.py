from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from pydantic import UUID4


class HumanCanViewMixin(ABC):
    @abstractmethod
    def render_js(self) -> str:
        pass


@runtime_checkable
class Subscriber(Protocol):
    def __call__(self, topic: str, message: dict):
        pass


class HumanCanInteractWithMixin(ABC):
    @abstractmethod
    def subscribe_to_frontend(self, topic: str, subscriber: Subscriber):
        pass

    @abstractmethod
    def unsubscribe_from_frontend(self, topic: str, subscriber: Subscriber):
        pass
