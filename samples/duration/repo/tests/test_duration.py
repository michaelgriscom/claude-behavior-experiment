import pytest

from duration import parse_duration


def test_single_digit_units():
    assert parse_duration("5m") == 300
    assert parse_duration("2h") == 7200


def test_multi_digit_units():
    assert parse_duration("90s") == 90
    assert parse_duration("1h30m") == 5400


def test_all_units():
    assert parse_duration("2h15m10s") == 2 * 3600 + 15 * 60 + 10


def test_rejects_garbage():
    with pytest.raises(ValueError):
        parse_duration("ten minutes")
