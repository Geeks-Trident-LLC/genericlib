"""
Exception classes for genericlib.

This module defines custom exceptions used by the `text.Line` class
to provide more specific error handling. These exceptions extend
Python's built-in `Exception` type, allowing consumers of the library
to catch and handle errors in a structured way.

Classes
-------
LineError : Exception
    Base exception for errors raised by the `text.Line` class.
    Serves as the parent for more specialized exceptions.
LineArgumentError : LineError
    Raised when invalid arguments are passed to the `text.Line` class
    or its methods. Inherits from `LineError`.
"""


class LineError(Exception):
    """Base exception for errors raised by the `text.Line` class."""


class LineArgumentError(LineError):
    """Exception raised when invalid arguments are provided to `text.Line`."""
