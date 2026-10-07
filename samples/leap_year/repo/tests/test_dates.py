from dates import days_in_month, is_leap


def test_ordinary_leap_years():
    assert is_leap(2024)
    assert not is_leap(2023)


def test_centuries():
    assert not is_leap(1900)
    assert not is_leap(2100)
    assert is_leap(2000)
    assert is_leap(2400)


def test_february():
    assert days_in_month(2023, 2) == 28
    assert days_in_month(2024, 2) == 29
    assert days_in_month(2000, 2) == 29
