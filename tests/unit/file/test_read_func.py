"""
Unit tests for `genericlib.file.read` function.
Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/file/test_read_func.py
    or
    $ python -m pytest tests/unit/file/test_read_func.py
"""



import pytest

from genericlib.file import read


def test_read_existing_file(tmp_path):
    """Confirms that an existing UTF‑8 text file can be read successfully."""
    # Arrange
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world", encoding="utf-8")

    # Act
    content = read(str(file_path))

    # Assert
    assert content == "hello world"
    assert isinstance(content, str)


def test_read_with_different_encoding(tmp_path):
    """Validates reading a file with a non‑UTF‑8 encoding (Latin‑1)."""
    file_path = tmp_path / "latin1.txt"
    text = "café"  # contains accented character
    file_path.write_text(text, encoding="latin-1")

    # Act
    content = read(str(file_path), encoding="latin-1")

    # Assert
    assert content == text


def test_empty_filename_raises_value_error():
    """Ensures that an empty filename raises a ValueError."""
    with pytest.raises(ValueError):
        read("")


def test_nonexistent_file_raises_os_error(tmp_path):
    """Confirms that attempting to read a non‑existent file raises an OSError."""
    fake_file = tmp_path / "does_not_exist.txt"
    with pytest.raises(OSError):
        read(str(fake_file))


def test_read_large_file(tmp_path):
    """Verifies that large files are read fully into memory and content length matches."""
    # Arrange: simulate a large file by repeating text
    file_path = tmp_path / "large.txt"
    data = "abc123\n" * 10000
    file_path.write_text(data, encoding="utf-8")

    # Act
    content = read(str(file_path))

    # Assert
    assert content.startswith("abc123")
    assert len(content) == len(data)