"""
Unit tests for the `genericlib.number` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_number.py
    or
    $ python -m pytest tests/unit/test_number.py
"""

import pytest
from genericlib import number


class TestIsBoolean:
    """Tests for the is_boolean() function."""

    def test_true_false_strings(self):
        """Ensure 'true' and 'false' strings are recognized as booleans."""
        assert number.is_boolean("true")
        assert number.is_boolean("false")

    def test_numeric_strings(self):
        """Ensure '0', '1', '0.0', '1.0' are recognized as booleans."""
        assert number.is_boolean("0")
        assert number.is_boolean("1")
        assert number.is_boolean("0.0")
        assert number.is_boolean("1.0")

    def test_invalid_string(self):
        """Ensure unrelated strings are not recognized as booleans."""
        assert not number.is_boolean("yes")
        assert not number.is_boolean("no")

    def test_numeric_types(self):
        """Ensure numeric types 0 and 1 are recognized as booleans."""
        assert number.is_boolean(0)
        assert number.is_boolean(1)
        assert not number.is_boolean(2)


class TestIsInteger:
    """Tests for the is_integer() function."""

    def test_integer_strings(self):
        """Ensure integer strings are recognized as integers."""
        assert number.is_integer("42")
        assert number.is_integer("-7")

    def test_boolean_strings(self):
        """Ensure 'true' and 'false' strings are recognized as integers."""
        assert number.is_integer("true")
        assert number.is_integer("false")

    def test_invalid_string(self):
        """Ensure non-integer strings are not recognized as integers."""
        assert not number.is_integer("3.14")
        assert not number.is_integer("hello")

    def test_numeric_types(self):
        """Ensure int and bool types are recognized as integers."""
        assert number.is_integer(10)
        assert number.is_integer(True)
        assert not number.is_integer(3.14)


class TestIsFloat:
    """Tests for the is_float() function."""

    def test_float_strings(self):
        """Ensure float strings are recognized as floats."""
        assert number.is_float("3.14")
        assert number.is_float("-0.5")
        assert number.is_float("42")  # integers are valid floats too

    def test_boolean_strings(self):
        """Ensure 'true' and 'false' strings are recognized as floats."""
        assert number.is_float("true")
        assert number.is_float("false")

    def test_invalid_string(self):
        """Ensure non-numeric strings are not recognized as floats."""
        assert not number.is_float("hello")

    def test_numeric_types(self):
        """Ensure int, float, and bool types are recognized as floats."""
        assert number.is_float(3.14)
        assert number.is_float(42)
        assert number.is_float(True)


class TestIsNumber:
    """Tests for the is_number() function."""

    def test_combined_checks(self):
        """Ensure boolean, integer, and float inputs are recognized as numbers."""
        assert number.is_number("true")
        assert number.is_number("42")
        assert number.is_number("3.14")
        assert not number.is_number("hello")


class TestTryToGetNumber:
    """Tests for the try_to_get_number() function."""

    def test_boolean_string(self):
        """Ensure 'true' and 'false' strings are converted to booleans."""
        success, val = number.try_to_get_number("true")
        assert success and val is True
        success, val = number.try_to_get_number("false")
        assert success and val is False

    def test_integer_string(self):
        """Ensure integer strings are converted to int."""
        success, val = number.try_to_get_number("123")
        assert success and val == 123

    def test_float_string(self):
        """Ensure float strings are converted to float."""
        success, val = number.try_to_get_number("3.14")
        assert success and pytest.approx(val, 0.01) == 3.14

    def test_cast_to_type(self):
        """Ensure conversion respects the requested return_type."""
        success, val = number.try_to_get_number("123", return_type=float)
        assert success and isinstance(val, float)

    def test_numeric_types(self):
        """Ensure native numeric/boolean types are returned correctly."""
        success, val = number.try_to_get_number(42)
        assert success and val == 42
        success, val = number.try_to_get_number(True)
        assert success and val is True

    def test_invalid_string(self):
        """Ensure invalid strings return False and original object."""
        success, val = number.try_to_get_number("hello")
        assert not success and val == "hello"