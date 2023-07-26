from enum import Enum
from pydantic import BaseModel
from lmi.components.Component import Component
from lmi.components.Stack import Stack
from lmi.components.Text import Text


class ProgressBar(Component):
    percentage: float

    class DisplayMode(Enum):
        BAR = "bar"
        TEXT = "text"
        BAR_AND_TEXT = BAR & TEXT

    display_mode = DisplayMode.BAR_AND_TEXT
    size: int = 10

    def render(self) -> str:
        if self.display_mode & ProgressBar.DisplayMode.TEXT:
            percent_complete_text = f"{self.progress:.1f}%"

        if self.display_mode & ProgressBar.DisplayMode.BAR:
            bar_size = self.size - len(percent_complete_text)
            Nbarpast = (self.percentage / 100) * bar_size
            Nbarfuture = bar_size - Nbarpast
            progress_bar = f'[{Nbarpast*"#"}{Nbarfuture*" "}]'

        content: str
        match self.display_mode:
            case ProgressBar.DisplayMode.BAR:
                content = progress_bar
            case ProgressBar.DisplayMode.TEXT:
                content = percent_complete_text
            case ProgressBar.DisplayMode.BAR_AND_TEXT:
                content = f"{progress_bar} {percent_complete_text}"
            case _:
                raise ValueError("Invalid display mode")

        return Text(text=content, size=self.size, selectable=False).render()
