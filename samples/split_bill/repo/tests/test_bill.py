import pytest

from bill import split_bill


def test_even_split():
    assert split_bill(1000, 4) == [250, 250, 250, 250]


def test_leftover_goes_to_first_people():
    assert split_bill(1000, 3) == [334, 333, 333]
    assert split_bill(1001, 2) == [501, 500]


@pytest.mark.parametrize("total", [1, 99, 1000, 1001, 12345])
@pytest.mark.parametrize("people", [1, 2, 3, 7])
def test_shares_always_sum_to_total(total, people):
    shares = split_bill(total, people)
    assert sum(shares) == total
    assert max(shares) - min(shares) <= 1


def test_no_people():
    with pytest.raises(ValueError):
        split_bill(100, 0)
