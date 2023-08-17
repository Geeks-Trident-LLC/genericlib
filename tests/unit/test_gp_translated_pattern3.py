import pytest           # noqa

from genericlib.gp import TranslatedDigitPattern
from genericlib.gp import TranslatedDigitsPattern

from genericlib.gp import TranslatedLetterPattern
from genericlib.gp import TranslatedLettersPattern

from genericlib.gp import TranslatedAlphabetNumericPattern

from genericlib.gp import TranslatedSymbolPattern
from genericlib.gp import TranslatedSymbolsPattern
from genericlib.gp import TranslatedSymbolsGroupPattern
from genericlib.gp import TranslatedGraphPattern

from genericlib.gp import TranslatedWordPattern
from genericlib.gp import TranslatedWordsPattern


class TestTranslatedSymbolPattern:
    """Test class for TranslatedSymbolPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('a', ''),
            ('1.', ''),
            ('@', '[\\x21-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\x7e]'),
            ('\\', '[\\x21-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\x7e]'),
        ]
    )
    def test_symbol_pattern(self, data, expected_pattern):
        node = TranslatedSymbolPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('@', TranslatedLetterPattern('a'), r'[\x21-\x7e]'),
            ('.', TranslatedLettersPattern('ab'), r'\S+'),
            ('+', TranslatedDigitPattern('1'), r'[\x21-\x7e]'),
            ('*', TranslatedDigitsPattern('42'), r'\S+'),
            ('{', TranslatedAlphabetNumericPattern('4'), r'[\x21-\x7e]'),
            ('}', TranslatedWordPattern('4'), r'\S+'),
            ('=', TranslatedWordsPattern('4'), r'\S+( \S+)*'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedSymbolPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedSymbolsPattern:
    """Test class for TranslatedSymbolsPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('a', ''),
            ('1.', ''),
            ('@', '[\\x21-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\x7e]+'),
            ('+-', '[\\x21-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\x7e]+'),
        ]
    )
    def test_symbols_pattern(self, data, expected_pattern):
        node = TranslatedSymbolsPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('@', TranslatedLetterPattern('a'), r'\S+'),
            ('.', TranslatedLettersPattern('ab'), r'\S+'),
            ('+', TranslatedDigitPattern('1'), r'\S+'),
            ('*', TranslatedDigitsPattern('42'), r'\S+'),
            ('{', TranslatedAlphabetNumericPattern('4'), r'\S+'),
            ('}', TranslatedWordPattern('4'), r'\S+'),
            ('=', TranslatedWordsPattern('4'), r'\S+( \S+)*'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedSymbolsPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern
        assert recommended_pat == expected_pattern


class TestTranslatedSymbolsGroupPattern:
    """Test class for TranslatedSymbolsGroupPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('a', ''),
            ('1.', ''),
            ('++ --', r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+( [\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+)+'),
            ('+- +-  +---', r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+( +[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+)+'),
        ]
    )
    def test_symbols_group_pattern(self, data, expected_pattern):
        node = TranslatedSymbolsGroupPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('-- --', TranslatedLetterPattern('a'), r'\S+( \S+)*'),
            ('.. ..', TranslatedLettersPattern('ab'), r'\S+( \S+)*'),
            ('++ ++', TranslatedDigitPattern('1'), r'\S+( \S+)*'),
            ('** **', TranslatedDigitsPattern('42'), r'\S+( \S+)*'),
            ('{{ {{', TranslatedAlphabetNumericPattern('4'), r'\S+( \S+)*'),
            ('}} }}', TranslatedWordPattern('4'), r'\S+( \S+)*'),
            ('== ==', TranslatedWordsPattern('4 5'), r'\S+( \S+)+'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedSymbolsGroupPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedGraphPattern:
    """Test class for TranslatedGraphPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('aa', ''),
            ('1', r'[\x21-\x7e]'),
            ('+', r'[\x21-\x7e]'),
            ('a', r'[\x21-\x7e]'),
        ]
    )
    def test_graph_pattern(self, data, expected_pattern):
        node = TranslatedGraphPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    # @pytest.mark.parametrize(
    #     "data,other,expected_pattern",
    #     [
    #         ('-', TranslatedLetterPattern('a'), r'[\x21-\x7e]'),
    #         ('.', TranslatedLettersPattern('ab'), r'[\x21-\x7e]+'),
    #         ('+', TranslatedDigitPattern('1'), r'[\x21-\x7e]'),
    #         ('*', TranslatedDigitsPattern('42'), r'[\x21-\x7e]+'),
    #         ('a', TranslatedAlphabetNumericPattern('4'), r'[\x21-\x7e]'),
    #         ('}', TranslatedWordPattern('4'), r'[\x21-\x7e]+'),
    #         ('=', TranslatedWordsPattern('4 5'), r'[\x21-\x7e]+( [\x21-\x7e]+)*'),
    #     ]
    # )
    # def test_recommend_pattern(self, data, other, expected_pattern):
    #     node = TranslatedGraphPattern(data)
    #     recommended_pat_obj = node.recommend(other)
    #     recommended_pat = recommended_pat_obj.pattern
    #
    #     assert recommended_pat == expected_pattern
