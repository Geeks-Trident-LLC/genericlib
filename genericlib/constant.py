"""Module containing the logic for constant definition"""

import re
from enum import IntFlag


class ICSValue:
    """Treating value as ignore case and ignore space during evaluating
    string equality"""
    def __init__(self, value, equality='', stripped=False):
        self.value = str(value)
        self.equality = equality
        self.stripped = stripped

    def __eq__(self, other):
        value1 = self.value.lower()

        if isinstance(other, self.__class__):
            value2 = other.value.lower()
        else:
            value2 = str(other).lower()

        value1 = re.sub(' +', ' ', value1)
        value2 = re.sub(' +', ' ', value2)

        if self.stripped:
            value1 = value1.strip()
            value2 = value2.strip()

        if self.equality:
            if isinstance(self.equality, (list, tuple)):
                is_equal = True
                for item in self.equality:
                    item = str(item)
                    try:
                        is_equal = bool(re.match(item, value2, re.I))
                    except Exception as ex:     # noqa
                        item = re.sub(' +', ' ', item.lower())
                        is_equal &= item == value2
                return is_equal
            else:
                pattern = str(self.equality)
                try:
                    is_equal = bool(re.match(pattern, value2, re.I))
                except Exception as ex:     # noqa
                    equality = re.sub(' +', ' ', str(self.equality).lower())
                    is_equal = equality == value2
                return is_equal
        else:
            chk = value1 == value2
        return chk

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return self.value


class ICSStripValue(ICSValue):
    """Treating value as ignore case, ignore space, and strip during evaluating
    string equality"""
    def __init__(self, value, equality=''):
        super().__init__(value, equality=equality, stripped=True)


class ECODE(IntFlag):
    SUCCESS = 0
    BAD = 1
    PASSED = SUCCESS
    FAILED = BAD


class STRING:
    EMPTY = ''
    NEWLINE = '\n'
    LINEFEED = '\n'
    CARRIAGE_RETURN = '\r'
    TRUE = 'True'
    FALSE = 'False'
    FORWARD_FLASH = '/'
    EQUAL_SYMBOL = '='
    SPACE_CHAR = ' '
    DOUBLE_SPACES = '  '
    DOT_CHAR = '.'

    CMDLINE = 'cmdline'
    CMDLINES = 'cmdlines'
    NAME = 'name'
    DESCRIPTION = 'description'
    LOGIN = 'login'
    SUCCESS = 'success'
    WARNING = 'warning'
    ERROR = 'error'
    SUBMIT = 'submit'

    START = 'start'
    END = 'end'
    MIDDLE = 'middle'
    FIRST = 'first'
    LAST = 'last'

    EXECUTION = 'execution'
    BATCH = 'batch'
    TEST_SCRIPT = 'test_script'
    STATIC = 'static'
    HIDDEN_INPUT_FIELD = 'hidden_input_field'
    TEMPLATE_RESULT = 'template_result'
    SCRIPT_RESULT = 'script_result'
    SEARCHED_TEMPLATE = 'searched_template'
    BUILT_TEMPLATE = 'built_template'
    BUILT_SCRIPT = 'built_script'
    SAVED_TEMPLATE = 'saved_template'
    ITERATIVE_TEST = 'iterative_test'
    ITERATIVE_RESULT = 'iterative_result'
    BATCH_ACTION = 'batch_action'
    BATCH_RESULT = 'batch_result'
    ROBOT = 'robot'
    PY = 'py'
    TEST_ = 'test_'

    UNSUPPORTED_PARSING = 'unsupported parsing'


STR = STRING


class LSSTRING:
    TRUE = ICSStripValue('true')
    FALSE = ICSStripValue('false')


class TEXT:
    ALPHABET_NUMERIC = 'alphabet_numeric'

    DIGIT = 'digit'
    DIGITS = 'digits'

    GRAPH = 'graph'

    LETTER = 'letter'
    LETTERS = 'letters'

    NUMBER = 'number'

    MIXED_NUMBER = 'mixed_number'
    MIXED_WORD = 'mixed_word'
    MIXED_WORDS = 'mixed_words'

    NON_WHITESPACE = 'non_whitespace'
    NON_WHITESPACES = 'non_whitespaces'
    NON_WHITESPACES_GROUP = 'non_whitespace_group'

    SYMBOL = 'symbol'
    SYMBOLS = 'symbols'
    SYMBOLS_GROUP = 'symbols_group'

    WORD = 'word'
    WORDS = 'words'


