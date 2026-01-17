"""
Unit tests for the `genericlib.shell` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/shell/test_shell.py
    or
    $ python -m pytest tests/unit/shell/test_shell.py
"""

import genericlib.platform as platform
from genericlib.shell import execute_command


class TestExecuteCommandFunc:
    def test_execute_command(self):
        """Verify shell command runs successfully."""
        cmdline = 'dir' if platform.is_windows_os() else 'ls'
        result = execute_command(cmdline)
        assert result.exit_code == 0
        assert result.is_success is True

    def test_execute_invalid_command(self):
        """Check invalid command handling."""
        result = execute_command("nonexistent_command_xyz")
        assert result.is_success is False
        assert result.exit_code != 0
        assert result.is_success is False
