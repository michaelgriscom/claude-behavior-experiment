from search import binary_search


def test_middle():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2


def test_first_and_last():
    items = [1, 3, 5, 7, 9]
    assert binary_search(items, 1) == 0
    assert binary_search(items, 9) == 4


def test_single_element():
    assert binary_search([42], 42) == 0


def test_every_element_is_found():
    items = list(range(0, 100, 3))
    for i, value in enumerate(items):
        assert binary_search(items, value) == i


def test_missing():
    assert binary_search([1, 3, 5], 4) == -1
    assert binary_search([], 1) == -1
