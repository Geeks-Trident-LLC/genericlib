"""
Unit tests for the `genericlib` package.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest
    $ pytest tests/unit
    or
    $ python -m pytest
    $ python -m pytest tests/unit
"""


import tempfile


class DummyClass:
    """A placeholder class used for testing dynamic exception naming."""
    def __init__(self):
        self.var1 = "value 1"
        self.var2 = "value 2"

class DummyDataClass:
    """Dummy class used for negative test cases in `raise_exception`."""
    def __init__(self):
        self.var1 = "value 1"
        self.var2 = "value 2"


def get_temp_file():
    """Create a temporary file and return its filename."""
    _, tmp_file_name = tempfile.mkstemp()
    return tmp_file_name


def get_temp_dir():
    """Create a temporary directory and return its path."""
    tmp_dir = tempfile.mkdtemp()
    return tmp_dir

