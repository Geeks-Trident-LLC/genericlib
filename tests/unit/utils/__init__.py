"""
Unit tests for the `genericlib.utils` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/utils
    or
    $ python -m pytest tests/unit/utils
"""

import sys

class DummyClass:
    """A placeholder class used for testing dynamic exception naming."""


def sample_func_displaying_stdout():
    """
    Print a message to stdout and return a string.

    Returns
    -------
    str
        The string "return_value".
    """
    print("hello stdout")
    return "return_value"


def sample_func_displaying_stderr():
    """
    Print a message to stderr and return an integer.

    Returns
    -------
    int
        The integer 9999.
    """
    print("hello stderr", file=sys.stderr)
    return 9999


def sample_func_displaying_stdout_and_stderr():
    """
    Print messages to both stdout and stderr and return a string.

    Returns
    -------
    str
        The string "mixed".
    """
    print("stdout here")
    print("stderr here", file=sys.stderr)
    return "mixed"


def sample_func_args(x, y=0):
    """
    Print the sum of two arguments to stdout and return the sum.

    Parameters
    ----------
    x : int or float
        First operand.
    y : int or float, optional
        Second operand, defaults to 0.

    Returns
    -------
    int or float
        The sum of x and y.
    """
    print(f"sum={x+y}")
    return x + y