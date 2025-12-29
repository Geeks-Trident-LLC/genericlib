"""
Unit tests for `genericlib.file.get_file_stream`.

This test suite verifies the behavior of the `get_file_stream` function,
ensuring correct handling of file operations across text and binary modes,
as well as proper error handling for invalid inputs.

Test Cases
----------
- test_read_existing_file
    Confirms that an existing text file can be opened and read correctly.
- test_write_and_read_file
    Validates that data can be written to a file and read back successfully.
- test_binary_mode
    Ensures binary read/write operations work and return a buffered stream.
- test_empty_filename_raises_value_error
    Verifies that an empty filename raises a ValueError.
- test_nonexistent_file_raises_os_error
    Confirms that attempting to open a non-existent file raises an OSError.
- test_invalid_mode_raises_value_error
    Ensures that passing an invalid mode string raises a ValueError.

Notes
-----
- Uses `tmp_path` fixture to create temporary files and directories safely.
- Tests cover both text (`io.TextIOBase`) and binary (`io.BufferedReader`)
  stream types returned by `open()`.
- Error conditions are validated using `pytest.raises`.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest /work_dir/tests/unit/file/test_get_file_stream_func.py
    or
    $ python -m pytest /work_dir/tests/unit/file/test_get_file_stream_func.py
"""


import io
import pytest

from genericlib.file import get_file_stream  # adjust import to your actual module


def test_read_existing_file(tmp_path):
    """Confirms that an existing text file can be opened and read correctly."""
    # Arrange
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")

    # Act
    with get_file_stream(str(file_path), mode="r", encoding="utf-8") as f:
        content = f.read()

    # Assert
    assert content == "hello world"
    assert isinstance(f, io.TextIOBase)


def test_write_and_read_file(tmp_path):
    """Validates that data can be written to a file and read back successfully."""
    file_path = tmp_path / "test_write.txt"

    # Write
    with get_file_stream(str(file_path), mode="w", encoding="utf-8") as f:
        f.write("pytest rocks")

    # Read back
    with get_file_stream(str(file_path), mode="r", encoding="utf-8") as f:
        content = f.read()

    assert content == "pytest rocks"


def test_binary_mode(tmp_path):
    """Ensures binary read/write operations work and return a buffered stream."""
    file_path = tmp_path / "test.bin"
    data = b"\x00\x01\x02"

    with get_file_stream(str(file_path), mode="wb") as f:
        f.write(data)

    with get_file_stream(str(file_path), mode="rb") as f:
        content = f.read()

    assert content == data
    assert isinstance(f, io.BufferedReader)


def test_empty_filename_raises_value_error():
    """Verifies that an empty filename raises a ValueError."""
    with pytest.raises(ValueError):
        get_file_stream("", mode="r")


def test_nonexistent_file_raises_os_error(tmp_path):
    """Confirms that attempting to open a non-existent file raises an OSError."""
    fake_file = tmp_path / "does_not_exist.txt"
    with pytest.raises(OSError):
        get_file_stream(str(fake_file), mode="r", encoding="utf-8")


def test_invalid_mode_raises_value_error(tmp_path):
    """Ensures that passing an invalid mode string raises a ValueError."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("data")
    with pytest.raises(ValueError):
        get_file_stream(str(file_path), mode="invalid")