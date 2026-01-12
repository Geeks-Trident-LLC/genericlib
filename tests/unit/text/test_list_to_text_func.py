"""
Unit tests for the `list_to_text` function in `genericlib.text`.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/text/test_list_to_text_func.py
    or
    $ python -m pytest tests/unit/text/test_list_to_text_func.py

"""

from genericlib.text import list_to_text
from textwrap import dedent


class TestListToText:
    """Unit tests for the list_to_text function."""

    def test_no_arguments(self):
        """It should return an empty string when no arguments are provided."""
        assert list_to_text() == ""

    def test_single_string(self):
        """It should return the string itself when given a single string."""
        assert list_to_text("hello") == "hello"

    def test_multiple_strings(self):
        """It should join multiple string arguments with newlines."""
        expected = dedent("""\
            apple
            banana
            cherry
        """).strip()
        assert list_to_text("apple", "banana", "cherry") == expected

    def test_bytes_argument(self):
        """It should decode bytes as UTF-8 before joining."""
        assert list_to_text(b"dog") == "dog"

    def test_list_argument(self):
        """It should flatten a list of strings into newline-separated text."""
        expected = "cat\ndog\nbird"
        assert list_to_text(["cat", "dog", "bird"]) == expected

    def test_tuple_argument(self):
        """It should flatten a tuple of strings into newline-separated text."""
        expected = "red\ngreen\nblue"
        assert list_to_text(("red", "green", "blue")) == expected

    def test_nested_lists_and_tuples(self):
        """It should recursively flatten nested lists/tuples."""
        expected = "a\nb\nc\nd"
        assert list_to_text(["a", ("b", ["c", ("d",)])]) == expected

    def test_mixed_arguments(self):
        """It should handle strings, lists, tuples, and bytes together."""
        expected = "one\ntwo\nthree\nfour\nfive"
        assert list_to_text("one", ["two", "three"], ("four",), b"five") == expected

    def test_non_string_items(self):
        """It should convert non-string items to strings before joining."""
        expected = "123\nTrue\nNone"
        assert list_to_text(123, True, None) == expected

    def test_empty_list_and_tuple(self):
        """It should ignore empty lists/tuples and return empty string if nothing else."""
        assert list_to_text([], ()) == ""

    def test_list_with_empty_strings(self):
        """It should preserve empty strings as blank lines."""
        expected = dedent("""\
            first

            third
        """).strip()
        assert list_to_text(["first", "", "third"]) == expected
