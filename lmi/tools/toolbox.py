from gptos.tools.tool import Tool


@attr.s(auto_attribs=True)
class Toolbox(Tool):
    """A toolbox is a tool that contains other tools."""

    @property
    def __doc__(self):
        return self.description

    @property
    def __name__(self):
        return self.name

    name: str
    description: str
    tools: list[Tool]

    def func(self, input) -> str:
        return "Select:" + "\t".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )
