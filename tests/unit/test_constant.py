import pytest   # noqa

from genericlib import ECODE
from genericlib import ICSValue
from genericlib import ICSStripValue
from genericlib import STRING
from genericlib import TEXT


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
            (STRING.FORWARD_FLASH, '/'),
            (STRING.EQUAL_SYMBOL, '='),
            (STRING.SPACE_CHAR, ' '),
            (STRING.DOT_CHAR, '.'),

            (STRING.CMDLINE, 'cmdline'),
            (STRING.CMDLINES, 'cmdlines'),
            (STRING.NAME, 'name'),
            (STRING.DESCRIPTION, 'description'),
            (STRING.LOGIN, 'login'),
            (STRING.SUCCESS, 'success'),
            (STRING.WARNING, 'warning'),
            (STRING.ERROR, 'error'),
            (STRING.SUBMIT, 'submit'),
            (STRING.EXECUTION, 'execution'),
            (STRING.BATCH, 'batch'),
            (STRING.STATIC, 'static'),
            (STRING.HIDDEN_INPUT_FIELD, 'hidden_input_field'),
            (STRING.TEMPLATE_RESULT, 'template_result'),
            (STRING.SCRIPT_RESULT, 'script_result'),
            (STRING.SEARCHED_TEMPLATE, 'searched_template'),
            (STRING.BUILT_TEMPLATE, 'built_template'),
            (STRING.BUILT_SCRIPT, 'built_script'),
            (STRING.SAVED_TEMPLATE, 'saved_template'),
            (STRING.ITERATIVE_TEST, 'iterative_test'),
            (STRING.ITERATIVE_RESULT, 'iterative_result'),
            (STRING.BATCH_ACTION, 'batch_action'),
            (STRING.ROBOT, 'robot'),
            (STRING.PY, 'py'),
        ]
    )
    def test_constant_string(self, constant_string, expected_result):
        assert constant_string == expected_result


class TestText:

    @pytest.mark.parametrize(
        "constant_text,expected_result",
        [
            (TEXT.ALPHABET_NUMERIC, 'alphabet_numeric'),

            (TEXT.DIGIT, 'digit'),
            (TEXT.DIGITS, 'digits'),

            (TEXT.GRAPH, 'graph'),

            (TEXT.LETTER, 'letter'),
            (TEXT.LETTERS, 'letters'),

            (TEXT.NUMBER, 'number'),

            (TEXT.MIXED_NUMBER, 'mixed_number'),
            (TEXT.MIXED_WORD, 'mixed_word'),
            (TEXT.MIXED_WORDS, 'mixed_words'),

            (TEXT.NON_WHITESPACE, 'non_whitespace'),
            (TEXT.NON_WHITESPACES_GROUP, 'non_whitespace_group'),
            (TEXT.NON_WHITESPACES, 'non_whitespaces'),

            (TEXT.WORD, 'word'),
            (TEXT.WORDS, 'words'),
        ]
    )
    def test_constant_text(self, constant_text, expected_result):
        assert constant_text == expected_result
