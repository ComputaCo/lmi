import attr

from gptos.lmi.handlers.event_handler import EventHandler


class DisplayEventHandler(EventHandler):
    @attr.s(auto_attribs=True)
    class DisplayEvent(EventHandler.Event):
        pass

    def on_show(self, event: DisplayEvent):
        pass

    def on_hide(self, event: DisplayEvent):
        pass
