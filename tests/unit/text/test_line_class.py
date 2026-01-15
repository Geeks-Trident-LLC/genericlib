"""
Unit tests for the `genericlib.text.Text` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/text/test_line_class.py
    or
    $ python -m pytest tests/unit/text/test_line_class.py
"""

import pytest
from genericlib.text import Line
from genericlib.text import LineArgumentError


class TestLineProperties:
    """Tests for Line properties related to whitespace and emptiness."""

    def test_whitespace_only_line(self):
        line = Line("   ")
        assert line.is_empty is False
        assert line.is_optional_empty is True
        assert line.leading == "   "
        assert line.trailing == "   "
        assert line.is_leading is True
        assert line.is_trailing is True

    def test_line_with_leading_and_trailing(self):
        line = Line("   hello   ")
        assert line.clean_line == "hello"
        assert line.leading == "   "
        assert line.trailing == "   "
        assert line.is_leading is True
        assert line.is_trailing is True

    def test_line_without_leading_or_trailing(self):
        line = Line("hello")
        assert line.leading == ""
        assert line.trailing == ""
        assert line.is_leading is False
        assert line.is_trailing is False


class TestLineClassMethods:
    """Tests for Line class methods."""

    def test_is_line_single_line(self):
        assert Line.is_line("hello") is True

    def test_is_line_multiple_lines_returns_false(self):
        assert Line.is_line("hello\nworld") is False

    def test_is_line_multiple_lines_raises(self):
        with pytest.raises(LineArgumentError):
            Line.is_line("hello\nworld", on_failure=True)

    def test_has_leading_and_trailing(self):
        assert Line.has_leading("   hello") is True
        assert Line.has_trailing("hello   ") is True
        assert Line.has_leading("hello") is False
        assert Line.has_trailing("hello") is False

    def test_leading_and_trailing_whitespace_extractors(self):
        assert Line.get_leading("   hello") == "   "
        assert Line.get_trailing("hello   ") == "   "

    def test_has_whitespace_in_line(self):
        assert Line.has_whitespace_in_line("hello\tworld") is True
        assert Line.has_whitespace_in_line("hello world") is False
        assert Line.has_whitespace_in_line("helloworld") is False
        assert Line.has_whitespace_in_line(123) is False


class TestLineRegexPattern:
    """Tests for regex pattern conversion and splitting."""

    def test_convert_to_regex_pattern_with_simple_text(self):
        line = Line("hello")
        pattern = line.convert_to_regex_pattern()
        assert isinstance(pattern, str)
        assert pattern != ""

    def test_do_finditer_split_with_spaces(self):
        line = Line("hello world")
        result = line.do_finditer_split("hello world", pattern=r"\s+")
        assert isinstance(result, list)
        assert all(hasattr(obj, "to_pattern") for obj in result)