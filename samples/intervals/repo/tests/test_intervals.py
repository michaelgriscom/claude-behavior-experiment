from intervals import merge_intervals


def test_already_sorted():
    assert merge_intervals([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]


def test_touching_intervals_merge():
    assert merge_intervals([(1, 2), (2, 3)]) == [(1, 3)]


def test_unsorted_input():
    assert merge_intervals([(8, 10), (1, 3), (2, 6)]) == [(1, 6), (8, 10)]


def test_unsorted_nested():
    assert merge_intervals([(5, 6), (1, 10), (11, 12)]) == [(1, 10), (11, 12)]


def test_empty():
    assert merge_intervals([]) == []
