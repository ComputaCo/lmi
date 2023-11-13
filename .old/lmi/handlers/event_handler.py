from abc import ABC
from typing import Literal

from pydantic import BaseModel


class BaseEvent(BaseModel):
    """Base class for all events"""

    pass


class HandlerBaseEvent(BaseEvent):
    """Base class for all events when they actually reach the handler"""


class BaseEventHandler(ABC):
    """
    Defines the handler method for the event. Every implementation should define the following methods:

    * dispath_*: Dispatches the event to the corresponding handler, possibly using a shared peripheral variable to coordinate state across interactions. Composite components should wrap-override this method to determine which child to forward the dispatch to.
    * on_*: The actual handler method for the event. Usually supplied on instantiation. Instance variable.

    (Some interfaces make exception to this, eg, DisplayEventHandler)
    """
