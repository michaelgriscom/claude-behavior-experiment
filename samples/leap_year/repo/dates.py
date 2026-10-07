_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_leap(year: int) -> bool:
    """Gregorian leap year rule."""
    return year % 4 == 0 and year % 100 != 0


def days_in_month(year: int, month: int) -> int:
    if not 1 <= month <= 12:
        raise ValueError(f"bad month: {month}")
    if month == 2 and is_leap(year):
        return 29
    return _DAYS[month - 1]
