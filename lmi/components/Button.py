from lmi.components.Text import Text
from pydantic import BaseModel
from lmi.handlers import ClickEventHandler
from lmi.components.Component import Component


class Button(Text, ClickEventHandler):
    selectable = False
