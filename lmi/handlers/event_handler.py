from abc import ABC
from typing import Literal

from pydantic import BaseModel

from lmi.components import Component


class Event(BaseModel):
    phase: Literal["capture", "handling", "bubbling"] = "handling"
    handled: bool = False
    target: Component

    def dispatch_event(event: Event, capture: bool = False):
        def fire_directly(self, target: Component):
            self.target = target
            ...

        # Capture phase
        if self.parent is not None:
            self.parent.dispatch_event(event, capture=True)

        # Handling phase
        if not event.cancel_bubble:
            handled = self.handle_event(event)

        # Bubbling phase
        if not event.cancel_bubble:
            for child in self.children:
                child.dispatch_event(event, capture=False)


class EventHandler(ABC):
    pass
