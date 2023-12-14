from lmi.components.Component import Component


class Spinner(Component):
    active = False
    frame_index = 0

    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def llm_render(self) -> str:
        if self.active:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            return self.frames[self.frame_index]
        return " "

    def start(self):
        self.active = True

    def stop(self):
        self.active = False
        self.frame_index = 0
