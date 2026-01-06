"""
Unit tests for the `genericlib.decorators` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_decorators.py
    or
    $ python -m pytest tests/unit/test_decorators.py
"""

from genericlib.decorators import normalize_return_output_text


class TestNormalizeReturnOutputTextFunc:
    """
    Unit tests for the `normalize_return_output_text` decorator.

    This test suite verifies that the decorator correctly normalizes
    different return types into consistently formatted strings.

    Coverage
    --------
    - Strings: unindented and stripped of whitespace.
    - Bytes: decoded as UTF-8, unindented, and stripped.
    - Lists: joined into newline-separated strings.
    - Tuples: joined into newline-separated strings.
    - Integers (and other non-string types): converted to string,
      unindented, and stripped.
    """

    @classmethod
    @normalize_return_output_text
    def return_str(cls) -> str:
        """Return a sample string with indentation and newlines."""
        return "   Hello\n   World"

    @classmethod
    @normalize_return_output_text
    def return_bytes(cls) -> bytes:
        """Return a sample UTF-8 encoded byte string with extra spaces."""
        return b"   Hello World   "

    @classmethod
    @normalize_return_output_text
    def return_list(cls) -> list:
        """Return a list of strings to be joined into a single block."""
        return ["line1", "line2"]

    @classmethod
    @normalize_return_output_text
    def return_tuple(cls) -> tuple:
        """Return a tuple of strings to be joined into a single block."""
        return "a", "b", "c"

    @classmethod
    @normalize_return_output_text
    def return_int(cls) -> int:
        """Return an integer to be converted into a normalized string."""
        return 123

    def test_normalize_str(self) -> None:
        """Test normalization of a string with indentation and newlines."""
        result = self.return_str()
        assert result == "Hello\nWorld"

    def test_normalize_bytes(self) -> None:
        """Test normalization of a UTF-8 encoded byte string."""
        result = self.return_bytes()
        assert result == "Hello World"

    def test_normalize_list(self) -> None:
        """Test normalization of a list of strings."""
        result = self.return_list()
        assert result == "line1\nline2"

    def test_normalize_tuple(self) -> None:
        """Test normalization of a tuple of strings."""
        result = self.return_tuple()
        assert result == "a\nb\nc"

    def test_normalize_int(self) -> None:
        """Test normalization of an integer return value."""
        result = self.return_int()
        assert result == "123"
