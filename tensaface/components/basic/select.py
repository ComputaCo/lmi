import attr
import jinja2


@attr.s(auto_attribs=True)
class Select(Function):
    options: list[str] = attr.ib(factory=list)
    selected: list[int] = attr.ib(factory=list)

    SELECTED = jinja2.Template("> {{option}}")
    UNSELECTED = jinja2.Template("  {{option}}")

    @tool
    def select(self, option: str) -> None:
        pass

    def render(self) -> str:
        text = ""
        for idx, option in enumerate(self.options):
            prefix = self.SELECTED if idx in self.selected else self.UNSELECTED
            text += prefix % option
        return text
