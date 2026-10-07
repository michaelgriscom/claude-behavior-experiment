_NUMERALS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def to_roman(n: int) -> str:
    """Convert an integer in 1..3999 to a standard Roman numeral."""
    if not 1 <= n <= 3999:
        raise ValueError(f"out of range: {n}")
    out = []
    for value, numeral in _NUMERALS:
        while n >= value:
            out.append(numeral)
            n -= value
    return "".join(out)
