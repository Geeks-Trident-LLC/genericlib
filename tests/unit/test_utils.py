import pytest   # noqa

from genericlib import Printer
from genericlib import File
from genericlib import Misc
from genericlib import MiscOutput
from genericlib import MiscObject
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
                TEST_DATA.printer.case1.data,               # noqa
                TEST_DATA.printer.case1.width,              # noqa
                TEST_DATA.printer.case1.header,             # noqa
                TEST_DATA.printer.case1.footer,             # noqa
                TEST_DATA.printer.case1.failure_msg,        # noqa
                TEST_DATA.printer.case1.expected_result     # noqa
            ),
            (
                TEST_DATA.printer.case2.data,               # noqa
                TEST_DATA.printer.case2.width,              # noqa
                TEST_DATA.printer.case2.header,             # noqa
                TEST_DATA.printer.case2.footer,             # noqa
                TEST_DATA.printer.case2.failure_msg,        # noqa
                TEST_DATA.printer.case2.expected_result     # noqa
            ),
            (
                TEST_DATA.printer.case3.data,               # noqa
                TEST_DATA.printer.case3.width,              # noqa
                TEST_DATA.printer.case3.header,             # noqa
                TEST_DATA.printer.case3.footer,             # noqa
                TEST_DATA.printer.case3.failure_msg,        # noqa
                TEST_DATA.printer.case3.expected_result     # noqa
            ),
            (
                TEST_DATA.printer.case4.data,               # noqa
                TEST_DATA.printer.case4.width,              # noqa
                TEST_DATA.printer.case4.header,             # noqa
                TEST_DATA.printer.case4.footer,             # noqa
                TEST_DATA.printer.case4.failure_msg,        # noqa
                TEST_DATA.printer.case4.expected_result     # noqa
            ),
            (
                TEST_DATA.printer.case5.data,               # noqa
                TEST_DATA.printer.case5.width,              # noqa
                TEST_DATA.printer.case5.header,             # noqa
                TEST_DATA.printer.case5.footer,             # noqa
                TEST_DATA.printer.case5.failure_msg,        # noqa
                TEST_DATA.printer.case5.expected_result     # noqa
            ),
            (
                TEST_DATA.printer.case6.data,               # noqa
                TEST_DATA.printer.case6.width,              # noqa
                TEST_DATA.printer.case6.header,             # noqa
                TEST_DATA.printer.case6.footer,             # noqa
                TEST_DATA.printer.case6.failure_msg,        # noqa
                TEST_DATA.printer.case6.expected_result     # noqa
            ),
            (
                TEST_DATA.printer.case7.data,               # noqa
                TEST_DATA.printer.case7.width,              # noqa
                TEST_DATA.printer.case7.header,             # noqa
                TEST_DATA.printer.case7.footer,             # noqa
                TEST_DATA.printer.case7.failure_msg,        # noqa
                TEST_DATA.printer.case7.expected_result     # noqa
            ),
            (
                TEST_DATA.printer.case8.data,               # noqa
                TEST_DATA.printer.case8.width,              # noqa
                TEST_DATA.printer.case8.header,             # noqa
                TEST_DATA.printer.case8.footer,             # noqa
                TEST_DATA.printer.case8.failure_msg,        # noqa
                TEST_DATA.printer.case8.expected_result     # noqa
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
        for cls in [list]:
            obj = cls()
            result = Misc.is_mutable_sequence(obj)
            assert result is True

    def test_is_sequence(self):
        for cls in [list, tuple, str]:
            obj = cls()
            result = Misc.is_sequence(obj)
            assert result is True

    def test_is_class(self):
        assert Misc.is_class(int) is True
        assert Misc.is_class(File) is True
        assert Misc.is_class(int.is_integer) is False

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
        assert Misc.join_string('Jack', 'Brown') == 'JackBrown'                 # noqa
        assert Misc.join_string('Jack', 'Brown', sep=' ') == 'Jack Brown'       # noqa
        assert Misc.join_string('Jack', 'Brown', separator='.') == 'Jack.Brown' # noqa

    def test_get_instance_class_name(self):
        class Foo:
            pass

        class Bar:
            pass

        class FooBar(Foo, Bar):
            pass

        foo = Foo()
        bar = Bar()
        foobar = FooBar()

        assert Misc.get_instance_class_name(foo) == 'Foo'
        assert Misc.get_instance_class_name(bar) == 'Bar'
        assert Misc.get_instance_class_name(foobar) == 'FooBar'


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
            TEST_DATA.tabular.case1.data,               # noqa
            TEST_DATA.tabular.case1.columns,            # noqa
            TEST_DATA.tabular.case1.justify,            # noqa
            TEST_DATA.tabular.case1.missing,            # noqa
            TEST_DATA.tabular.case1.expected_result     # noqa
        ),
        (
            TEST_DATA.tabular.case2.data,               # noqa
            TEST_DATA.tabular.case2.columns,            # noqa
            TEST_DATA.tabular.case2.justify,            # noqa
            TEST_DATA.tabular.case2.missing,            # noqa
            TEST_DATA.tabular.case2.expected_result     # noqa
        ),
        (
            TEST_DATA.tabular.case3.data,               # noqa
            TEST_DATA.tabular.case3.columns,            # noqa
            TEST_DATA.tabular.case3.justify,            # noqa
            TEST_DATA.tabular.case3.missing,            # noqa
            TEST_DATA.tabular.case3.expected_result     # noqa
        ),
        (
            TEST_DATA.tabular.case4.data,               # noqa
            TEST_DATA.tabular.case4.columns,            # noqa
            TEST_DATA.tabular.case4.justify,            # noqa
            TEST_DATA.tabular.case4.missing,            # noqa
            TEST_DATA.tabular.case4.expected_result     # noqa
        ),
        (
            TEST_DATA.tabular.case5.data,               # noqa
            TEST_DATA.tabular.case5.columns,            # noqa
            TEST_DATA.tabular.case5.justify,            # noqa
            TEST_DATA.tabular.case5.missing,            # noqa
            TEST_DATA.tabular.case5.expected_result     # noqa
        ),
        (
            TEST_DATA.tabular.case6.data,               # noqa
            TEST_DATA.tabular.case6.columns,            # noqa
            TEST_DATA.tabular.case6.justify,            # noqa
            TEST_DATA.tabular.case6.missing,            # noqa
            TEST_DATA.tabular.case6.expected_result     # noqa
        ),
        (
            TEST_DATA.tabular.case7.data,               # noqa
            TEST_DATA.tabular.case7.columns,            # noqa
            TEST_DATA.tabular.case7.justify,            # noqa
            TEST_DATA.tabular.case7.missing,            # noqa
            TEST_DATA.tabular.case7.expected_result     # noqa
        ),
        (
            TEST_DATA.tabular.case8.data,               # noqa
            TEST_DATA.tabular.case8.columns,            # noqa
            TEST_DATA.tabular.case8.justify,            # noqa
            TEST_DATA.tabular.case8.missing,            # noqa
            TEST_DATA.tabular.case8.expected_result     # noqa
        ),
    ]
)
def test_get_data_as_tabular(data, columns, justify, missing, expected_result):
    result = get_data_as_tabular(data, columns=columns, justify=justify, missing=missing)
    assert result == expected_result


class TestMiscObject:
    @pytest.mark.parametrize(
        "data,expected_result",
        [
            ([1, 2], [True, True]),
            ([dict(item1=1, item2=2), dict(item3=3, item4=4)], [True, True]),

        ]
    )
    def test_copy(self, data, expected_result):
        new_data = MiscObject.copy(data)
        equality_chk = new_data == data
        identity_chk = id(new_data) != id(data)
        result = [equality_chk, identity_chk]
        assert result == expected_result

    @pytest.mark.parametrize(
        "data,expected_result",
        [
            (
                [
                    {'key1': 'item 1', 'key2': '  item2  '},
                    {'key1': 'other item1', 'key2': ' other item 2'}
                ],
                [
                    {'key1': 'item 1', 'key2': 'item2'},
                    {'key1': 'other item1', 'key2': 'other item 2'}
                ]
            ),
        ]
    )
    def test_cleanup_list_of_dict(self, data, expected_result):
        result = MiscObject.cleanup_list_of_dict(data)
        assert result == expected_result
