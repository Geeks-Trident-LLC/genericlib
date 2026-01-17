"""
Unit tests for the genericlib.config module.

Usage
-----
Run pytest from the project root:
    $ pytest tests/unit/test_config.py
    or
    $ python -m pytest tests/unit/test_config.py
"""

import pytest
import genericlib.config as config
from genericlib.shell import PackageInfo

# Package info for genericlib
pkg_info = PackageInfo("genericlib")

# Skip marker if genericlib is not installed
skip_if_missing_genericlib = pytest.mark.skipif(
    not pkg_info.is_installed,
    reason="Skipping: genericlib package is not installed."
)


@skip_if_missing_genericlib
def test_version_matches_config():
    """Ensure installed package version matches config version."""
    assert pkg_info.is_installed is True
    assert pkg_info.version == config.version