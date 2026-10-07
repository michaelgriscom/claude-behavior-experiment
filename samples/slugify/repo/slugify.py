import re


def slugify(text: str) -> str:
    """Turn arbitrary text into a URL slug.

    Lowercases, replaces each run of non-alphanumeric characters with a
    single hyphen, and trims leading/trailing hyphens.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9]", "-", text)
    return text.strip("-")
