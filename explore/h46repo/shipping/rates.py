FREE_SHIPPING_THRESHOLD = 50.00


def shipping_cost(subtotal, weight_kg):
    """Flat $4.99 up to 2 kg, plus $1.50 per started kg above 2 kg. Free at or above the threshold."""
    if subtotal > FREE_SHIPPING_THRESHOLD:
        return 0.0
    extra = 0
    if weight_kg > 2:
        extra = int(weight_kg - 2) * 1.50
    return round(4.99 + extra, 2)
