"""
Unit tests for the `genericlib.platform` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_platform.py
    or
    $ python -m pytest tests/unit/test_platform.py
"""


import platform
import sys
import types
import genericlib.platform as platform_helper  # replace with your actual module name



class TestOSChecks:
    """Tests for OS detection helpers."""

    def test_is_windows_os(self, monkeypatch):
        """Detect Windows OS."""
        monkeypatch.setattr(platform, "system", lambda: "Windows")
        assert platform_helper.is_windows_os()
        assert not platform_helper.is_mac_os()
        assert not platform_helper.is_linux_os()

    def test_is_mac_os(self, monkeypatch):
        """Detect macOS."""
        monkeypatch.setattr(platform, "system", lambda: "Darwin")
        assert platform_helper.is_mac_os()
        assert platform_helper.is_nix_os()

    def test_is_linux_os(self, monkeypatch):
        """Detect Linux OS."""
        monkeypatch.setattr(platform, "system", lambda: "Linux")
        assert platform_helper.is_linux_os()
        assert platform_helper.is_nix_os()

    def test_is_nix_os_false(self, monkeypatch):
        """Detect non-Unix OS."""
        monkeypatch.setattr(platform, "system", lambda: "Windows")
        assert not platform_helper.is_nix_os()


class TestSystemInfo:
    """Tests for system and Python info helpers."""

    def test_get_kernel_info(self, monkeypatch):
        """Return kernel info."""
        fake_uname = types.SimpleNamespace(system="TestOS", release="1.0")
        monkeypatch.setattr(platform, "uname", lambda: fake_uname)
        assert platform_helper.get_kernel_info() == "TestOS 1.0"

    def test_get_python_info(self, monkeypatch):
        """Return Python version."""
        monkeypatch.setattr(platform, "python_version", lambda: "3.11.5")
        assert platform_helper.get_python_info() == "Python 3.11.5"

    def test_get_python_docs_url(self, monkeypatch):
        """Return Python docs URL."""
        fake_version = types.SimpleNamespace(major=3, minor=11)
        monkeypatch.setattr(sys, "version_info", fake_version)
        assert platform_helper.get_python_docs_url() == "https://docs.python.org/3.11/"