import attr

from gptos.lmi.handlers.mouse_event_handler import MouseEventHandler


class DragEventHandler(MouseEventHandler):
    @attr.s(auto_attribs=True)
    class DragEvent(MouseEventHandler.MouseEvent):
        obj: object

    def start_drag(self, event: DragEvent):
        """Triggered on X when X begins being draged."""
        pass

    def end_drag(self, event: DragEvent):
        """Triggered on X when X stops being draged."""
        pass
