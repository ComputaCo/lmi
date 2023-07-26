import attr
from abc import abstractmethod

from lmi.components.abstract.component import Component
from lmi.components.layout.scrollbox import ScrollView
from lmi.consts.alignment import Alignment
from lmi.consts.truncation import truncate


@attr.s(auto_attribs=True)
class Text(Component):
    text: str
    scrollable = False
    truncation_alignment: Alignment = Alignment.LEFT

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        if self.scrollable:
            self._scrolled_text = Text(name=self.name, text=self.text)
            self._scrollview = ScrollView(child=self._scrolled_text)

    @property
    def preferred_size(self) -> int:
        return len(self.text)

    @abstractmethod
    def render(self, size) -> str:
        if self.scrollable:
            self._scrolled_text.text = self.text
            return self._scrollview.render(size)
        else:
            return truncate(self.text, self.truncation_alignment, size)

    @property
    def tools(self):
        tools = super().tools
        if self.scrollable:
            tools += self._scrollview.tools
        return tools
