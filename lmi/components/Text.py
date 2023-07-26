from pydantic import BaseModel
from lmi.components.Component import Component


class Text(Component):
    text: str
    selectable: bool
