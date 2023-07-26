from typing import Any, Union


def make_union(types: list[type[Any]]) -> type[Any]:
    t = types[0]
    for ti in types[1:]:
        t = Union[t, ti]
    return t
