"""
Unit tests for the `genericlib.misc` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_misc.py
    or
    $ python -m pytest tests/unit/test_misc.py
"""


import pytest

from genericlib.misc import sys_exit
from genericlib import ECODE

class TestSysExitFunction:

    def test_sys_exit_success(self, capsys):
        # Expect SystemExit with code SUCCESS
        with pytest.raises(SystemExit) as excinfo:
            sys_exit(success=True, msg="Gracefully exit")
        assert excinfo.value.code == ECODE.SUCCESS

        # Verify printed message
        captured = capsys.readouterr()
        assert "Gracefully exit" in captured.out

    def test_sys_exit_failure(self, capsys):
        # Expect SystemExit with code BAD
        with pytest.raises(SystemExit) as excinfo:
            sys_exit(success=False, msg="Something went wrong")
        assert excinfo.value.code == ECODE.BAD

        # Verify printed message
        captured = capsys.readouterr()
        assert "Something went wrong" in captured.out

    def test_sys_exit_no_message(self, capsys):
        # Expect SystemExit with code SUCCESS and no output
        with pytest.raises(SystemExit) as excinfo:
            sys_exit(success=True)
        assert excinfo.value.code == ECODE.SUCCESS

        captured = capsys.readouterr()
        assert captured.out == ""
