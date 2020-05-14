import string


def is_color(value: str) -> bool:
    return len(value) == 6 and all([ch in string.hexdigits for ch in value])


def is_base16(value: str) -> bool:
    return (
        len(value) == 6
        and value[:4] == "base"
        and value[4] in string.hexdigits
        and value[5] in string.hexdigits
    )
