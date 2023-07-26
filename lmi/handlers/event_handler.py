from abc import ABC

from pydantic import BaseModel


class EventHandler(ABC):
    class Event(BaseModel):
        pass
