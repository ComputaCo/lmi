from lmi.components.basic.list import List


class UnorderedList(List):
    bullet_style = List.BulletStyle.BULLETS
    format_string = r"{bullet} {item}\n"
