"""
Unit test package for file.File class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/file/test_file_class.py
    or
    $ python -m pytest tests/unit/file/test_file_class.py
"""


import pytest
from datetime import datetime
import time

from genericlib import File
import genericlib.platform as platform
from genericlib import DotObject

from tests.unit import get_temp_file
from tests.unit import get_temp_dir

from tests.unit.file import get_sample_yaml_data


class TestFile:

    @pytest.mark.parametrize(
        "path,expected",
        [
            (get_temp_file(), True),
            (get_temp_file() + "_not_exist", False),
        ],
    )
    def test_is_file(self, path, expected):
        """Check if path is a file."""
        assert File.is_file(path) is expected

    @pytest.mark.parametrize(
        "path,expected",
        [
            (get_temp_dir(), True),
            (get_temp_dir() + "_not_exist", False),
        ],
    )
    def test_is_dir(self, path, expected):
        """Check if path is a directory."""
        assert File.is_dir(path) is expected

    @pytest.mark.parametrize(
        "path,expected",
        [
            (get_temp_file(), True),
            (get_temp_file() + "_not_exist", False),
        ],
    )
    def test_is_exist(self, path, expected):
        """Check if path exists."""
        assert File.is_exist(path) is expected

    @pytest.mark.parametrize(
        "src,dst",
        [
            (get_temp_file(), get_temp_file() + "_copy"),
            (get_temp_file(), get_temp_dir()),
        ],
    )
    def test_copy_file(self, src, dst):
        """Check single file copy."""
        assert File.copy_file(src, dst) != ""

    @pytest.mark.parametrize(
        "src,dst",
        [
            (get_temp_file(), get_temp_dir()),
            ([get_temp_file(), get_temp_file(), get_temp_file()], get_temp_dir()),
        ],
    )
    def test_copy_files(self, src, dst):
        """Check multiple file copy."""
        assert File.copy_files(src, dst)

    @pytest.mark.parametrize("path", [get_temp_dir() + "_new"])
    def test_make_directory(self, path):
        """Check directory creation."""
        assert File.make_directory(path)

    @pytest.mark.parametrize("path", [get_temp_file() + "_new"])
    def test_create_file(self, path):
        """Check file creation."""
        assert File.create(path)

    @pytest.mark.parametrize("path", [get_temp_file()])
    def test_get_path(self, path):
        """Check path resolution."""
        assert File.get_path(path)

    @pytest.mark.parametrize("path", [get_temp_file(), get_temp_dir()])
    def test_get_dir(self, path):
        """Check directory resolution from path."""
        assert File.get_dir(path)

    @pytest.mark.parametrize("path", [get_temp_file()])
    def test_get_content(self, path):
        """Check file content retrieval."""
        assert File.get_content(path) == ""

    @pytest.mark.parametrize("path", [get_temp_file()])
    def test_save_content(self, path):
        """Check saving content to file."""
        assert File.save(path, "abc")

    def test_delete_file(self):
        """Check file deletion."""
        path = get_temp_file() + "_new"
        File.save(path, str(datetime.now()))
        assert File.delete(path)

    def test_change_home_dir_to_generic(self):
        """Check home directory path conversion."""
        path = File.get_path("file1", is_home=True)
        assert File.change_home_dir_to_generic(path)

    def test_is_duplicate_file(self):
        """Verify duplicate file detection."""
        src = get_temp_file() + "_file"
        dst = get_temp_file() + "_copied_file"

        File.save(src, str(datetime.now()))
        File.copy_file(src, dst)

        assert File.is_duplicate_file(src, dst)

    def test_list_filenames_in_directory(self):
        """Verify listing of filenames in a directory."""
        tmp_dir = get_temp_dir()
        total_files = 3

        for i in range(1, total_files + 1):
            fname = File.get_path(tmp_dir, f"file{i}")
            File.save(fname, str(datetime.now()))
            time.sleep(0.001)

        result = File.get_list_of_filenames(top=tmp_dir)
        assert len(result) == total_files

    def test_quicklook_search(self):
        """Verify quicklook finds substring in file content."""
        fname = get_temp_file() + "_file"
        File.save(fname, "abc xyz 123")
        assert File.quicklook(fname, "xyz")

    def test_yaml_result_dict(self):
        """Verify YAML parsing returns dictionary results."""
        fname = get_temp_file() + ".yaml"
        File.save(fname, get_sample_yaml_data())

        result = File.get_result_from_yaml_file(fname)

        err_msg = f"Expected dict from {fname}, got {type(result).__name__}"
        assert isinstance(result, dict), err_msg

        assert result["location"]["main"] == "San Jose, CA"
        assert result["location"]["branch"] == "Milpitas, CA"
        assert result["employees"]["employee1"]["name"] == "Jack Brown"
        assert result["employees"]["employee2"]["name"] == "Linda Wilson"

    def test_yaml_result_dotobject(self):
        """Verify YAML parsing returns DotObject results."""
        fname = get_temp_file() + ".yaml"
        File.save(fname, get_sample_yaml_data())

        result = File.get_result_from_yaml_file(fname, dot_datatype=True)

        err_msg = f"Expected dict from {fname}, got {type(result).__name__}"
        assert isinstance(result, DotObject), err_msg

        assert result.location.main == "San Jose, CA"
        assert result.location.branch == "Milpitas, CA"
        assert result.employees.employee1.name == "Jack Brown"
        assert result.employees.employee2.name == "Linda Wilson"

    def test_yaml_result_with_substitution(self):
        """Verify YAML parsing with variable substitution."""
        fname = get_temp_file() + ".yaml"
        File.save(fname, get_sample_yaml_data())

        result = File.get_result_from_yaml_file(
            fname, dot_datatype=True, var_substitution=True
        )

        err_msg = f"Expected dict from {fname}, got {type(result).__name__}"
        assert isinstance(result, DotObject), err_msg

        assert result.location.main == "San Jose, CA"
        assert result.location.branch == "Milpitas, CA"
        assert result.employees.employee1.name == "Jack Brown"
        assert result.employees.employee1.office_location == "San Jose, CA"
        assert result.employees.employee2.name == "Linda Wilson"
        assert result.employees.employee2.office_location == "Milpitas, CA"

    @pytest.mark.parametrize(
        "filename,new_name,prefix,postfix,new_ext,expected",
        [
            ("", "blab_blab", "blab_blab", "blab_blab", "blab_blab", ""),
            (".", "blab_blab", "blab_blab", "blab_blab", "blab_blab", "."),
            ("abc/file1.txt", "file2.py", "", "", "", "abc/file2.py"),
            ("abc/file1.txt", "", "", "", "bat", "abc/file1.bat"),
            ("abc/file1.txt", "", "test_", "", "bat", "abc/test_file1.bat"),
            ("abc/test_file1.txt", "", "test_", "", "bat", "abc/test_file1.bat"),
            ("abc/file1.txt", "", "test_", "_xyz", "bat", "abc/test_file1_xyz.bat"),
            ("abc/test_file1.txt", "", "test_", "_xyz", "bat", "abc/test_file1_xyz.bat"),
            ("abc/test_file1_xyz.txt", "", "test_", "_xyz", "bat", "abc/test_file1_xyz.bat"),
        ],
    )
    def test_get_new_filename(self, filename, new_name, prefix, postfix, new_ext, expected):
        """Verify new filename generation with prefix, postfix, and extension changes."""
        result = File.get_new_filename(
            filename,
            new_name=new_name,
            prefix=prefix,
            postfix=postfix,
            new_extension=new_ext,
        )

        if platform.is_windows_os():
            assert result == expected.replace("/", "\\")
        else:
            assert result == expected
