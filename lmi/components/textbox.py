import attr
from gptos.lmi.components.scrollbox import Scrollbox
from gptos.lmi.components.text import Text
from gptos.lmi.handlers.keyboard_event_handler import KeyboardEventHandler


@attr.s(auto_attribs=True)
class TextBox(Scrollbox, KeyboardEventHandler):
    """Used for editing text that requires more than one-shot input. (For one shot input, use Input.)"""

    multiline = True
    cursor = "▮"
    cursor_location = (0, 0) # (horizontal, vertical)

    text: Text = attr.ib(init=False, default=attr.Factory(Text))

    def input(self, text):
        self.key_input(KeyboardEventHandler.KeyboardEvent(list(text)))

    def key_input(self, event: KeyboardEventHandler.KeyboardEvent):
        for key in event.keys:
            if key == "BACKSPACE":
                self.text = (
                    self.text[: self.cursor_location - 1]
                    + self.text[self.cursor_location :]
                )
                self.cursor_location -= 1
            elif key == "DELETE":
                self.text = (
                    self.text[: self.cursor_location]
                    + self.text[self.cursor_location + 1 :]
                )
            elif key == "RIGHT":
                self.cursor_location += 1
            elif key == "LEFT":
                self.cursor_location -= 1
            elif key == "HOME":
                self.cursor_location = 0
            elif key == "END":
                self.cursor_location = len(self.text)
            elif key == "ENTER":
                self.text = (
                    self.text[: self.cursor_location]
                    + "
        
        if DOWN_ARROW in event.keys:
            
        
        
        self.text = (
            self.text[: self.cursor_location]
            + event.key
            + self.text[self.cursor_location :]
        )

    def render(self, size) -> str:
        _content = self.text.copy()
        self.text = (
            self.text[: self.cursor_location]
            + self.cursor
            + self.text[self.cursor_location :]
        )
        rendering = super().render(size)
        self.text = _content
        return rendering

    @property
    def tools(self):
        return super().tools + [self.input]
