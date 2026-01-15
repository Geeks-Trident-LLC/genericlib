"""
Unit tests for the `genericlib.text` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/text/test_text.py
    or
    $ python -m pytest tests/unit/text/test_text.py
"""


import pytest   # noqa

from genericlib.text import BaseMatchedObject
from genericlib.text import dedent_and_strip

from genericlib.text import decorate_list_of_line


class TestBaseMatchedObject:
    @pytest.mark.parametrize(
        'data,expected_result',
        [
            (' ', ' '),
            ('  ', ' +'),
            (' \t ', r'\s+'),
            ('abc xyz', 'abc xyz'),
            ('+++', r'\+{2,}'),
            ('+------------+', r'\+-{2,}\+'),
            ('+-----_-_-_-_-_-+', r'\+-{2,}(_-){2,}\+'),
            ('. . . . . . . . ', r'(\. ){2,}'),
        ]
    )
    def test_wrap_html(self, data, expected_result):
        node = BaseMatchedObject(data)
        result = node.to_pattern()
        assert result == expected_result


class TestDedentAndStripFunction:
    """
    Unit tests for the `dedent_and_strip` utility function.

    This test suite verifies that text normalization works correctly by
    converting input to string, removing common leading indentation, and
    stripping leading/trailing whitespace. It ensures consistent behavior
    across single-line, multi-line, and mixed-indentation inputs.
    """
    def test_dedent_and_strip_removes_indentation_and_whitespace(self):
        txt = "    line1\n    line2\n"
        result = dedent_and_strip(txt)
        assert result == "line1\nline2"

    def test_dedent_and_strip_trims_leading_and_trailing_spaces(self):
        txt = "   hello world   "
        result = dedent_and_strip(txt)
        assert result == "hello world"

    def test_dedent_and_strip_handles_multiline_with_mixed_indent(self):
        txt = """
            line1
              line2
            line3
        """
        result = dedent_and_strip(txt)
        # dedent removes common leading whitespace, strip removes outer blank lines
        assert result == "line1\n  line2\nline3"


class TestDecorateListOfLineFunction:
    """
    Unit tests for the `decorate_list_of_line` function.

    This test suite validates that framed text messages are generated
    correctly from lists of strings. It ensures proper alignment,
    border construction, and whitespace handling across a variety
    of input scenarios.
    """
    def test_single_line(self):
        expected = dedent_and_strip("""
            +--------------+
            | Hello Python |
            +--------------+
        """)
        lst_of_line = ["Hello Python"]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected

    def test_multiple_lines(self):
        expected = dedent_and_strip("""
            +------------------+
            | Short            |
            | Much longer line |
            | Mid              |
            +------------------+
        """)
        lst_of_line = ["Short", "Much longer line", "Mid"]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected

    def test_empty_string_line(self):
        expected = dedent_and_strip("""
            +-----+
            |     |
            | abc |
            +-----+
        """)
        lst_of_line = ["", "abc"]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected

    def test_all_empty_lines(self):
        expected = dedent_and_strip("""
            +--+
            |  |
            |  |
            +--+
        """)
        lst_of_line = ["", ""]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected

    def test_preserves_whitespace(self):
        expected = dedent_and_strip("""
            +----+
            | a  |
            | b  |
            +----+
        """)
        lst_of_line = ["a ", "b"]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected
