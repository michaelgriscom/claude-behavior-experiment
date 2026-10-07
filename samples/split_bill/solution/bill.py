def split_bill(total_cents: int, people: int) -> list[int]:
    """Split a bill into per-person shares, in cents.

    Shares must sum exactly to total_cents and differ by at most one cent.
    Any leftover cents go to the first people in the list.
    """
    if people <= 0:
        raise ValueError("need at least one person")
    share, leftover = divmod(total_cents, people)
    return [share + 1 if i < leftover else share for i in range(people)]
