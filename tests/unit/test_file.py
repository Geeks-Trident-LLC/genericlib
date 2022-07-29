import pytest
from datetime import datetime
import time
from textwrap import dedent

from genericlib import File
from genericlib import Misc

from . import get_temp_file
from . import get_temp_dir

sample_yaml_data = dedent("""
    location:
      main: San Jose, CA
      branch: Milpitas, CA
    employees:
      employee1:
        name: Jack Brown
        office_location: "{self.location.main}"
      employee2:
        name: Linda Wilson
        office_location: "{self.location.branch}"  
""").strip()


class TestFile:

    @pytest.mark.parametrize(
        "file_name,expected_result",
        [
            (get_temp_file(), True),
            (get_temp_file() + '_not_exist', False)
        ]
    )
    def test_is_file(self, file_name, expected_result):
        result = File.is_file(file_name)
        assert result is expected_result

    @pytest.mark.parametrize(
        "dir_name,expected_result",
        [
            (get_temp_dir(), True),
            (get_temp_dir() + '_not_exist', False)
        ]
    )
    def test_is_dir(self, dir_name, expected_result):
        result = File.is_dir(dir_name)
        assert result is expected_result

    @pytest.mark.parametrize(
        "file_name,expected_result",
        [
            (get_temp_file(), True),
            (get_temp_file() + '_not_exist', False)
        ]
    )
    def test_is_exist(self, file_name, expected_result):
        result = File.is_exist(file_name)
        assert result is expected_result

    @pytest.mark.parametrize(
        "src,dst",
        [
            (get_temp_file(), get_temp_file() + '_copy_file'),
            (get_temp_file(), get_temp_dir())
        ]
    )
    def test_copy_file(self, src, dst):
        result = File.copy_file(src, dst)
        assert result != ''

    @pytest.mark.parametrize(
        "src,dst",
        [
            (get_temp_file(), get_temp_dir()),
            ([get_temp_file(), get_temp_file(), get_temp_file()], get_temp_dir())
        ]
    )
    def test_copy_files(self, src, dst):
        result = File.copy_files(src, dst)
        assert result != ''

    @pytest.mark.parametrize(
        "src,dst",
        [
            (get_temp_file(), get_temp_dir()),
            ([
                 get_temp_file(),
                 get_temp_file(),
                 get_temp_file()
             ], get_temp_dir())
        ]
    )
    def test_copy_files(self, src, dst):
        result = File.copy_files(src, dst)
        assert result

    @pytest.mark.parametrize(
        "file_path",
        [
            get_temp_dir() + '_new_dir',
        ]
    )
    def test_make_directory(self, file_path):
        result = File.make_directory(file_path)
        assert result

    @pytest.mark.parametrize(
        "file_name",
        [
            get_temp_file() + '_new_file',
        ]
    )
    def test_create(self, file_name):
        result = File.create(file_name)
        assert result

    @pytest.mark.parametrize(
        "file_name",
        [
            get_temp_file(),
        ]
    )
    def test_get_path(self, file_name):
        result = File.get_path(file_name)
        assert result

    @pytest.mark.parametrize(
        "file_name_or_directory",
        [
            get_temp_file(),
            get_temp_dir()
        ]
    )
    def test_get_dir(self, file_name_or_directory):
        result = File.get_dir(file_name_or_directory)
        assert result

    @pytest.mark.parametrize(
        "file_name",
        [
            get_temp_file(),
        ]
    )
    def test_get_content(self, file_name):
        result = File.get_content(file_name)
        assert result == ''

    @pytest.mark.parametrize(
        "file_name",
        [
            get_temp_file(),
        ]
    )
    def test_save(self, file_name):
        result = File.save(file_name, 'abc')
        assert result

    def test_delete(self):
        file_name = get_temp_file() + '_new_file'
        File.save(file_name, str(datetime.now()))
        result = File.delete(file_name)
        assert result

    def test_change_home_dir_to_generic(self):
        file_name = File.get_path('file1', is_home=True)

        result = File.change_home_dir_to_generic(file_name)
        assert result

    def test_is_duplicate_file(self):
        file_name = get_temp_file() + '_file'
        copied_file_name = get_temp_file() + '_copied_file'

        File.save(file_name, str(datetime.now()))
        File.copy_file(file_name, copied_file_name)

        result = File.is_duplicate_file(file_name, copied_file_name)
        assert result

    def test_get_list_of_filenames(self):
        tmp_dir = get_temp_dir()

        total = 3
        for i in range(1, total + 1):
            file_name = File.get_path(tmp_dir, 'file%s' % i)
            File.save(file_name, str(datetime.now()))
            time.sleep(0.001)

        result = File.get_list_of_filenames(top=tmp_dir)
        assert len(result) == total

    def test_quick_look(self):
        file_name = get_temp_file() + '_file'
        File.save(file_name, 'abc xyz 123')
        result = File.quicklook(file_name, 'xyz')
        assert result

    def test_get_result_from_yaml_file_case1(self):
        file_name = get_temp_file() + '.yaml'

        File.save(file_name, sample_yaml_data)

        result = File.get_result_from_yaml_file(file_name)
        assert result['location']['main'] == 'San Jose, CA'
        assert result['location']['branch'] == 'Milpitas, CA'
        assert result['employees']['employee1']['name'] == 'Jack Brown'
        assert result['employees']['employee2']['name'] == 'Linda Wilson'

    def test_get_result_from_yaml_file_case2(self):
        file_name = get_temp_file() + '.yaml'

        File.save(file_name, sample_yaml_data)

        result = File.get_result_from_yaml_file(file_name, dot_datatype=True)
        assert result.location.main == 'San Jose, CA'
        assert result.location.branch == 'Milpitas, CA'
        assert result.employees.employee1.name == 'Jack Brown'
        assert result.employees.employee2.name == 'Linda Wilson'

    def test_get_result_from_yaml_file_case3(self):
        file_name = get_temp_file() + '.yaml'

        File.save(file_name, sample_yaml_data)

        result = File.get_result_from_yaml_file(
            file_name, dot_datatype=True, var_substitution=True
        )
        assert result.location.main == 'San Jose, CA'
        assert result.location.branch == 'Milpitas, CA'

        assert result.employees.employee1.name == 'Jack Brown'
        assert result.employees.employee1.office_location == 'San Jose, CA'

        assert result.employees.employee2.name == 'Linda Wilson'
        assert result.employees.employee2.office_location == 'Milpitas, CA'

    @pytest.mark.parametrize(
        "filename,new_name,prefix,postfix,new_extension,expected_result",
        [
            ('', 'blab_blab', 'blab_blab', 'blab_blab', 'blab_blab', ''),
            ('.', 'blab_blab', 'blab_blab', 'blab_blab', 'blab_blab', '.'),
            ('abc/file1.txt', 'file2.py', '', '', '', 'abc/file2.py'),
            ('abc/file1.txt', '', '', '', 'bat', 'abc/file1.bat'),
            ('abc/file1.txt', '', 'test_', '', 'bat', 'abc/test_file1.bat'),
            ('abc/test_file1.txt', '', 'test_', '', 'bat', 'abc/test_file1.bat'),
            ('abc/file1.txt', '', 'test_', '_xyz', 'bat', 'abc/test_file1_xyz.bat'),
            ('abc/test_file1.txt', '', 'test_', '_xyz', 'bat', 'abc/test_file1_xyz.bat'),
            ('abc/test_file1_xyz.txt', '', 'test_', '_xyz', 'bat', 'abc/test_file1_xyz.bat'),
        ]
    )
    def test_get_new_filename(self, filename, new_name, prefix, postfix,
                              new_extension, expected_result):
        result = File.get_new_filename(filename, new_name=new_name,
                                       prefix=prefix, postfix=postfix,
                                       new_extension=new_extension)

        if Misc.is_window_os():
            expected_result_for_win_os = expected_result.replace('/', '\\')
            assert result == expected_result_for_win_os
        else:
            assert result == expected_result
