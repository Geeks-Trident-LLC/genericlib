"""
Unit tests for the `list_to_text` function in `genericlib.text`.

This test suite verifies that `list_to_text` correctly converts strings,
lists, and tuples into a newline-separated string representation. It ensures
robust handling of edge cases such as empty inputs, mixed argument types,
and non-string values.

Test Coverage
-------------
- No arguments: returns an empty string.
- Single string: returns the string itself.
- Multiple strings: joins arguments with newline separators.
- List or tuple inputs: flattens and converts elements to strings.
- Mixed inputs: handles combinations of strings, lists, and tuples.
- Non-string items: converts objects (e.g., int, bool, None) to string form.
- Empty lists/tuples: ignored unless containing empty strings.
- Empty strings: preserved as blank lines in the output.

The tests are written with `pytest` for readability and maintainability.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/text/test_list_to_text_func.py
    or
    $ python -m pytest tests/unit/text/test_list_to_text_func.py

"""

from genericlib.text import list_to_text
from genericlib.text import dedent_and_strip


class TestListToTextFunc:
    """Unit tests for the list_to_text function."""

    def test_no_arguments(self):
        """It should return an empty string when no arguments are provided."""
        assert list_to_text() == ""

    def test_single_string(self):
        """It should return the string itself when given a single string."""
        assert list_to_text("hello") == "hello"

    def test_multiple_strings(self):
        """It should join multiple string arguments with newlines."""
        expected = dedent_and_strip("""\
            apple
            banana
            cherry
        """)
        assert list_to_text("apple", "banana", "cherry") == expected

    def test_list_argument(self):
        """It should flatten a list of strings into newline-separated text."""
        expected = dedent_and_strip("""
            cat
            dog
            bird
        """)
        assert list_to_text(["cat", "dog", "bird"]) == expected

    def test_tuple_argument(self):
        """It should flatten a tuple of strings into newline-separated text."""
        expected = dedent_and_strip("""
            red
            green
            blue
        """)
        assert list_to_text(("red", "green", "blue")) == expected

    def test_mixed_arguments(self):
        """It should handle strings, lists, and tuples together."""
        expected = dedent_and_strip("""
            one
            two
            three
            four
        """)
        assert list_to_text("one", ["two", "three"], ("four",)) == expected

    def test_non_string_items(self):
        """It should convert non-string items to strings before joining."""
        expected = dedent_and_strip("""
            123
            True
            None
        """)
        assert list_to_text(123, True, None) == expected

    def test_empty_list_and_tuple(self):
        """It should ignore empty lists/tuples and
        return empty string if nothing else."""
        assert list_to_text([], ()) == ""

    def test_list_with_empty_strings(self):
        """It should preserve empty strings as blank lines."""
        expected = dedent_and_strip("""
            first

            third
        """)
        assert list_to_text(["first", "", "third"]) == expected
