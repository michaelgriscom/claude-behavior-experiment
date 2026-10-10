from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def invoice_total(subtotal, tax_rate, discount):
    """Total for an invoice: the fixed discount comes off the subtotal, then tax is added."""
    subtotal = Decimal(subtotal)
    taxed = subtotal * (1 + Decimal(tax_rate))
    total = taxed - Decimal(discount)
    return total.quantize(CENT, rounding=ROUND_HALF_UP)


def line_total(unit_price, quantity):
    return (Decimal(unit_price) * quantity).quantize(CENT, rounding=ROUND_HALF_UP)
