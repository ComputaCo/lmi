from typing import Callable, Literal


PASS = lambda *args, **kwargs: None
Handler = Callable[[], None]

namespace_counter = {}


def gen_unique_name(namespace: str) -> str:
    namespace_counter[namespace] = namespace_counter.get(namespace, 0) + 1
    return f"{namespace}{namespace_counter[namespace]}"
