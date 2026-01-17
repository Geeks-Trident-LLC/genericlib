"""
Unit tests for `genericlib.file.safe_load_yaml`.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/file/test_write_func.py
    or
    $ python -m pytest tests/unit/file/test_write_func.py
"""

import pytest
import yaml

from genericlib.file import safe_load_yaml


def test_load_valid_yaml_dict(tmp_path):
    """Confirms that a valid YAML file containing a dictionary is parsed correctly."""
    file_path = tmp_path / "config.yaml"
    file_path.write_text("key: value\nnumber: 42", encoding="utf-8")

    result = safe_load_yaml(str(file_path))
    assert isinstance(result, dict)
    assert result["key"] == "value"
    assert result["number"] == 42


def test_load_valid_yaml_list(tmp_path):
    """Validates that a YAML file containing a list is parsed into a Python list."""
    file_path = tmp_path / "list.yaml"
    file_path.write_text("- one\n- two\n- three", encoding="utf-8")

    result = safe_load_yaml(str(file_path))
    assert isinstance(result, list)
    assert result == ["one", "two", "three"]


def test_empty_filename_raises_value_error():
    """Ensures that passing an empty filename raises a ValueError."""
    with pytest.raises(ValueError):
        safe_load_yaml("")


def test_nonexistent_file_raises_os_error(tmp_path):
    """Confirms that attempting to load a nonexistent file raises an OSError."""
    fake_file = tmp_path / "does_not_exist.yaml"
    with pytest.raises(OSError):
        safe_load_yaml(str(fake_file))


def test_invalid_yaml_raises_yaml_error(tmp_path):
    """Ensures that invalid YAML content raises a yaml.YAMLError."""
    file_path = tmp_path / "invalid.yaml"
    # Invalid YAML: unbalanced brackets
    file_path.write_text("list: [1, 2, 3", encoding="utf-8")

    with pytest.raises(yaml.YAMLError):
        safe_load_yaml(str(file_path))