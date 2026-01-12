"""
Unit tests for the `do_soft_regex_escape` function in `genericlib.text`.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/text/test_do_soft_regex_escape.py
    or
    $ python -m pytest tests/unit/text/test_do_soft_regex_escape.py

"""

import pytest
from genericlib.text import do_soft_regex_escape


class TestDoSoftRegexEscape:
    """Unit tests for do_soft_regex_escape."""

    def test_basic_string(self):
        assert do_soft_regex_escape("hello") == "hello"

    def test_regex_metacharacters(self):
        assert do_soft_regex_escape("^$.*+?|{}[]()\\") == (
            "\\^\\$\\.\\*\\+\\?\\|\\{\\}\\[\\]\\(\\)\\\\"
        )

    def test_punctuation_non_metacharacters(self):
        # Comma and exclamation should remain unescaped
        assert do_soft_regex_escape("hi, world!") == "hi, world!"

    def test_mixed_content(self):
        assert do_soft_regex_escape("price$100") == "price\\$100"

    def test_bytes_input(self):
        assert do_soft_regex_escape(b"dog") == "dog"

    def test_integer_input(self):
        assert do_soft_regex_escape(123) == "123"

    def test_nested_escape(self):
        # Parentheses must be escaped
        assert do_soft_regex_escape("a(b)c") == "a\\(b\\)c"

    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("cat.dog", "cat\\.dog"),
            ("a+b", "a\\+b"),
            ("{value}", "\\{value\\}"),
            ("hello world", "hello world"),
        ],
    )
    def test_parametrized_cases(self, raw, expected):
        assert do_soft_regex_escape(raw) == expected
