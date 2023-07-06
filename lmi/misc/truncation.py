from gptos.lmi.misc.alignment import Alignment

TRUNC_SYMBOL = "…"


def truncate(string, /, *, alignment: Alignment, size: int, trunc_symbol=TRUNC_SYMBOL):

    if size is None:
        return string

    if len(string) <= size:
        return string
    elif alignment == Alignment.LEFT:
        return string[: size - 1] + trunc_symbol
    elif alignment == Alignment.CENTER:
        return string[: size // 2 - 1] + trunc_symbol + string[-size // 2 + 1 :]
    elif alignment == Alignment.RIGHT:
        return trunc_symbol + string[1 - size :]
    else:
        raise ValueError(f"Invalid alignment: {alignment}")
