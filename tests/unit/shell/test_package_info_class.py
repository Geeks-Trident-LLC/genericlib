"""
Unit tests for the `genericlib.shell.PackageInfo` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/shell/test_package_info_class.py
    or
    $ python -m pytest tests/unit/shell/test_package_info_class.py
"""

import pytest
import re

from genericlib.shell import PackageInfo

from tests.unit import DummyCommandResult

class TestPackageInfoClassUsingDummyCommandResult:
    def test_freeze_detects_version(self, monkeypatch):
        """Check version detection from pip freeze."""
        def fake_exec(cmd):
            return DummyCommandResult("mypkg==1.2.3")
        monkeypatch.setattr("genericlib.shell.execute_command", fake_exec)

        pkg = PackageInfo("mypkg")
        assert pkg.is_installed is True
        assert pkg.version == "1.2.3"
        assert pkg.name == "mypkg"

    def test_freeze_detects_url(self, monkeypatch):
        """Check installed package with @ URL but no version."""
        def fake_exec(cmd):
            return DummyCommandResult("mypkg @ git+https://example.com/repo.git")
        monkeypatch.setattr("genericlib.shell.execute_command", fake_exec)

        pkg = PackageInfo("mypkg")
        assert pkg.is_installed is True
        assert pkg.version == ""  # no version from @
        assert pkg.name == "mypkg"


# Package info for pytest
pytest_info = PackageInfo("pytest")

# Skip marker if pytest is not installed
skip_if_no_pytest = pytest.mark.skipif(
    not pytest_info.is_installed,
    reason="Skipping: pytest package is not installed in the environment."
)


@skip_if_no_pytest
def test_pytest_installation():
    """Verify pytest is installed and version is valid."""
    assert pytest_info.is_installed is True
    assert pytest_info.name == "pytest"
    assert re.match(r"\d+\.\d+", pytest_info.version) is not None


# Package info for genericlib
genericlib_info = PackageInfo("genericlib")

# Skip marker if genericlib is not installed
skip_if_no_genericlib = pytest.mark.skipif(
    not genericlib_info.is_installed,
    reason="Skipping: genericlib package is not installed in the environment."
)


@skip_if_no_genericlib
def test_genericlib_installation():
    """Verify genericlib is installed and version is valid."""
    assert genericlib_info.is_installed is True
    assert genericlib_info.name == "genericlib"
    assert re.match(r"\d+\.\d+", genericlib_info.version) is not None
