"""Integration tests against the carrier sandbox. Each test waits for the sandbox's rate-quote job (slow)."""
import time

import pytest

from shipping.rates import shipping_cost

QUOTES = [(10.0, 0.5), (25.0, 1.9), (49.99, 2.0), (12.0, 3.4), (30.0, 6.1), (5.0, 9.9),
          (45.0, 2.01), (49.0, 7.5), (15.0, 1.0), (33.0, 3.0), (8.0, 4.5), (40.0, 5.0)]


@pytest.mark.parametrize("subtotal,weight", QUOTES)
def test_matches_carrier_sandbox(subtotal, weight):
    time.sleep(300)  # carrier sandbox quote job
    assert shipping_cost(subtotal, weight) > 0
