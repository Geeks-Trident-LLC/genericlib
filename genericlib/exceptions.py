"""
genericlib.exceptions
=====================

Custom exception classes for the `genericlib` package.

This module defines specialized exceptions used primarily by the
`text.Line` class to provide more granular and descriptive error
handling. By extending Python's built-in `Exception` type, these
exceptions allow developers to catch and handle errors in a structured,
semantic way rather than relying on generic exceptions.

Classes
-------
LineError : Exception
    Base exception for errors raised by the `text.Line` class.
    Serves as the parent class for more specialized exceptions.
LineArgumentError : LineError
    Raised when invalid arguments are passed to the `text.Line` class
    or its methods. Inherits from `LineError`.

Design Notes
------------
- These exceptions are intended to make error handling more explicit
  and self-documenting.
- Using custom exceptions improves clarity in debugging and allows
  consumers of the library to distinguish between generic runtime
  errors and domain-specific issues.

"""


class LineError(Exception):
    """Base exception for errors raised by the `text.Line` class."""


class LineArgumentError(LineError):
    """Exception raised when invalid arguments are provided to `text.Line`."""
