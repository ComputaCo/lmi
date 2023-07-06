from lmi.components.component import Component


class App(Component):
    @property
    def _hover_tool(self):
        pass  # TODO: implement

    @property
    def _type_tool(self):
        pass  # TODO: implement

    @property
    def _click_tool(self):
        pass  # TODO: implement

    @property
    def _scroll_tool(self):
        pass  # TODO: implement

    @property
    def _drag_tool(self):
        pass  # TODO: implement

    @property
    def _drop_tool(self):
        pass  # TODO: implement

    @property
    def tools(self) -> list[BaseTool]:
        return [child.tools for child in self.visible_components] + [
            self._hover_tool,
            self._type_tool,
            self._click_tool,
            self._scroll_tool,
            self._drag_tool,
            self._drop_tool,
        ]

    def serve(self, host, port):
        pass

    def run(self, agent):
        pass

    def cli(self):
        pass
