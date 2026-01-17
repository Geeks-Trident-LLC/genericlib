"""
Unit tests for `genericlib.file.write`.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/file/test_write_func.py
    or
    $ python -m pytest tests/unit/file/test_write_func.py
"""

import pytest

from genericlib.file import write, read  # adjust import to your actual module


def test_write_creates_new_file(tmp_path):
    """Confirms that writing to a new file creates it and stores the content."""
    file_path = tmp_path / "new.txt"
    write(str(file_path), "hello world")
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == "hello world"


def test_write_overwrites_existing_file(tmp_path):
    """Validates that writing to an existing file overwrites its previous content."""
    file_path = tmp_path / "overwrite.txt"
    file_path.write_text("old content", encoding="utf-8")

    write(str(file_path), "new content")
    assert file_path.read_text(encoding="utf-8") == "new content"


def test_write_with_different_encoding(tmp_path):
    """Ensures that writing with a non‑UTF‑8 encoding (Latin‑1) works correctly."""
    file_path = tmp_path / "latin1.txt"
    text = "café"
    write(str(file_path), text, encoding="latin-1")
    assert file_path.read_text(encoding="latin-1") == text


def test_empty_filename_raises_value_error():
    """Ensures that passing an empty filename raises a ValueError."""
    with pytest.raises(ValueError):
        write("", "data")


def test_write_permission_denied_triggers_os_error(tmp_path):
    """Confirms that attempting to write to a read‑only file raises an OSError."""
    file_path = tmp_path / "readonly.txt"
    file_path.write_text("cannot overwrite", encoding="utf-8")
    file_path.chmod(0o400)  # make file read-only

    with pytest.raises(OSError):
        write(str(file_path), "new content")

    # Reset permissions so tmp_path cleanup works
    file_path.chmod(0o600)