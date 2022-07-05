import pytest

from genericlib import Printer
from genericlib import File
from genericlib import Misc
from genericlib import MiscOutput
from genericlib import get_data_as_tabular

TEST_DATA = File.get_result_from_yaml_file(
    'data/utils_data.yaml',
    base_dir=File.get_dir(__file__),
    dot_datatype=True,
    var_substitution=True
)


class TestPrinter:
    @pytest.mark.parametrize(
        "data,width,header,footer,failure_msg,expected_result",
        [
            (
                TEST_DATA.printer.case1.data,
                TEST_DATA.printer.case1.width,
                TEST_DATA.printer.case1.header,
                TEST_DATA.printer.case1.footer,
                TEST_DATA.printer.case1.failure_msg,
                TEST_DATA.printer.case1.expected_result
            ),
            (
                TEST_DATA.printer.case2.data,
                TEST_DATA.printer.case2.width,
                TEST_DATA.printer.case2.header,
                TEST_DATA.printer.case2.footer,
                TEST_DATA.printer.case2.failure_msg,
                TEST_DATA.printer.case2.expected_result
            ),
            (
                TEST_DATA.printer.case3.data,
                TEST_DATA.printer.case3.width,
                TEST_DATA.printer.case3.header,
                TEST_DATA.printer.case3.footer,
                TEST_DATA.printer.case3.failure_msg,
                TEST_DATA.printer.case3.expected_result
            ),
            (
                TEST_DATA.printer.case4.data,
                TEST_DATA.printer.case4.width,
                TEST_DATA.printer.case4.header,
                TEST_DATA.printer.case4.footer,
                TEST_DATA.printer.case4.failure_msg,
                TEST_DATA.printer.case4.expected_result
            ),
            (
                TEST_DATA.printer.case5.data,
                TEST_DATA.printer.case5.width,
                TEST_DATA.printer.case5.header,
                TEST_DATA.printer.case5.footer,
                TEST_DATA.printer.case5.failure_msg,
                TEST_DATA.printer.case5.expected_result
            ),
            (
                TEST_DATA.printer.case6.data,
                TEST_DATA.printer.case6.width,
                TEST_DATA.printer.case6.header,
                TEST_DATA.printer.case6.footer,
                TEST_DATA.printer.case6.failure_msg,
                TEST_DATA.printer.case6.expected_result
            ),
            (
                TEST_DATA.printer.case7.data,
                TEST_DATA.printer.case7.width,
                TEST_DATA.printer.case7.header,
                TEST_DATA.printer.case7.footer,
                TEST_DATA.printer.case7.failure_msg,
                TEST_DATA.printer.case7.expected_result
            ),
            (
                TEST_DATA.printer.case8.data,
                TEST_DATA.printer.case8.width,
                TEST_DATA.printer.case8.header,
                TEST_DATA.printer.case8.footer,
                TEST_DATA.printer.case8.failure_msg,
                TEST_DATA.printer.case8.expected_result
            )
        ]
    )
    def test_get_method(self, data, width, header, footer, failure_msg, expected_result):
        result = Printer.get(data, width=width, header=header,
                             footer=footer, failure_msg=failure_msg)
        assert result == expected_result


class TestMisc:

    def test_is_dict(self):
        obj = dict()
        result = Misc.is_dict(obj)
        assert result is True

    def test_is_mapping(self):
        obj = dict()
        result = Misc.is_mapping(obj)
        assert result is True

    def test_is_list(self):
        obj = list()
        result = Misc.is_list(obj)
        assert result is True

    def test_is_mutable_sequence(self):
        for cls in [list, tuple, set]:
            obj = cls()
            result = Misc.is_mutable_sequence(obj)
            assert result is True

    def test_is_sequence(self):
        for cls in [list, tuple, str]:
            obj = cls()
            result = Misc.is_sequence(obj)
            assert result is True

    @pytest.mark.parametrize(
        "data,return_type,expected_result",
        [
            (1, None, (True, 1)),
            ('1', None, (True, 1)),
            ('1.0', None, (True, 1.0)),
            (' .1', None, (True, 0.1)),
            (False, None, (True, False)),
            ('true', None, (True, True)),
            ('  tRue  ', None, (True, True)),
            ('  tRue  ', int, (True, 1)),
            ('  faLse  ', float, (True, 0.0)),
            ('  2.3  ', float, (True, 2.3)),
            ('  2.3  ', int, (True, 2)),
            ('  2.3  ', bool, (True, 1)),
            ('1.0 2.0', None, (False, '1.0 2.0')),

        ]
    )
    def test_try_to_get_number(self, data, return_type, expected_result):
        result = Misc.try_to_get_number(data, return_type=return_type)
        assert result == expected_result

    @pytest.mark.parametrize(
        "data,expected_result",
        [
            (1, True),
            ('1', True),
            (' 1.0 ', False),
            ('.0', False),

        ]
    )
    def test_is_integer(self, data, expected_result):
        result = Misc.is_integer(data)
        assert result == expected_result

    @pytest.mark.parametrize(
        "data,expected_result",
        [
            (1, True),
            (1.1, True),
            ('1', True),
            (' 1.0 ', True),
            ('.0', True),
            ('1.0 2.0', False)

        ]
    )
    def test_is_float(self, data, expected_result):
        result = Misc.is_float(data)
        assert result == expected_result

    @pytest.mark.parametrize(
        "data,expected_result",
        [
            (True, True),
            (False, True),
            (1, True),
            (0, True),
            (1.0, True),
            (0.0, True),
            (' true ', True),
            (' false ', True),
            (0.1, False),
            ('0', False),

        ]
    )
    def test_is_boolean(self, data, expected_result):
        result = Misc.is_boolean(data)
        assert result == expected_result

    @pytest.mark.parametrize(
        "data,expected_result",
        [
            (True, True),
            (False, True),
            (1, True),
            (0, True),
            (1.0, True),
            (0.0, True),
            (' true ', True),
            (' false ', True),
            (0.1, True),
            ('0', True),
            ('0 0', False)

        ]
    )
    def test_is_number(self, data, expected_result):
        result = Misc.is_number(data)
        assert result == expected_result

    def test_is_class(self):
        assert Misc.is_class(int) is True
        assert Misc.is_class(File) is True
        assert Misc.is_class(Misc.is_number) is False

    def test_is_callable(self):
        assert Misc.is_callable(print) is True
        assert Misc.is_callable(1) is False

    def test_is_iterator(self):
        assert Misc.is_iterator(iter(list())) is True

    def test_is_generator(self):
        def foo():
            yield 1

        assert Misc.is_generator(foo()) is True

    def test_is_iterable(self):
        assert Misc.is_iterable([]) is True
        assert Misc.is_iterable(tuple()) is True
        assert Misc.is_iterable('abc') is True

    def test_join_string(self):
        assert Misc.join_string('Jack', 'Brown') == 'JackBrown'
        assert Misc.join_string('Jack', 'Brown', sep=' ') == 'Jack Brown'
        assert Misc.join_string('Jack', 'Brown', separator='.') == 'Jack.Brown'


class TestMiscOutput:

    def test_execute_shell_command(self):
        cmdline = 'dir' if Misc.is_window_os() else 'ls'
        result = MiscOutput.execute_shell_command(cmdline)
        assert result.exit_code == 0
        assert result.is_success is True


@pytest.mark.parametrize(
    "data,columns,justify,missing,expected_result",
    [
        (
            TEST_DATA.tabular.case1.data,
            TEST_DATA.tabular.case1.columns,
            TEST_DATA.tabular.case1.justify,
            TEST_DATA.tabular.case1.missing,
            TEST_DATA.tabular.case1.expected_result
        ),
        (
            TEST_DATA.tabular.case2.data,
            TEST_DATA.tabular.case2.columns,
            TEST_DATA.tabular.case2.justify,
            TEST_DATA.tabular.case2.missing,
            TEST_DATA.tabular.case2.expected_result
        ),
        (
            TEST_DATA.tabular.case3.data,
            TEST_DATA.tabular.case3.columns,
            TEST_DATA.tabular.case3.justify,
            TEST_DATA.tabular.case3.missing,
            TEST_DATA.tabular.case3.expected_result
        ),
        (
            TEST_DATA.tabular.case4.data,
            TEST_DATA.tabular.case4.columns,
            TEST_DATA.tabular.case4.justify,
            TEST_DATA.tabular.case4.missing,
            TEST_DATA.tabular.case4.expected_result
        ),
        (
            TEST_DATA.tabular.case5.data,
            TEST_DATA.tabular.case5.columns,
            TEST_DATA.tabular.case5.justify,
            TEST_DATA.tabular.case5.missing,
            TEST_DATA.tabular.case5.expected_result
        ),
        (
            TEST_DATA.tabular.case6.data,
            TEST_DATA.tabular.case6.columns,
            TEST_DATA.tabular.case6.justify,
            TEST_DATA.tabular.case6.missing,
            TEST_DATA.tabular.case6.expected_result
        ),
        (
            TEST_DATA.tabular.case7.data,
            TEST_DATA.tabular.case7.columns,
            TEST_DATA.tabular.case7.justify,
            TEST_DATA.tabular.case7.missing,
            TEST_DATA.tabular.case7.expected_result
        ),
        (
            TEST_DATA.tabular.case8.data,
            TEST_DATA.tabular.case8.columns,
            TEST_DATA.tabular.case8.justify,
            TEST_DATA.tabular.case8.missing,
            TEST_DATA.tabular.case8.expected_result
        ),
    ]
)
def test_get_data_as_tabular(data, columns, justify, missing, expected_result):
    result = get_data_as_tabular(data, columns=columns, justify=justify, missing=missing)
    assert result == expected_result
