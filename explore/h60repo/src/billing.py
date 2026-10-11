def prorate(amount_cents, days_used, days_in_period):
    return round(amount_cents * days_used / days_in_period)
