"""
Unit tests for the `enclose_string` function in `genericlib.text`.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/text/test_enclose_string_func.py
    or
    $ python -m pytest tests/unit/text/test_enclose_string_func.py

"""

import pytest
from genericlib.text import enclose_string


class TestEncloseString:
    """Unit tests for enclose_string."""

    def test_single_line_default_quote(self):
        assert enclose_string("hello") == '"hello"'

    def test_single_line_with_single_quote(self):
        assert enclose_string("it's fine", quote="'") == "'it\\'s fine'"

    def test_invalid_quote_defaults_to_double(self):
        assert enclose_string("hello", quote="*") == '"hello"'

    def test_bytes_input(self):
        assert enclose_string(b"dog") == '"dog"'

    def test_non_string_input(self):
        assert enclose_string(123) == '"123"'

    def test_multi_line_default(self):
        text = "hello\nworld"
        expected = '"""hello\nworld"""'
        assert enclose_string(text) == expected

    def test_multi_line_new_line_format(self):
        text = "hello\nworld"
        expected = '"""\nhello\nworld\n"""'
        assert enclose_string(text, is_new_line=True) == expected

    def test_escape_quotes_inside_text(self):
        text = 'She said "yes"'
        expected = '"She said \\"yes\\""'
        assert enclose_string(text) == expected

    @pytest.mark.parametrize(
        "raw, quote, expected",
        [
            ("abc", '"', '"abc"'),
            ("abc", "'", "'abc'"),
            ("a\nb", '"', '"""a\nb"""'),
            ("a\nb", "'", "'''a\nb'''"),
        ],
    )
    def test_parametrized_cases(self, raw, quote, expected):
        assert enclose_string(raw, quote=quote) == expected
