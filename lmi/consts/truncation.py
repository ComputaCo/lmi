from lmi.consts.alignment import Alignment


TRUNC_SYMBOL = "…"


def truncate(string, /, *, alignment: Alignment, size: int, trunc_symbol=TRUNC_SYMBOL):
    if size is None:
        return string

    if len(string) <= size:
        return string

    match alignment:
        case Alignment.LEFT:
            return string[: size - 1] + trunc_symbol
        case Alignment.CENTER:
            return string[: size // 2 - 1] + trunc_symbol + string[-size // 2 + 1 :]
        case Alignment.RIGHT:
            return trunc_symbol + string[1 - size :]
        case _:
            raise ValueError(f"Invalid alignment: {alignment}")
