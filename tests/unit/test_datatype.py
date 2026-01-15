"""
Unit tests for the `genericlib.datatype` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_datatype.py
    or
    $ python -m pytest tests/unit/test_datatype.py
"""

import pytest

import genericlib.datatype as datatype

from tests.unit import dummy_generator
from tests.unit import DummyClass
from tests.unit import DummyDataClass


@pytest.mark.parametrize(
    "func,obj,expected",
    [
        (datatype.is_dict, dict(a=1, b=2), True),
        (datatype.is_dict, list([1, 2]), False),

        (datatype.is_mapping, dict(a=1, b=2), True),
        (datatype.is_mapping, list([1, 2]), False),

        (datatype.is_list, list([1, 2]), True),
        (datatype.is_list, dict(a=1, b=2), False),

        (datatype.is_mutable_sequence, list([1, 2]), True),
        (datatype.is_mutable_sequence, tuple([1, 2]), False),

        (datatype.is_sequence, list([1, 2]), True),
        (datatype.is_sequence, tuple([1, 2]), True),
        (datatype.is_sequence, str("abc123"), True),
        (datatype.is_sequence, 123, False),

        (datatype.is_class, int, True),
        (datatype.is_class, list, True),
        (datatype.is_class, dict, True),
        (datatype.is_class, int(123), False),
        (datatype.is_class, list([1, 2]), False),
        (datatype.is_class, dict(a=1, b=2), False),

        (datatype.is_callable, print, True),
        (datatype.is_callable, iter, True),
        (datatype.is_callable, str.isdigit, True),
        (datatype.is_callable, print("Hello World"), False),
        (datatype.is_callable, iter([1, 2, 3]), False),
        (datatype.is_callable, str.isdigit("123"), False),

        (datatype.is_iterator, iter([1, 2, 3]), True),
        (datatype.is_iterator, range(1, 5), False),

        (datatype.is_generator, dummy_generator(), True),
        (datatype.is_generator, iter([1, 2, 3]), False),
        (datatype.is_generator, range(1, 5), False),

        (datatype.is_iterable, list([1, 2]), True),
        (datatype.is_iterable, "123", True),
        (datatype.is_iterable, 123, False),

        (datatype.is_none, None, True),
        (datatype.is_none, "", False),
        (datatype.is_none, 123, False),

    ]
)
def test_check_datatype(func, obj, expected):
    """Verify type-check helpers return expected results for various inputs."""
    assert func(obj) == expected


@pytest.mark.parametrize(
    "obj,expected",
    [
        (int, "int"),
        (123, "int"),
        (dummy_generator, "function"),
        (dummy_generator(), "generator"),
        ((i for i in range(5)), "generator"),
        (range, "range"),
        (range(5), "range"),
        (DummyClass, "DummyClass"),
        (DummyClass(), "DummyClass"),
        (DummyDataClass, "DummyDataClass"),
        (DummyDataClass(), "DummyDataClass"),
        (Exception, "Exception"),
        (Exception("Hello Exception"), "Exception"),
    ]
)
def test_get_class_name(obj, expected):
    """Ensure get_class_name returns the correct class name for classes,
    instances, functions, and generators."""
    assert datatype.get_class_name(obj) == expected


class TestCopyObj:
    """Tests for copy_obj."""

    def test_shallow_copy(self):
        """Shallow copy keeps inner references."""
        data = [[1], [2]]
        shallow = datatype.copy_obj(data, deep=False)
        assert shallow == data
        assert shallow is not data
        assert shallow[0] is data[0]

    def test_deep_copy(self):
        """Deep copy breaks inner references."""
        data = {"a": [1, 2]}
        deep = datatype.copy_obj(data, deep=True)
        assert deep == data
        assert deep is not data
        assert deep["a"] is not data["a"]


class TestCleanListOfDicts:
    """Tests for clean_list_of_dicts."""

    def test_non_list_input(self):
        """Return unchanged if not list."""
        data = {"a": " test "}
        assert datatype.clean_list_of_dicts(data) == data

    def test_strip_strings(self):
        """Strip whitespace from strings."""
        items = [{"a": " hello ", "b": "world"}]
        cleaned = datatype.clean_list_of_dicts(items)
        assert cleaned[0]["a"] == "hello"
        assert cleaned[0]["b"] == "world"

    def test_strip_with_chars(self):
        """Strip custom chars from strings."""
        items = [{"a": "xxhelloxx"}]
        cleaned = datatype.clean_list_of_dicts(items, chars="x")
        assert cleaned[0]["a"] == "hello"

    def test_bytes_handling(self):
        """Decode, strip, re-encode bytes."""
        items = [{"a": b" hello "}]
        cleaned = datatype.clean_list_of_dicts(items)
        assert cleaned[0]["a"] == b"hello"

    def test_nested_list_of_dicts(self):
        """Clean nested lists of dicts."""
        items = [{"a": [{"b": " hi "}]}]
        cleaned = datatype.clean_list_of_dicts(items)
        assert cleaned[0]["a"][0]["b"] == "hi"

    def test_mixed_types(self):
        """Copy non-str/bytes values."""
        items = [{"a": 123, "b": [1, 2], "c": {"nested": " ok "}}]
        cleaned = datatype.clean_list_of_dicts(items)
        assert cleaned[0]["a"] == 123
        assert cleaned[0]["b"] == [1, 2]
        assert cleaned[0]["c"]["nested"] == " ok "

    def test_list_with_non_dict_elements(self):
        """Copy non-dict list elements."""
        items = [" hello ", 42]
        cleaned = datatype.clean_list_of_dicts(items)
        assert cleaned[0] == " hello "
        assert cleaned[1] == 42
