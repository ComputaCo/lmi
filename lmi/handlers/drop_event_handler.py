import attr

from gptos.lmi.handlers.mouse_event_handler import MouseEventHandler


class DropEventHandler(MouseEventHandler):
    @attr.s(auto_attribs=True)
    class DropEvent(MouseEventHandler.MouseEvent):
        obj: object

    def drop(self, event: DropEvent):
        """Triggered on Y when obj is dropped on Y."""
        pass
