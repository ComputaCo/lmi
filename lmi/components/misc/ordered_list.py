from lmi.components.basic.list import List


class OrderedList(List):
    bullet_style = List.BulletStyle.NUMBERS
    format_string = r"{bullet}. {item}\n"
