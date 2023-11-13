from lmi.components.basic.input import TextInput


class NumericInput(TextInput):
    
    def before_change(self, new_value: str):
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False