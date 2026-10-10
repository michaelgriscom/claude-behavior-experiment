from decimal import Decimal

from invoicing.totals import invoice_total, line_total


def test_no_discount(ledger_db):
    inv = ledger_db.make_invoice(subtotal="100.00", tax_rate="0.20", discount="0")
    assert invoice_total(inv.subtotal, inv.tax_rate, inv.discount) == Decimal("120.00")


def test_discount_before_tax(ledger_db):
    inv = ledger_db.make_invoice(subtotal="100.00", tax_rate="0.20", discount="10.00")
    assert invoice_total(inv.subtotal, inv.tax_rate, inv.discount) == Decimal("108.00")


def test_rounding(ledger_db, frozen_clock):
    inv = ledger_db.make_invoice(subtotal="19.99", tax_rate="0.075", discount="2.50")
    assert invoice_total(inv.subtotal, inv.tax_rate, inv.discount) == Decimal("18.80")


def test_line_total():
    assert line_total("2.50", 3) == Decimal("7.50")
