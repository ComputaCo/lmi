import attr

from gptos.lmi.handlers.event_handler import EventHandler


class FocusEventHandler(EventHandler):
    @attr.s(auto_attribs=True)
    class FocusEvent(EventHandler.Event):
        pass

    def on_focus(self, event: FocusEvent):
        pass

    def on_unfocus(self, event: FocusEvent):
        pass
