import pytest

from genericlib import ECODE
from genericlib import ICSValue
from genericlib import ICSStripValue
from genericlib import STRING


class TestICSValue:

    @pytest.mark.parametrize(
        "data,equality,stripped,expected_result",
        [
            ('', '', False, ''),
            ('True', '', False, 'true'),
            ('tRUE', '', False, 'true'),
            ('True ', '', False, 'true '),
            ('True ', '', True, 'true'),
            ('  True ', '', False, '  true '),
            ('  True ', '', True, 'true'),
            ('robotframework', r'(rf|robotframework)$', True, 'robotframework'),
            ('robotframework', r'(rf|robotframework)$', True, 'rf')

        ]
    )
    def test_ignore_case_strip_value(self, data, equality, stripped, expected_result):
        result = ICSValue(data, equality=equality, stripped=stripped)
        assert result == expected_result


class TestICSStripValue:

    @pytest.mark.parametrize(
        "data,equality,expected_result",
        [
            ('', '', ''),
            ('True', '', 'true'),
            ('  True ', '', 'true'),
            ('robotframework', r'(rf|robotframework)$', 'robotframework'),
            ('robotframework', r'(rf|robotframework)$', 'rf'),

        ]
    )
    def test_ignore_case_strip_value(self, data, equality, expected_result):
        result = ICSStripValue(data, equality=equality)
        assert result == expected_result


class TestECode:

    @pytest.mark.parametrize(
        "constant_number,expected_result",
        [
            (ECODE.SUCCESS, 0),
            (ECODE.BAD, 1),
            (ECODE.PASSED, 0),
            (ECODE.FAILED, 1)
        ]
    )
    def test_exit_code(self, constant_number, expected_result):
        assert constant_number == expected_result


class TestString:

    @pytest.mark.parametrize(
        "constant_string,expected_result",
        [
            (STRING.EMPTY, ''),
            (STRING.TRUE, 'True'),
            (STRING.FALSE, 'False'),
            (STRING.NEWLINE, '\n'),
            (STRING.LINEFEED, '\n'),
            (STRING.CARRIAGE_RETURN, '\r'),
            (STRING.CMDLINE, 'cmdline'),
            (STRING.CMDLINES, 'cmdlines'),
            (STRING.NAME, 'name'),
            (STRING.DESCRIPTION, 'description'),
            (STRING.LOGIN, 'login'),
            (STRING.SUCCESS, 'success'),
            (STRING.WARNING, 'warning'),
            (STRING.ERROR, 'error'),
            (STRING.SUBMIT, 'submit')
        ]
    )
    def test_constant_string(self, constant_string, expected_result):
        assert constant_string == expected_result
