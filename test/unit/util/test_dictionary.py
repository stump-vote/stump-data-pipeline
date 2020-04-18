import pytest

from util.dictionary import convert_keys_from_camel_to_snake


@pytest.mark.parametrize(
    "d, expected",
    (
        (
            {"camelCase": 1, "not_camel_case": 2},
            {"camel_case": 1, "not_camel_case": 2},
        ),
        (
            {
                "camelCase": {
                    "moreCamelCase": "foo",
                    "moreMoreCamelCase": {"evenMoreCamelCase": "bar"},
                },
                "not_camel": "baz",
            },
            {
                "camel_case": {
                    "more_camel_case": "foo",
                    "more_more_camel_case": {"even_more_camel_case": "bar"},
                },
                "not_camel": "baz",
            },
        ),
        (
            {"aList": ["doNotChangeMe", {"camelCase": "foo"}, {"camelCase": "bar"}]},
            {"a_list": ["doNotChangeMe", {"camel_case": "foo"}, {"camel_case": "bar"}]},
        ),
    ),
)
def test_convert_keys_from_camel_to_snake(d, expected):
    assert convert_keys_from_camel_to_snake(d) == expected
