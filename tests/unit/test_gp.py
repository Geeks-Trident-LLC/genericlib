# import re

import pytest
from genericlib.gp import CommonPhrase

from genericlib.gp import TranslatedPattern

from genericlib.gp import TranslatedDigitPattern
from genericlib.gp import TranslatedDigitsPattern

from genericlib.gp import TranslatedNumberPattern
from genericlib.gp import TranslatedMixedNumberPattern

from genericlib.gp import TranslatedLetterPattern
from genericlib.gp import TranslatedLettersPattern

from genericlib.gp import TranslatedAlphabetNumericPattern

from genericlib.gp import TranslatedWordPattern
from genericlib.gp import TranslatedWordsPattern
from genericlib.gp import TranslatedMixedWordPattern
from genericlib.gp import TranslatedMixedWordsPattern
from genericlib.gp import TranslatedMixedFlexWordsPattern

from genericlib.gp import TranslatedNonWhiteSpace
from genericlib.gp import TranslatedNonWhiteSpaces
from genericlib.gp import TranslatedNonWhiteSpaceGroup
from genericlib.gp import TranslatedFlexNonWhiteSpaceGroup


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
