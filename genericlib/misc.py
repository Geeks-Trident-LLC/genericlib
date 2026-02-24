"""
genericlib.misc
===============
Miscellaneous utility functions for genericlib.

This module provides helper routines that support standardized program
termination and other lightweight operations. It is intended to centralize
common functionality that does not belong to a specific domain module.


Notes
-----
- Exit codes are defined in `genericlib.ECODE` and should be used consistently
  across the application.
- This module is designed for lightweight, generic helpers that simplify
  application control flow.
"""


import sys
from platform import python_version as py_version

from genericlib.constant import ECODE
from genericlib.text import decorate_list_of_line


def sys_exit(success: bool = True, msg: str = "") -> None:
    """
    Exit the program with a standardized code.

    Prints an optional message and terminates using ECODE.SUCCESS or
    ECODE.BAD to ensure consistent exit handling across the application.
    """
    exit_code = ECODE.SUCCESS if success else ECODE.BAD

    if msg:
        stream = sys.stderr if exit_code == ECODE.BAD else sys.stdout
        print(msg, file=stream)

    sys.exit(exit_code)


def ensure_tkinter_available(app_name: str = ""):
    """
    Import and return the tkinter module, exiting with a formatted error
    message if it is missing or fails to load.
    """
    name = app_name.title() if app_name else "The"

    try:
        import tkinter as tk
        return tk

    except ModuleNotFoundError:
        items = [
            f"{name} application failed to start.",
            f"Python {py_version()} was detected without the tkinter module.",
            "Install tkinter to enable GUI support and retry.",
        ]
        sys_exit(False, decorate_list_of_line(items))

    except Exception as exc:
        items = [
            f"{name} application could not be started due to:",
            f"*** {type(exc).__name__}: {exc}",
        ]
        sys_exit(False, decorate_list_of_line(items))
