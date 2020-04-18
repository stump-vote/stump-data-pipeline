from util.string import camel_to_snake

import pytest


@pytest.mark.parametrize(
    "s, expected",
    (
        ("camelCase", "camel_case",),
        ("snake_case", "snake_case",),
        ("WEIRDness", "WEIRDness",),
        ("CapitalizedCamelCase", "Capitalized_camel_case",),
    ),
)
def test_camel_to_snake(s, expected):
    assert camel_to_snake(s) == expected
