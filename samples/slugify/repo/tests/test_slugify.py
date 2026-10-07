from slugify import slugify


def test_simple():
    assert slugify("Hello World") == "hello-world"


def test_punctuation_collapses_to_one_hyphen():
    assert slugify("Hello,  World!") == "hello-world"


def test_trims_and_collapses():
    assert slugify("  --Already--slugged--  ") == "already-slugged"


def test_digits_kept():
    assert slugify("Top 10 Tips (2024)") == "top-10-tips-2024"
