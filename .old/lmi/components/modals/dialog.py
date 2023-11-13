from lmi.components.core.abstract.component import Component


class Dialog(Component):
    @staticmethod
    def show(title, message, buttons: list[str] = ["ok"]):
        pass
