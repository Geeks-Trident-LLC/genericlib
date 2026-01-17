"""
Unit tests for the `genericlib.utils` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/utils/test_utils.py
    or
    $ python -m pytest tests/unit/utils/test_utils.py
"""


import pytest   # noqa

from genericlib import Printer
from genericlib import File
from genericlib import get_data_as_tabular

TEST_DATA = File.get_result_from_yaml_file(
    '../data/utils_data.yaml',
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
