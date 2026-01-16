"""
genericlib.shell
================

Shell command utilities for GenericLib.

This module provides helper functions to execute, manage, and
validate shell commands within Python applications. It abstracts
common subprocess patterns, offering a consistent interface for
running commands, capturing output, and handling errors.
"""

import subprocess

from genericlib import DotObject, ECODE


def execute_command(cmdline):
    """
    Execute a shell command and capture its result.

    This method runs the specified command line string in the system shell
    using `subprocess.getstatusoutput`. It collects both the exit code and
    the command's output, then wraps them in a `DotObject` for convenient
    access. A success flag is also included for quick checks.

    Parameters
    ----------
    cmdline : str
        The shell command to execute, provided as a single string.

    Returns
    -------
    DotObject
        An object containing:
        - output : str
            The captured stdout and stderr output from the command.
        - exit_code : int
            The exit status code returned by the shell.
        - is_success : bool
            True if the exit code equals `ECODE.SUCCESS`, False otherwise.

    Notes
    -----
    - This method is useful for programmatically running shell commands
      while capturing their results in a structured way.
    - The `is_success` flag depends on the definition of `ECODE.SUCCESS`
      in your environment (commonly 0).
    """
    exit_code, output = subprocess.getstatusoutput(cmdline)
    result = DotObject(
        output=output,                          # noqa
        exit_code=exit_code,                    # noqa
        is_success=exit_code == ECODE.SUCCESS   # noqa
    )
    return result
