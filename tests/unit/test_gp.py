# import re

import pytest           # noqa
from genericlib.gp import CommonPhrase

from genericlib.gp import TranslatedPattern

from genericlib.gp import TranslatedDigitPattern
from genericlib.gp import TranslatedDigitsPattern

from genericlib.gp import TranslatedNumberPattern
from genericlib.gp import TranslatedMixedNumberPattern

from genericlib.gp import TranslatedLetterPattern
from genericlib.gp import TranslatedLettersPattern

from genericlib.gp import TranslatedAlphabetNumericPattern

from genericlib.gp import TranslatedSymbolPattern
from genericlib.gp import TranslatedSymbolsPattern
from genericlib.gp import TranslatedSymbolsGroupPattern
from genericlib.gp import TranslatedGraphPattern

from genericlib.gp import TranslatedWordPattern
from genericlib.gp import TranslatedWordsPattern
from genericlib.gp import TranslatedMixedWordPattern
from genericlib.gp import TranslatedMixedWordsPattern

from genericlib.gp import TranslatedNonWhitespacePattern
from genericlib.gp import TranslatedNonWhitespacesPattern
from genericlib.gp import TranslatedNonWhitespacesGroupPattern


class TestCommonPhrase:
    """Test class for CommonPhrase."""

    @pytest.mark.parametrize(
        "data,is_generic,is_flex_space,expected_result",
        [
            ('', False, False, ''),
            (' ', False, False, ' '),
            ('   ', False, False, '   '),
            ('   ', False, True, ' +'),
            ('abc xyz', False, False, 'abc xyz'),
            ('abc   xyz', False, False, 'abc   xyz'),
            ('abc   xyz', False, True, 'abc +xyz'),
            ('  abc   xyz', False, True, ' +abc +xyz'),
            ('  abc   xyz  ', False, True, ' +abc +xyz +'),
            ('  (abc)   xyz  ', False, True, ' +\\(abc\\) +xyz +'),
            ('  (abc+)   xyz  ', False, True, ' +\\(abc\\+\\) +xyz +'),
            ('  (abc++)   x.yz  ', False, True, ' +\\(abc\\+\\+\\) +x\\.yz +'),
        ]
    )
    def test_common_phrase(self, data, is_generic, is_flex_space, expected_result):
        node = CommonPhrase(data, is_generic=is_generic, is_flex_space=is_flex_space)
        pattern = node.pattern
        assert pattern == expected_result


class TestTranslatedPattern:
    """Test class for TranslatedPattern."""

    @pytest.mark.parametrize(
        "data1,data2,expected_pattern",
        [
            ('5', '4', '[0-9]'),
            ('5', '44', '[0-9]+'),
            ('555', '4', '[0-9]+'),
            ('1.1', '4', '[0-9]*[.]?[0-9]+'),
            ('12', '4.1', '[0-9]*[.]?[0-9]+'),
            ('12.3', '4.1', '[0-9]*[.]?[0-9]+'),
            ('5', '+4.4', '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
        ]
    )
    def test_recommend_pattern(self, data1, data2, expected_pattern):

        method = TranslatedPattern.recommend_pattern_using_data
        recommended_pat_obj = method(data1, data2)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedDigitPattern:
    """Test class for TranslatedDigitPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('5', '[0-9]'),
            ('', ''),
            ('123', ''),
        ]
    )
    def test_digit_pattern(self, data, expected_pattern):
        node = TranslatedDigitPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('5', TranslatedDigitPattern('4'), '[0-9]'),
            ('5', TranslatedDigitsPattern('44'), '[0-9]+'),
            ('5', TranslatedNumberPattern('4.4'), '[0-9]*[.]?[0-9]+'),
            ('5', TranslatedMixedNumberPattern('4.4'), '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedDigitPattern(data)

        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedDigitsPattern:
    """Test class for TranslatedDigitsPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('5', '[0-9]+'),
            ('123', '[0-9]+'),
        ]
    )
    def test_digits_pattern(self, data, expected_pattern):
        node = TranslatedDigitsPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('5', TranslatedDigitPattern('4'), '[0-9]+'),
            ('5', TranslatedDigitsPattern('44'), '[0-9]+'),
            ('5', TranslatedNumberPattern('4.4'), '[0-9]*[.]?[0-9]+'),
            ('5', TranslatedMixedNumberPattern('4.4'), '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedDigitsPattern(data)

        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedNumberPattern:
    """Test class for TranslatedNumberPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('5', '[0-9]*[.]?[0-9]+'),
            ('.5', '[0-9]*[.]?[0-9]+'),
            ('0.5', '[0-9]*[.]?[0-9]+'),
            ('-0.5', ''),
        ]
    )
    def test_number_pattern(self, data, expected_pattern):
        node = TranslatedNumberPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('5.1', TranslatedDigitPattern('4'), '[0-9]*[.]?[0-9]+'),
            ('5.1', TranslatedDigitsPattern('44'), '[0-9]*[.]?[0-9]+'),
            ('5.1', TranslatedNumberPattern('4.4'), '[0-9]*[.]?[0-9]+'),
            ('5.1', TranslatedMixedNumberPattern('4.4'), '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedNumberPattern(data)

        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedMixedNumberPattern:
    """Test class for TranslatedNumberPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('5', '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
            ('.5', '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
            ('0.5', '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
            ('-0.5', '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
            ('+0.5', '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
            ('(0.5)', '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
        ]
    )
    def test_mixed_number_pattern(self, data, expected_pattern):
        node = TranslatedMixedNumberPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('+5.1', TranslatedDigitPattern('4'), '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
            ('-5.1', TranslatedDigitsPattern('44'), '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
            ('(5.1)', TranslatedNumberPattern('4.4'), '[\\(+-]?[0-9]*[.]?[0-9]+[)]?'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedMixedNumberPattern(data)

        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedLetterPattern:
    """Test class for TranslatedLetterPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('ab', ''),
            ('b', '[a-zA-Z]'),
        ]
    )
    def test_letter_pattern(self, data, expected_pattern):
        node = TranslatedLetterPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('a', TranslatedLetterPattern('a'), '[a-zA-Z]'),
            # ('a', TranslatedDigitPattern('4'), ''),
            # ('a', TranslatedDigitsPattern('4'), ''),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedLetterPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedLettersPattern:
    """Test class for TranslatedLettersPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('ab', '[a-zA-Z]+'),
            ('b', '[a-zA-Z]+'),
        ]
    )
    def test_letters_pattern(self, data, expected_pattern):
        node = TranslatedLettersPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('a', TranslatedLetterPattern('a'), '[a-zA-Z]+'),
            ('a', TranslatedLettersPattern('ac'), '[a-zA-Z]+'),
            # ('a', TranslatedDigitsPattern('4'), ''),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedLettersPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedAlphabetNumericPattern:
    """Test class for TranslatedAlphabetNumericPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('1', '[a-zA-Z0-9]'),
            ('b', '[a-zA-Z0-9]'),
        ]
    )
    def test_alphabet_numeric_pattern(self, data, expected_pattern):
        node = TranslatedAlphabetNumericPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('a', TranslatedLetterPattern('a'), '[a-zA-Z0-9]'),
            ('a', TranslatedAlphabetNumericPattern('1'), '[a-zA-Z0-9]'),
            # ('a', TranslatedDigitsPattern('4'), ''),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedAlphabetNumericPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedWordPattern:
    """Test class for TranslatedWordPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('1', '[a-zA-Z0-9]+'),
            ('ab', '[a-zA-Z0-9]+'),
        ]
    )
    def test_word_pattern(self, data, expected_pattern):
        node = TranslatedWordPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('a', TranslatedLetterPattern('a'), '[a-zA-Z0-9]+'),
            ('a', TranslatedLettersPattern('ab'), '[a-zA-Z0-9]+'),
            ('a', TranslatedDigitPattern('1'), '[a-zA-Z0-9]+'),
            ('a', TranslatedDigitsPattern('4'), '[a-zA-Z0-9]+'),
            ('a', TranslatedAlphabetNumericPattern('4'), '[a-zA-Z0-9]+'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedWordPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedWordsPattern:
    """Test class for TranslatedWordsPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('ab  xy', '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)+'),
            ('1 2', '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)+'),
            ('ab xy', '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)+'),
        ]
    )
    def test_words_pattern(self, data, expected_pattern):
        node = TranslatedWordsPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('a b', TranslatedLetterPattern('a'), '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)*'),
            ('a b', TranslatedLettersPattern('ab'), '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)*'),
            ('a b', TranslatedDigitPattern('1'), '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)*'),
            ('a b', TranslatedDigitsPattern('4'), '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)*'),
            ('a b', TranslatedAlphabetNumericPattern('4'), '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)*'),
            ('a b', TranslatedWordPattern('4'), '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)*'),
            ('a b', TranslatedWordsPattern('ab xy'), '[a-zA-Z0-9]+( +[a-zA-Z0-9]+)+'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedWordsPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedMixedWordPattern:
    """Test class for TranslatedMixedWordPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('ab xy', ''),
            ('1', '[\\x21-\\x7e]+'),
            ('abc', '[\\x21-\\x7e]+'),
            ('192.168.0.1', '[\\x21-\\x7e]+'),
            ('a::b', '[\\x21-\\x7e]+'),
        ]
    )
    def test_mixed_word_pattern(self, data, expected_pattern):
        node = TranslatedMixedWordPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('a', TranslatedLetterPattern('a'), '[\\x21-\\x7e]+'),
            ('a', TranslatedLettersPattern('ab'), '[\\x21-\\x7e]+'),
            ('a', TranslatedDigitPattern('1'), '[\\x21-\\x7e]+'),
            ('a', TranslatedDigitsPattern('4'), '[\\x21-\\x7e]+'),
            ('a', TranslatedAlphabetNumericPattern('4'), '[\\x21-\\x7e]+'),
            ('a', TranslatedWordPattern('4'), '[\\x21-\\x7e]+'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedMixedWordPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedMixedWordsPattern:
    """Test class for TranslatedMixedWordsPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('ab xy', '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)+'),
            ('1', '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
            ('abc', '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
            ('192.168.0.1', '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
            ('a::b', '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
        ]
    )
    def test_mixed_words_pattern(self, data, expected_pattern):
        node = TranslatedMixedWordsPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('a b', TranslatedLetterPattern('a'), '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
            ('a b', TranslatedLettersPattern('ab'), '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
            ('a b', TranslatedDigitPattern('1'), '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
            ('a b', TranslatedDigitsPattern('4'), '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
            ('a b', TranslatedAlphabetNumericPattern('4'), '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
            ('a b', TranslatedWordPattern('4'), '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedMixedWordsPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


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
            ('@', TranslatedLetterPattern('a'), '[\\x21-\\x7e]'),
            ('.', TranslatedLettersPattern('ab'), '[\\x21-\\x7e]+'),
            ('+', TranslatedDigitPattern('1'), '[\\x21-\\x7e]'),
            ('*', TranslatedDigitsPattern('42'), '[\\x21-\\x7e]+'),
            ('{', TranslatedAlphabetNumericPattern('4'), '[\\x21-\\x7e]'),
            ('}', TranslatedWordPattern('4'), '[\\x21-\\x7e]+'),
            ('=', TranslatedWordsPattern('4'), '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
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
            ('@', TranslatedLetterPattern('a'), '[\\x21-\\x7e]+'),
            ('.', TranslatedLettersPattern('ab'), '[\\x21-\\x7e]+'),
            ('+', TranslatedDigitPattern('1'), '[\\x21-\\x7e]+'),
            ('*', TranslatedDigitsPattern('42'), '[\\x21-\\x7e]+'),
            ('{', TranslatedAlphabetNumericPattern('4'), '[\\x21-\\x7e]+'),
            ('}', TranslatedWordPattern('4'), '[\\x21-\\x7e]+'),
            ('=', TranslatedWordsPattern('4'), '[\\x21-\\x7e]+( +[\\x21-\\x7e]+)*'),
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
            ('++ --', r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+( +[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+)+'),
            ('+- +- +---', r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+( +[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+)+'),
        ]
    )
    def test_symbols_group_pattern(self, data, expected_pattern):
        node = TranslatedSymbolsGroupPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('-- --', TranslatedLetterPattern('a'), r'[\x21-\x7e]+( +[\x21-\x7e]+)*'),
            ('.. ..', TranslatedLettersPattern('ab'), r'[\x21-\x7e]+( +[\x21-\x7e]+)*'),
            ('++ ++', TranslatedDigitPattern('1'), r'[\x21-\x7e]+( +[\x21-\x7e]+)*'),
            ('** **', TranslatedDigitsPattern('42'), r'[\x21-\x7e]+( +[\x21-\x7e]+)*'),
            ('{{ {{', TranslatedAlphabetNumericPattern('4'), r'[\x21-\x7e]+( +[\x21-\x7e]+)*'),
            ('}} }}', TranslatedWordPattern('4'), r'[\x21-\x7e]+( +[\x21-\x7e]+)*'),
            ('== ==', TranslatedWordsPattern('4 5'), r'[\x21-\x7e]+( +[\x21-\x7e]+)+'),
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

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('-', TranslatedLetterPattern('a'), r'[\x21-\x7e]'),
            ('.', TranslatedLettersPattern('ab'), r'[\x21-\x7e]+'),
            ('+', TranslatedDigitPattern('1'), r'[\x21-\x7e]'),
            ('*', TranslatedDigitsPattern('42'), r'[\x21-\x7e]+'),
            ('a', TranslatedAlphabetNumericPattern('4'), r'[\x21-\x7e]'),
            ('}', TranslatedWordPattern('4'), r'[\x21-\x7e]+'),
            ('=', TranslatedWordsPattern('4 5'), r'[\x21-\x7e]+( +[\x21-\x7e]+)*'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedGraphPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern


class TestTranslatedNonWhitespacePattern:
    """Test class for TranslatedNonWhitespacePattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('aa', ''),
            ('1', r'\S'),
            ('+', r'\S'),
            ('a', r'\S'),
        ]
    )
    def test_non_whitespace_pattern(self, data, expected_pattern):
        node = TranslatedNonWhitespacePattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('-', TranslatedLetterPattern('a'), r'\S'),
            ('.', TranslatedLettersPattern('ab'), r'\S+'),
            ('+', TranslatedDigitPattern('1'), r'\S'),
            ('*', TranslatedDigitsPattern('42'), r'\S+'),
            ('a', TranslatedAlphabetNumericPattern('4'), r'\S'),
            ('}', TranslatedWordPattern('4'), r'\S+'),
            ('=', TranslatedWordsPattern('4 5'), r'\S+( +\S+)*'),
            ('@', TranslatedNonWhitespacesPattern('4'), r'\S+'),
            ('#', TranslatedNonWhitespacesGroupPattern('4'), r'\S+( +\S+)*'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedNonWhitespacePattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern
        assert recommended_pat == expected_pattern


class TestTranslatedNonWhitespacesPattern:
    """Test class for TranslatedNonWhitespacesPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('aa', r'\S+'),
            ('1', r'\S+'),
            ('+', r'\S+'),
            ('a', r'\S+'),
        ]
    )
    def test_non_whitespace_pattern(self, data, expected_pattern):
        node = TranslatedNonWhitespacesPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('-', TranslatedLetterPattern('a'), r'\S+'),
            ('.', TranslatedLettersPattern('ab'), r'\S+'),
            ('+', TranslatedDigitPattern('1'), r'\S+'),
            ('*', TranslatedDigitsPattern('42'), r'\S+'),
            ('a', TranslatedAlphabetNumericPattern('4'), r'\S+'),
            ('}', TranslatedWordPattern('4'), r'\S+'),
            ('=', TranslatedWordsPattern('4 5'), r'\S+( +\S+)*'),
            ('@', TranslatedNonWhitespacesPattern('4'), r'\S+'),
            ('#', TranslatedNonWhitespacesGroupPattern('4'), r'\S+( +\S+)*'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedNonWhitespacesPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern
        assert recommended_pat == expected_pattern


class TestTranslatedNonWhitespacesGroupPattern:
    """Test class for TranslatedNonWhitespacesGroupPattern."""

    @pytest.mark.parametrize(
        "data,expected_pattern",
        [
            ('', ''),
            ('aa', r'\S+( +\S+)*'),
            ('1', r'\S+( +\S+)*'),
            ('+', r'\S+( +\S+)*'),
            ('a', r'\S+( +\S+)*'),
        ]
    )
    def test_non_whitespace_pattern(self, data, expected_pattern):
        node = TranslatedNonWhitespacesGroupPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('-', TranslatedLetterPattern('a'), r'\S+( +\S+)*'),
            ('.', TranslatedLettersPattern('ab'), r'\S+( +\S+)*'),
            ('+', TranslatedDigitPattern('1'), r'\S+( +\S+)*'),
            ('*', TranslatedDigitsPattern('42'), r'\S+( +\S+)*'),
            ('a', TranslatedAlphabetNumericPattern('4'), r'\S+( +\S+)*'),
            ('}', TranslatedWordPattern('4'), r'\S+( +\S+)*'),
            ('=', TranslatedWordsPattern('4 5'), r'\S+( +\S+)*'),
            ('@', TranslatedNonWhitespacesPattern('4'), r'\S+( +\S+)*'),
            ('#', TranslatedNonWhitespacesGroupPattern('4'), r'\S+( +\S+)*'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedNonWhitespacesGroupPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern
        assert recommended_pat == expected_pattern
