"""
Unit tests for `genericlib.file.read_with_exit` function.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/file/test_read_with_exit_func.py
    or
    $ python -m pytest tests/unit/file/test_read_with_exit_func.py
"""

import pytest

from genericlib.file import read_with_exit


def test_read_existing_file(tmp_path):
    """Confirms that an existing UTF‑8 text file is read successfully."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world", encoding="utf-8")

    content = read_with_exit(str(file_path))
    assert content == "hello world"
    assert isinstance(content, str)


def test_read_with_different_encoding(tmp_path):
    """Validates reading a file with a non‑UTF‑8 encoding (Latin‑1)."""
    file_path = tmp_path / "latin1.txt"
    text = "café"
    file_path.write_text(text, encoding="latin-1")

    content = read_with_exit(str(file_path), encoding="latin-1")
    assert content == text


def test_nonexistent_file_triggers_sys_exit(tmp_path):
    """Ensures that attempting to read a nonexistent file triggers SystemExit."""
    fake_file = tmp_path / "does_not_exist.txt"
    with pytest.raises(SystemExit) as excinfo:
        read_with_exit(str(fake_file))
    assert excinfo.value.code == 1


def test_empty_filename_triggers_sys_exit():
    """Ensures that passing an empty filename triggers SystemExit."""
    with pytest.raises(SystemExit) as excinfo:
        read_with_exit("")
    assert excinfo.value.code == 1