from abc import ABC

import attr


class EventHandler(ABC):
    @attr.s(auto_attribs=True)
    class Event:
        pass
