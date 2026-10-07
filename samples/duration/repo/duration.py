import re

_UNITS = {"h": 3600, "m": 60, "s": 1}
_TOKEN = re.compile(r"(\d)([hms])")


def parse_duration(text: str) -> int:
    """Parse a compact duration like "1h30m" or "45s" into seconds."""
    text = text.strip()
    if not re.fullmatch(r"(\d+[hms])+", text):
        raise ValueError(f"bad duration: {text!r}")
    return sum(int(number) * _UNITS[unit] for number, unit in _TOKEN.findall(text))
