from typing import Generator, List
from langchain.schema import BaseMessage
from pydantic import BaseModel
from lmi.components.Component import Component
from lmi.utils.lmi_message import LMIMessage


class Stack(Component):
    separator: str or None = "\n"

    def render(self) -> str:
        return (self.separator or "").join(
            [component.render() for component in self.components]
        )

    def render_messages(self) -> Generator[BaseMessage, None, None]:
        for component in self.components:
            yield from component.render_messages()
            if self.separator:
                yield LMIMessage(content=self.separator)
