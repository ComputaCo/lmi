import attr
from gptos.lmi.handlers.event_handler import EventHandler


class KeyboardEventHandler(EventHandler):
    @attr.s(auto_attribs=True)
    class KeyboardEvent(EventHandler.Event):
        keys: list[str] = attr.ib([])

        @property
        def key(self):
            if len(self.keys) == 0:
                return None
            return filter(lambda key: len(key) == 1, self.keys)[0]

    def key_input(self, event: KeyboardEvent):
        pass
