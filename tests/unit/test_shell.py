"""
Unit tests for the `genericlib.shell` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_shell.py
    or
    $ python -m pytest tests/unit/test_shell.py
"""

import genericlib.platform as platform
from genericlib.shell import execute_command


def test_execute_command():
    """Verify shell command runs successfully."""
    cmdline = 'dir' if platform.is_windows_os() else 'ls'
    result = execute_command(cmdline)
    assert result.exit_code == 0
    assert result.is_success is True
