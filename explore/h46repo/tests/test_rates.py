from shipping.rates import shipping_cost


def test_flat_rate():
    assert shipping_cost(20.00, 1.0) == 4.99


def test_free_at_threshold():
    assert shipping_cost(50.00, 1.0) == 0.0


def test_free_above_threshold():
    assert shipping_cost(80.00, 5.0) == 0.0


def test_started_kg_rounds_up():
    assert shipping_cost(20.00, 2.2) == 6.49


def test_two_extra_kg():
    assert shipping_cost(20.00, 4.0) == 7.99
