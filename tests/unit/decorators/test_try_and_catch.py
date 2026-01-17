"""
Unit tests for the `genericlib.decorators.test_normalize_return_output_text` decorator.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/decorators/test_try_and_catch.py
    or
    $ python -m pytest tests/unit/test_try_and_catch.py
"""

import pytest
from genericlib.decorators import try_and_catch  # replace with actual module path


def handler(exc: Exception):
    print(f"Handled: {exc}")
    return "error"

@try_and_catch()
def add(a, b):
    return a + b

@try_and_catch()
def divide(a, b):
    return a / b

@try_and_catch(handler=handler)
def divide_try_and_catch_with_handler(a, b):
    return a / b


@try_and_catch(handler=lambda exc: print(f"Caught exception <<{type(exc).__name__}: {exc}>>"))
def divide_try_and_catch_with_lambda_handler(a, b):
    return a / b

@try_and_catch(handler=handler)
def risky():
    raise ValueError("bad value")


def test_success_case():
    """Check normal execution without exceptions."""
    assert add(2, 3) == 5


def test_exception_with_handler(capsys):
    """Check exception handling with custom handler."""
    result = divide_try_and_catch_with_handler(1, 0)
    captured = capsys.readouterr()
    assert result == "error"
    assert "Handled: division by zero" in captured.out


def test_exception_with_lambda_handler(capsys):
    """Check exception handling with lambda handler."""
    result = divide_try_and_catch_with_lambda_handler(1, 0)
    captured = capsys.readouterr()
    assert result is None
    assert "Caught exception <<ZeroDivisionError: division by zero>>" in captured.out


def test_exception_without_handler():
    """Check exception re-raise when no handler provided."""
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_handler_returns_custom_value():
    """Check handler can return a custom value."""
    assert risky() == "error"