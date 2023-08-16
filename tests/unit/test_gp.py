import pytest           # noqa

from genericlib.gp import SnippetElement
from genericlib.gp import EditingSnippet

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


class TestSnippetElement:
    """Test class for SnippetElement"""
    @pytest.mark.parametrize(
        "snippet,trailing,expected_result",
        [
            ('mixed_word(var=v0, value=utun0:)', '', ['mixed_word', 'v0', 'utun0:', '']),
            ('mixed_word(var=v0, value=utun0:)', '  ', ['mixed_word', 'v0', 'utun0:', '  ']),
        ]
    )
    def test_creation(self, snippet, trailing, expected_result):
        node = SnippetElement(snippet, trailing=trailing)
        lst_of_attrs = [node.name, node.var_name, node.value, node.trailing]
        assert lst_of_attrs == expected_result

    @pytest.mark.parametrize(
        "snippet,expected_result",
        [
            ('mixed_word(var=v0, value=utun0:)', 'mixed_word(kvar=v0, value=utun0:)'),
            ('mixed_word(kvar=v0, value=utun1:)', 'mixed_word(kvar=v0, value=utun1:)'),
            ('mixed_word(cvar=v0, value=utun2:)', 'mixed_word(kvar=v0, value=utun2:)'),
        ]
    )
    def test_set_kept(self, snippet, expected_result):
        node = SnippetElement(snippet)
        node.set_kept()
        new_snippet = node.to_snippet()
        assert new_snippet == expected_result

    @pytest.mark.parametrize(
        "snippet,expected_result",
        [
            ('mixed_word(var=v0, value=utun0:)', 'mixed_word(cvar=v0, value=utun0:)'),
            ('mixed_word(kvar=v0, value=utun1:)', 'mixed_word(cvar=v0, value=utun1:)'),
            ('mixed_word(cvar=v0, value=utun2:)', 'mixed_word(cvar=v0, value=utun2:)'),
        ]
    )
    def test_set_captured(self, snippet, expected_result):
        node = SnippetElement(snippet)
        node.set_captured()
        new_snippet = node.to_snippet()
        assert new_snippet == expected_result

    @pytest.mark.parametrize(
        "snippet,expected_result",
        [
            ('mixed_word(var=v0, value=utun0:)', 'mixed_word(var=v0, value=utun0:)'),
            ('mixed_word(kvar=v0, value=utun1:)', 'mixed_word(kvar=v0, value=utun1:)'),
            ('mixed_word(cvar=v0, value=utun2:)', 'mixed_word(cvar=v0, value=utun2:)'),
        ]
    )
    def test_to_snippet(self, snippet, expected_result):
        node = SnippetElement(snippet)
        new_snippet = node.to_snippet()
        assert new_snippet == expected_result

    @pytest.mark.parametrize(
        "snippet,expected_pattern",
        [
            ('mixed_word(var=v0, value=utun0:)', 'utun0:'),
            ('mixed_word(var=v0, value=utun0++**:)', r'utun0\+\+\*\*:'),
            ('mixed_word(kvar=v0, value=utun1:)', r'[\x21-\x7e]+'),
            ('mixed_word(cvar=v0, value=utun2:)', r'(?P<v0>[\x21-\x7e]+)'),
        ]
    )
    def test_to_regex(self, snippet, expected_pattern):
        node = SnippetElement(snippet)
        pattern = node.to_regex()
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "snippet,expected_template_snippet",
        [
            ('mixed_word(var=v0, value=utun0:)', 'utun0:'),
            ('mixed_word(var=v0, value=utun0++**:)', r'utun0++**:'),
            ('mixed_word(kvar=v0, value=utun1:)', 'mixed_word()'),
            ('mixed_word(cvar=v0, value=utun2:)', 'mixed_word(var_v0)'),
        ]
    )
    def test_to_template_snippet(self, snippet, expected_template_snippet):
        node = SnippetElement(snippet)
        pattern = node.to_template_snippet()
        assert pattern == expected_template_snippet

    @pytest.mark.parametrize(
        "snippet,splitter,ref_index,expected_snippet",
        [
            (
                'mixed_word(var=v0, value=flags=8049<UP,LOOPBACK,RUNNING>)',
                '',
                5,
                ('letters(var=v6, value=flags)symbol(var=v7, value==)'
                 'digits(var=v8, value=8049)symbol(var=v9, value=<)'
                 'letters(var=v10, value=UP)symbol(var=v11, value=,)'
                 'letters(var=v12, value=LOOPBACK)symbol(var=v13, value=,)'
                 'letters(var=v14, value=RUNNING)symbol(var=v15, value=>)')
            ),
            (
                'mixed_word(var=v0, value=flags=8049<UP,LOOPBACK,RUNNING>)',
                '=<>',
                5,
                ('letters(var=v6, value=flags)symbol(var=v7, value==)'
                 'digits(var=v8, value=8049)symbol(var=v9, value=<)'
                 'mixed_word(var=v10, value=UP,LOOPBACK,RUNNING)symbol(var=v11, value=>)')
            ),

        ]
    )
    def test_split(self, snippet, splitter, ref_index, expected_snippet):
        node = SnippetElement(snippet)
        lst = node.split(splitter, ref_index=ref_index)
        lst_of_split_snippet = [item.to_snippet() for item in lst]
        new_snippet = ''.join(lst_of_split_snippet)
        assert new_snippet == expected_snippet

    @pytest.mark.parametrize(
        "lst_of_snippets,expected_snippet",
        [
            (
                [
                    'letters(var=v6, value=flags)',
                    'symbol(var=v7, value==)',
                    'digits(var=v8, value=8049)'
                ],
                'mixed_word(var=v6, value=flags=8049)'
            ),

        ]
    )
    def test_join(self, lst_of_snippets, expected_snippet):
        lst = []
        for snippet in lst_of_snippets:
            node = SnippetElement(snippet)
            lst.append(node)

        first_node = lst[0]
        remaining = lst[1:]
        new_node = first_node.join(*remaining)
        new_snippet = new_node.to_snippet()
        assert new_snippet == expected_snippet


class TestEditingSnippet:
    """Test class for EditingSnippet."""

    @pytest.mark.parametrize(
        "snippet,expected_snippet",
        [
            # test apply_action_join
            (
                'capture() keep() action(0:1-join): letters(var=v0, value=total) letters(var=v1, value=oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',     # noqa
                'capture() keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)'   # noqa
            ),
            (
                'capture() keep() action(0,1-join): letters(var=v0, value=total) letters(var=v1, value=oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',     # noqa
                'capture() keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)'   # noqa
            ),
            (
                'capture() keep() action(v0,v1-join): letters(var=v0, value=total) letters(var=v1, value=oranges) symbol(var=v2, value=:) digits(var=v3, value=123)', # noqa
                'capture() keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)'   # noqa
            ),
            (
                'capture() keep() action(v0,v1-join, 2,3-join): letters(var=v0, value=total) letters(var=v1, value=oranges) symbol(var=v2, value=:) digits(var=v3, value=123)', # noqa
                'capture() keep() action(): words(var=v0, value=total oranges) mixed_words(var=v2, value=: 123)'   # noqa
            ),
            (
                'capture() keep() action(v0,v1_join, 2,3-join): letters(var=v0, value=total) letters(var=v1, value=oranges) symbol(var=v2, value=:) digits(var=v3, value=123)', # noqa
                'capture() keep() action(): words(var=v0, value=total oranges) mixed_words(var=v2, value=: 123)'  # noqa
            ),
            # test apply_action_split
            (
                'capture() keep() action(1-split): mixed_word(var=v1, value=flags=8051<UP,RUNNING>)',   # noqa
                'capture() keep() action(): letters(var=v2, value=flags)symbol(var=v3, value==)digits(var=v4, value=8051)symbol(var=v5, value=<)letters(var=v6, value=UP)symbol(var=v7, value=,)letters(var=v8, value=RUNNING)symbol(var=v9, value=>)'   # noqa
            ),
            (
                'capture() keep() action(1-split-=<>): mixed_word(var=v1, value=flags=8051<UP,RUNNING>)',   # noqa
                'capture() keep() action(): letters(var=v2, value=flags)symbol(var=v3, value==)digits(var=v4, value=8051)symbol(var=v5, value=<)mixed_word(var=v6, value=UP,RUNNING)symbol(var=v7, value=>)'  # noqa
            ),
            (
                'capture() keep() action(v1-split-=<>): mixed_word(var=v1, value=flags=8051<UP,RUNNING>)',    # noqa
                'capture() keep() action(): letters(var=v2, value=flags)symbol(var=v3, value==)digits(var=v4, value=8051)symbol(var=v5, value=<)mixed_word(var=v6, value=UP,RUNNING)symbol(var=v7, value=>)'  # noqa
            ),
            # test apply_keep
            (
                'capture() keep(0) action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',   # noqa
                'capture() keep() action(): words(kvar=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)'  # noqa
            ),
            (
                'capture() keep(0_or) action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',  # noqa
                'capture() keep() action(): words(Kvar=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)'      # noqa
            ),
            (
                'capture() keep(0_or_empty) action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',    # noqa
                'capture() keep() action(): words(Kvar=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)'      # noqa
            ),
            (
                'capture() keep(0,  3) action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',  # noqa
                'capture() keep() action(): words(kvar=v0, value=total oranges) symbol(var=v2, value=:) digits(kvar=v3, value=123)'  # noqa
            ),
            (
                'capture() keep(v0,3) action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',   # noqa
                'capture() keep() action(): words(kvar=v0, value=total oranges) symbol(var=v2, value=:) digits(kvar=v3, value=123)'     # noqa
            ),
            (
                'capture() keep(v3,v0) action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',     # noqa
                'capture() keep() action(): words(kvar=v0, value=total oranges) symbol(var=v2, value=:) digits(kvar=v3, value=123)'     # noqa
            ),
            (
                'capture() keep(v0, 2:3) action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',# noqa
                'capture() keep() action(): words(kvar=v0, value=total oranges) symbol(kvar=v2, value=:) digits(kvar=v3, value=123)' # noqa
            ),
            (
                'capture() keep(v0, 2:3-or-empty) action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',  # noqa
                'capture() keep() action(): words(kvar=v0, value=total oranges) symbol(Kvar=v2, value=:) digits(Kvar=v3, value=123)'    # noqa
            ),

            # test apply_capture
            (
                'capture(0) keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',     # noqa
                'capture() keep() action(): words(cvar=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)'      # noqa
            ),
            (
                'capture(0_or) keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',  # noqa
                'capture() keep() action(): words(Cvar=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)'  # noqa
            ),
            (
                'capture(0_or_empty) keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',    # noqa
                'capture() keep() action(): words(Cvar=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)'      # noqa
            ),
            (
                'capture(0,  3) keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',     # noqa
                'capture() keep() action(): words(cvar=v0, value=total oranges) symbol(var=v2, value=:) digits(cvar=v3, value=123)'     # noqa
            ),
            (
                'capture(v0,3) keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',  # noqa
                'capture() keep() action(): words(cvar=v0, value=total oranges) symbol(var=v2, value=:) digits(cvar=v3, value=123)'     # noqa
            ),
            (
                'capture(v3,v0) keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',     # noqa
                'capture() keep() action(): words(cvar=v0, value=total oranges) symbol(var=v2, value=:) digits(cvar=v3, value=123)'     # noqa
            ),
            (
                'capture(v0, 2:3) keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',   # noqa
                'capture() keep() action(): words(cvar=v0, value=total oranges) symbol(cvar=v2, value=:) digits(cvar=v3, value=123)'    # noqa
            ),
            (
                'capture(v0, 2:3-or-empty) keep() action(): words(var=v0, value=total oranges) symbol(var=v2, value=:) digits(var=v3, value=123)',  # noqa
                'capture() keep() action(): words(cvar=v0, value=total oranges) symbol(Cvar=v2, value=:) digits(Cvar=v3, value=123)'    # noqa
            ),
        ]
    )
    def test_editing_snippet(self, snippet, expected_snippet):
        node = EditingSnippet(snippet)
        edited_snippet = node.to_snippet()
        assert edited_snippet == expected_snippet


class TestTranslatedPattern:
    """Test class for TranslatedPattern."""

    @pytest.mark.parametrize(
        "data1,data2,expected_pattern",
        [
            ('1', '4', '[0-9]'),
            ('2', '44', '[0-9]+'),
            ('555', '4', '[0-9]+'),
            ('1.1', '4', '[0-9]*[.]?[0-9]+'),
            ('12', '4.1', '[0-9]*[.]?[0-9]+'),
            ('12.3', '4.1', '[0-9]*[.]?[0-9]+'),
            ('3', '+4.4', r'[\(+-]?[0-9]*[.]?[0-9]+[)]?'),
            ('4', 'a', r'[a-zA-Z0-9]'),
            ('5', '-', r'[\x21-\x7e]'),
            ('5', '-+', r'[\x21-\x7e]+'),
            ('6', '- -', r'[\x21-\x7e]+( [\x21-\x7e]+)*'),
        ]
    )
    def test_recommend_pattern(self, data1, data2, expected_pattern):
        method = TranslatedPattern.recommend_pattern_using_data
        recommended_pat_obj = method(data1, data2)
        recommended_pat = recommended_pat_obj.pattern

        assert recommended_pat == expected_pattern

    @pytest.mark.parametrize(
        "data,var,expected_snippet",
        [
            ('1', '', 'digit(value=1)'),
            ('1', 'v1', 'digit(var=v1, value=1)'),
            ('123', 'v1', 'digits(var=v1, value=123)'),
            ('1.1', 'v1', 'number(var=v1, value=1.1)'),
            ('-1.1', 'v1', 'mixed_number(var=v1, value=-1.1)'),
            ('-', 'v1', 'symbol(var=v1, value=-)'),
            ('(),', 'v1', 'symbols(var=v1, value=_SYMBOL_LEFT_PARENTHESIS__SYMBOL_RIGHT_PARENTHESIS_,)'),  # noqa
            ('( ) ,', 'v1', 'symbols_group(var=v1, value=_SYMBOL_LEFT_PARENTHESIS_ _SYMBOL_RIGHT_PARENTHESIS_ ,)'),    # noqa
            ('--  ---- ++++++', 'v1', 'symbols_group(var=v1, value=--  ---- ++++++)'),
            ('a', 'v1', 'letter(var=v1, value=a)'),
            ('ab', 'v1', 'letters(var=v1, value=ab)'),
            ('a1', 'v1', 'word(var=v1, value=a1)'),
            ('a1 b2', 'v1', 'words(var=v1, value=a1 b2)'),
            ('1.1.1.1', 'v1', 'mixed_word(var=v1, value=1.1.1.1)'),
            ('1.1.1.1 2::2', 'v1', 'mixed_words(var=v1, value=1.1.1.1 2::2)'),
        ]
    )
    def test_get_readable_snippet(self, data, var, expected_snippet):
        node = TranslatedPattern.do_factory_create(data)
        snippet = node.get_readable_snippet(var=var)
        assert snippet == expected_snippet


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
            ('ab xy', '[a-zA-Z0-9]+( [a-zA-Z0-9]+)+'),
            ('1 2', '[a-zA-Z0-9]+( [a-zA-Z0-9]+)+'),
            ('ab xy', '[a-zA-Z0-9]+( [a-zA-Z0-9]+)+'),
        ]
    )
    def test_words_pattern(self, data, expected_pattern):
        node = TranslatedWordsPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('a b', TranslatedLetterPattern('a'), '[a-zA-Z0-9]+( [a-zA-Z0-9]+)*'),
            ('a b', TranslatedLettersPattern('ab'), '[a-zA-Z0-9]+( [a-zA-Z0-9]+)*'),
            ('a b', TranslatedDigitPattern('1'), '[a-zA-Z0-9]+( [a-zA-Z0-9]+)*'),
            ('a b', TranslatedDigitsPattern('4'), '[a-zA-Z0-9]+( [a-zA-Z0-9]+)*'),
            ('a b', TranslatedAlphabetNumericPattern('4'), '[a-zA-Z0-9]+( [a-zA-Z0-9]+)*'),
            ('a b', TranslatedWordPattern('4'), '[a-zA-Z0-9]+( [a-zA-Z0-9]+)*'),
            ('a b', TranslatedWordsPattern('ab xy'), '[a-zA-Z0-9]+( [a-zA-Z0-9]+)+'),
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
            ('ab xy', '[\\x21-\\x7e]+( [\\x21-\\x7e]+)+'),
            ('1', '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
            ('abc', '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
            ('192.168.0.1', '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
            ('a::b', '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
        ]
    )
    def test_mixed_words_pattern(self, data, expected_pattern):
        node = TranslatedMixedWordsPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('a b', TranslatedLetterPattern('a'), '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
            ('a b', TranslatedLettersPattern('ab'), '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
            ('a b', TranslatedDigitPattern('1'), '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
            ('a b', TranslatedDigitsPattern('4'), '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
            ('a b', TranslatedAlphabetNumericPattern('4'), '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
            ('a b', TranslatedWordPattern('4'), '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
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
            ('=', TranslatedWordsPattern('4'), '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
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
            ('=', TranslatedWordsPattern('4'), '[\\x21-\\x7e]+( [\\x21-\\x7e]+)*'),
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
            ('-- --', TranslatedLetterPattern('a'), r'[\x21-\x7e]+( [\x21-\x7e]+)*'),
            ('.. ..', TranslatedLettersPattern('ab'), r'[\x21-\x7e]+( [\x21-\x7e]+)*'),
            ('++ ++', TranslatedDigitPattern('1'), r'[\x21-\x7e]+( [\x21-\x7e]+)*'),
            ('** **', TranslatedDigitsPattern('42'), r'[\x21-\x7e]+( [\x21-\x7e]+)*'),
            ('{{ {{', TranslatedAlphabetNumericPattern('4'), r'[\x21-\x7e]+( [\x21-\x7e]+)*'),
            ('}} }}', TranslatedWordPattern('4'), r'[\x21-\x7e]+( [\x21-\x7e]+)*'),
            ('== ==', TranslatedWordsPattern('4 5'), r'[\x21-\x7e]+( [\x21-\x7e]+)+'),
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
            ('=', TranslatedWordsPattern('4 5'), r'[\x21-\x7e]+( [\x21-\x7e]+)*'),
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
            ('=', TranslatedWordsPattern('4 5'), r'\S+( \S+)*'),
            ('@', TranslatedNonWhitespacesPattern('4'), r'\S+'),
            ('#', TranslatedNonWhitespacesGroupPattern('4'), r'\S+( \S+)*'),
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
            ('=', TranslatedWordsPattern('4 5'), r'\S+( \S+)*'),
            ('@', TranslatedNonWhitespacesPattern('4'), r'\S+'),
            ('#', TranslatedNonWhitespacesGroupPattern('4'), r'\S+( \S+)*'),
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
            ('aa', r'\S+( \S+)*'),
            ('1', r'\S+( \S+)*'),
            ('+', r'\S+( \S+)*'),
            ('a', r'\S+( \S+)*'),
        ]
    )
    def test_non_whitespace_pattern(self, data, expected_pattern):
        node = TranslatedNonWhitespacesGroupPattern(data)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "data,other,expected_pattern",
        [
            ('-', TranslatedLetterPattern('a'), r'\S+( \S+)*'),
            ('.', TranslatedLettersPattern('ab'), r'\S+( \S+)*'),
            ('+', TranslatedDigitPattern('1'), r'\S+( \S+)*'),
            ('*', TranslatedDigitsPattern('42'), r'\S+( \S+)*'),
            ('a', TranslatedAlphabetNumericPattern('4'), r'\S+( \S+)*'),
            ('}', TranslatedWordPattern('4'), r'\S+( \S+)*'),
            ('=', TranslatedWordsPattern('4 5'), r'\S+( \S+)*'),
            ('@', TranslatedNonWhitespacesPattern('4'), r'\S+( \S+)*'),
            ('#', TranslatedNonWhitespacesGroupPattern('4'), r'\S+( \S+)*'),
        ]
    )
    def test_recommend_pattern(self, data, other, expected_pattern):
        node = TranslatedNonWhitespacesGroupPattern(data)
        recommended_pat_obj = node.recommend(other)
        recommended_pat = recommended_pat_obj.pattern
        assert recommended_pat == expected_pattern
