import re
from collections import OrderedDict
from itertools import combinations

import operator as op

from difflib import ndiff

from genericlib import NUMBER
from genericlib import STRING
from genericlib import PATTERN
from genericlib import TEXT
from genericlib import SYMBOL

from genericlib import Misc
from genericlib import MiscFunction
from genericlib import DotObject

from regexpro import TextPattern
from templatepro import TemplateBuilder


def get_textfsm_template(template_snippet, author='', email='',
                         company='', description=''):
    builder = TemplateBuilder(user_data=template_snippet, author=author,
                              email=email, company=company, description=description)
    textfsm_tmpl = builder.template
    return textfsm_tmpl


def verify(template_snippet, test_data,
           expected_rows_count=None, expected_result=None,
           ignore_space=True):
    builder = TemplateBuilder(user_data=template_snippet, test_data=test_data)
    is_verified = builder.verify(expected_rows_count=expected_rows_count,
                                 expected_result=expected_result,
                                 ignore_space=ignore_space)
    return is_verified


class RuntimeException:
    def raise_runtime_error(self, name='', msg=''):
        name = name.strip()
        obj = name or self
        MiscFunction.raise_runtime_error(obj=obj, msg=msg)

    @classmethod
    def do_raise_runtime_error(cls, obj=None, msg=''):
        MiscFunction.raise_runtime_error(obj=obj, msg=msg)


class LData(RuntimeException):
    def __init__(self, data):
        self.raw_data = str(data)
        self.data = self.raw_data.strip()

    def __call__(self, *args, **kwargs):
        new_instance = self.__class__(*args, **kwargs)
        return new_instance

    @property
    def leading(self):
        leading_spaces = Misc.get_leading_line(self.raw_data)
        return leading_spaces

    @property
    def trailing(self):
        match = re.search(PATTERN.SPACESATEOS, self.raw_data)
        return match.group() if match else STRING.EMPTY

    @property
    def is_leading(self):
        chk = self.leading != STRING.EMPTY
        return chk

    @property
    def is_trailing(self):
        chk = self.trailing != STRING.EMPTY
        return chk


class TranslatedPattern(RuntimeException):

    def __init__(self, data, *other, name='',
                 defined_pattern='', defined_patterns=None):
        self.data = str(data)
        self.lst_of_other_data = list(other)
        self.lst_of_all_data = [self.data] + self.lst_of_other_data
        self.defined_pattern = str(defined_pattern)
        lst = defined_patterns if isinstance(defined_patterns, list) else []
        self.defined_patterns = lst
        self.name = str(name)
        self._pattern = STRING.EMPTY
        self.process()

    def __len__(self):
        chk = self._pattern != STRING.EMPTY
        return chk

    def __call__(self, *args, **kwargs):
        new_instance = self.__class__(*args, **kwargs)
        return new_instance

    @property
    def translated(self):
        chk = self._pattern != STRING.EMPTY
        return chk

    @property
    def pattern(self):
        return self._pattern

    def process(self):
        if self.defined_patterns:
            is_matched = False
            for pat in self.defined_patterns:
                is_matched = is_matched or self.check_matching(pat)
            if is_matched:
                is_multi_spaces = self.is_group_with_multi_spaces()
                if self.is_plural():
                    index = NUMBER.TWO if is_multi_spaces else NUMBER.ONE
                    self._pattern = self.defined_patterns[-index]
                else:
                    index = NUMBER.ONE if is_multi_spaces else NUMBER.ZERO
                    self._pattern = self.defined_patterns[index]
            else:
                self._pattern = STRING.EMPTY
        else:
            is_matched = self.check_matching(self.defined_pattern)
            self._pattern = self.defined_pattern if is_matched else STRING.EMPTY

    def check_matching(self, pattern):
        pat = '%s$' % pattern

        chk = True
        for data in self.lst_of_all_data:
            match = re.match(pat, data)
            chk = chk and bool(match)

        return chk

    def is_digit(self):
        return self.name == TEXT.DIGIT

    def is_digits(self):
        return self.name == TEXT.DIGITS

    def is_number(self):
        return self.name == TEXT.NUMBER

    def is_mixed_number(self):
        return self.name == TEXT.MIXED_NUMBER

    def is_letter(self):
        return self.name == TEXT.LETTER

    def is_letters(self):
        return self.name == TEXT.LETTERS

    def is_alphabet_numeric(self):
        return self.name == TEXT.ALPHABET_NUMERIC

    def is_symbol(self):
        return self.name == TEXT.SYMBOL

    def is_symbols(self):
        return self.name == TEXT.SYMBOLS

    def is_symbols_group(self):
        return self.name == TEXT.SYMBOLS_GROUP

    def is_graph(self):
        return self.name == TEXT.GRAPH

    def is_word(self):
        return self.name == TEXT.WORD

    def is_words(self):
        return self.name == TEXT.WORDS

    def is_mixed_word(self):
        return self.name == TEXT.MIXED_WORD

    def is_mixed_words(self):
        return self.name == TEXT.MIXED_WORDS

    def is_non_whitespace(self):
        return self.name == TEXT.NON_WHITESPACE

    def is_non_whitespaces(self):
        return self.name == TEXT.NON_WHITESPACES

    def is_non_whitespaces_group(self):
        return self.name == TEXT.NON_WHITESPACES_GROUP

    def is_group(self):
        chk = self.is_symbols_group()
        chk = chk or self.is_words()
        chk = chk or self.is_mixed_words()
        chk = chk or self.is_non_whitespaces_group()
        return chk

    def is_group_with_multi_spaces(self):
        if not self.is_group():
            return False

        for data in self.lst_of_all_data:
            if STRING.DOUBLE_SPACES in data.strip():
                return True
        return False

    def is_subset_of(self, other):
        fmt = 'Need to implement subset verification for (%s, %s)'
        cls_name = Misc.get_instance_class_name(self)
        other_cls_name = Misc.get_instance_class_name(other)
        error = fmt % (cls_name, other_cls_name)
        raise NotImplementedError(error)

    def is_superset_of(self, other):
        fmt = 'Need to implement superset verification for (%s, %s)'
        cls_name = Misc.get_instance_class_name(self)
        other_cls_name = Misc.get_instance_class_name(other)
        error = fmt % (cls_name, other_cls_name)
        raise NotImplementedError(error)

    def get_new_subset(self, other):
        new_instance = other(other.data, other.get_reference_data(self))
        return new_instance

    def get_new_superset(self, other):
        new_instance = self(self.data, self.get_reference_data(other))
        return new_instance

    def is_plural(self):
        chk = True
        for data in self.lst_of_all_data:
            chk = chk and STRING.SPACE_CHAR in data.strip()
        return chk

    def is_singular(self):
        chk = True
        for data in self.lst_of_all_data:
            chk = chk and STRING.SPACE_CHAR not in data.strip()
        return chk

    def is_mixing_singular_plural(self):
        chk = not self.is_singular() and not self.is_plural()
        return chk

    def get_singular_data(self):
        singular_data = str.split(self.data, STRING.SPACE_CHAR)[NUMBER.ZERO]
        return singular_data

    def get_plural_data(self):
        for data in self.lst_of_all_data:
            if STRING.SPACE_CHAR in data.strip():
                return data
        else:
            plural_data = '%s %s' % (self.data, self.data)
            return plural_data

    def get_reference_data(self, other):
        if isinstance(other, TranslatedPattern):
            if self.is_subset_of(other) or self.is_superset_of(other):
                return other.data
            else:
                if self.is_plural() and other.is_plural():
                    return self.data
                else:
                    result = self.get_singular_data()
                    return result
        else:
            return self.data

    def raise_recommend_exception(self, other):
        cls_name = Misc.get_instance_class_name(self)
        fmt = 'Need to implement this case (%r, %r) for %s'
        self.raise_runtime_error(
            name='NotImplementRecommendedRTPattern',
            msg=fmt % (self.data, other.data, cls_name),
        )

    def get_readable_snippet(self, var=''):
        if not self.name:
            self.raise_runtime_error(
                name='TranslatedPatternSnippetRTError',
                msg='CANT create snippet without name',
            )

        value = self.data
        value = value.replace(SYMBOL.LEFT_PARENTHESIS, '_SYMBOL_LEFT_PARENTHESIS_')
        value = value.replace(SYMBOL.RIGHT_PARENTHESIS, '_SYMBOL_RIGHT_PARENTHESIS_')

        if var:
            snippet = '%s(var=%s, value=%s)' % (self.name, var, value)
        else:
            snippet = '%s(value=%s)' % (self.name, value)
        return snippet

    def get_regex_pattern(self, var=''):
        if not self.name:
            self.raise_runtime_error(
                name='TranslatedPatternRegexRTError',
                msg='CANT create regex pattern without name'
            )

        fmt = '(?P<%s>%s)'
        pattern = fmt % (var, self.pattern) if var else self.pattern
        return pattern

    def get_template_snippet(self, var=''):
        if not self.name:
            self.raise_runtime_error(
                name='TranslatedPatternTemplateSnippetRTError',
                msg='CANT create snippet without name'
            )

        var_txt = 'var_%s' % var if var else STRING.EMPTY
        tmpl_snippet = '%s(%s)' % (self.name, var_txt)
        return tmpl_snippet

    @classmethod
    def do_factory_create(cls, data, *other):
        classes = [
            TranslatedDigitPattern,
            TranslatedDigitsPattern,

            TranslatedNumberPattern,

            TranslatedLetterPattern,
            TranslatedLettersPattern,

            TranslatedAlphabetNumericPattern,
            TranslatedWordPattern,

            TranslatedSymbolPattern,
            TranslatedSymbolsPattern,
            TranslatedSymbolsGroupPattern,

            TranslatedGraphPattern,

            TranslatedMixedNumberPattern,
            TranslatedMixedWordPattern,

            TranslatedWordsPattern,

            TranslatedMixedWordsPattern,

            TranslatedNonWhitespacePattern,
            TranslatedNonWhitespacesPattern,
            TranslatedNonWhitespacesGroupPattern,
        ]
        for class_ in classes:
            node = class_(data, *other)
            if node:
                return node

        RuntimeException.do_raise_runtime_error(
            obj='FactoryTranslatedPatternRTIssue',
            msg='Need to implement this case (%r, %r)' % (data, other)
        )

    @classmethod
    def recommend_pattern(cls, translated_pat_obj1, translated_pat_obj2):
        generalized_pat = translated_pat_obj1.recommend(translated_pat_obj2)
        return generalized_pat

    @classmethod
    def recommend_pattern_using_data(cls, data1, data2):
        translated_pat_obj1 = cls.do_factory_create(data1)
        translated_pat_obj2 = cls.do_factory_create(data2)
        generalized_pat = translated_pat_obj1.recommend(translated_pat_obj2)
        return generalized_pat


class TranslatedDigitPattern(TranslatedPattern):

    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.DIGIT,
                         defined_pattern=PATTERN.DIGIT)

    def is_subset_of(self, other):
        chk = other.is_digit() or other.is_digits()
        chk = chk or other.is_number() or other.is_mixed_number()
        chk = chk or other.is_alphabet_numeric() or other.is_graph()
        chk = chk or other.is_word() or other.is_mixed_word()
        chk = chk or other.is_words() or other.is_mixed_words()
        chk = chk or other.is_non_whitespace() or other.is_non_whitespaces()
        chk = chk or other.is_non_whitespaces_group()
        return chk

    def is_superset_of(self, other):
        return False

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_letter()
            case2 = other.is_letters()
            case3 = other.is_symbol()
            case4 = other.is_symbols()
            case5 = other.is_symbols_group()

            if case1:
                return TranslatedAlphabetNumericPattern(self.data, other.data)
            elif case2:
                return TranslatedWordPattern(self.data, other.data)
            elif case3:
                return TranslatedGraphPattern(self.data, other.data)
            elif case4:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case5:
                return TranslatedMixedWordsPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedDigitsPattern(TranslatedPattern):

    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.DIGITS,
                         defined_pattern=PATTERN.DIGITS)

    def is_subset_of(self, other):
        chk = other.is_digits()
        chk = chk or other.is_number() or other.is_mixed_number()
        chk = chk or other.is_word() or other.is_mixed_word()
        chk = chk or other.is_words() or other.is_mixed_words()
        chk = chk or other.is_non_whitespaces() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_digit()
        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_letter() or other.is_letters() or other.is_alphabet_numeric()
            case2 = other.is_symbol() or other.is_symbols() or other.is_graph()
            case3 = other.is_symbols_group()
            case4 = other.is_non_whitespace()
            if case1:
                return TranslatedWordPattern(self.data, other.data)
            elif case2:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case3:
                return TranslatedMixedWordsPattern(self.data, other.data)
            elif case4:
                return TranslatedNonWhitespacesPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedNumberPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.NUMBER,
                         defined_pattern=PATTERN.NUMBER)

    def is_subset_of(self, other):
        chk = other.is_number() or other.is_mixed_number()
        chk = chk or other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespaces() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_digit() or other.is_digits()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_letter() or other.is_letters()
            case1 = case1 or other.is_alphabet_numeric() or other.is_graph()
            case1 = case1 or other.is_symbol() or other.is_symbols() or other.is_word()

            case2 = other.is_words() or other.is_symbols_group()
            case3 = other.is_non_whitespace()

            if case1:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case2:
                return TranslatedMixedWordsPattern(self.data, other.data)
            elif case3:
                return TranslatedNonWhitespacesPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedMixedNumberPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.MIXED_NUMBER,
                         defined_pattern=PATTERN.MIXED_NUMBER)

    def is_subset_of(self, other):
        chk = other.is_mixed_number() or other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespaces() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_digit() or other.is_digits() or other.is_number()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_letter() or other.is_letters()
            case1 |= other.is_alphabet_numeric() or other.is_graph()
            case1 |= other.is_symbol() or other.is_symbols()
            case1 |= other.is_word()

            case2 = other.is_words() or other.is_symbols_group()
            case3 = other.is_non_whitespace()

            if case1:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case2:
                return TranslatedMixedWordsPattern(self.data, other.data)
            elif case3:
                return TranslatedNonWhitespacesPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedLetterPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.LETTER,
                         defined_pattern=PATTERN.LETTER)

    def is_subset_of(self, other):
        chk = other.is_letter() or other.is_letters()
        chk = chk or other.is_alphabet_numeric() or other.is_graph()
        chk = chk or other.is_word() or other.is_words()
        chk = chk or other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespace() or other.is_non_whitespaces()
        chk = chk or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        return False

    def recommend(self, other):
        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_digit()
            case2 = other.is_digits()
            case3 = other.is_symbols() or other.is_number() or other.is_mixed_number()
            case4 = other.is_symbol()
            case5 = other.is_symbols_group()

            if case1:
                return TranslatedAlphabetNumericPattern(self.data, other.data)
            elif case2:
                return TranslatedWordPattern(self.data, other.data)
            elif case3:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case4:
                return TranslatedGraphPattern(self.data, other.data)
            elif case5:
                return TranslatedMixedWordsPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedLettersPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.LETTERS,
                         defined_pattern=PATTERN.LETTERS)

    def is_subset_of(self, other):
        chk = other.is_letters() or other.is_word() or other.is_words()
        chk = chk or other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespaces() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_letter()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_digit() or other.is_digits()

            case2 = other.is_number() or other.is_mixed_number()
            case2 = case2 or other.is_alphabet_numeric()
            case2 = case2 or other.is_symbol() or other.is_symbols()

            case3 = other.is_symbols_group()
            case4 = other.is_non_whitespace()

            if case1:
                return TranslatedWordPattern(self.data, other.data)
            elif case2:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case3:
                return TranslatedMixedWordsPattern(self.data, other.data)
            elif case4:
                return TranslatedNonWhitespacesPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedAlphabetNumericPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.ALPHABET_NUMERIC,
                         defined_pattern=PATTERN.ALPHABET_NUMERIC)

    def is_subset_of(self, other):
        chk = other.is_alphabet_numeric() or other.is_word() or other.is_words()
        chk = chk or other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespace() or other.is_non_whitespaces()
        chk = chk or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_letter() or other.is_letters() or other.is_digit()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_digits()
            case2 = other.is_number() or other.is_mixed_number()
            case2 = case2 or other.is_symbol() or other.is_symbols()
            case3 = other.is_symbols_group()

            if case1:
                return TranslatedWordPattern(self.data, other.data)
            elif case2:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case3:
                return TranslatedMixedWordsPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedSymbolPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.SYMBOL,
                         defined_pattern=PATTERN.SYMBOL)

    def is_subset_of(self, other):
        chk = other.is_symbol() or other.is_graph()
        chk = chk or other.is_symbols() or other.is_symbols_group()
        chk = chk or other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespace() or other.is_non_whitespaces()
        chk = chk or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        return False

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_letter() or other.is_digit() or other.is_alphabet_numeric()

            case2 = other.is_letters() or other.is_digits()
            case2 = case2 or other.is_number() or other.is_mixed_number()
            case2 = case2 or other.is_word()

            case3 = other.is_words()

            if case1:
                return TranslatedGraphPattern(self.data)
            elif case2:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case3:
                return TranslatedMixedWordsPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedSymbolsPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.SYMBOLS,
                         defined_pattern=PATTERN.SYMBOLS)

    def is_subset_of(self, other):
        chk = other.is_symbols() or other.is_symbols_group()
        chk = chk or other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespaces() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_symbol()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_letter() or other.is_digit()
            case1 = case1 or other.is_alphabet_numeric() or other.is_graph()
            case1 = case1 or other.is_letters() or other.is_digits()
            case1 = case1 or other.is_number() or other.is_mixed_number()
            case1 = case1 or other.is_word()

            case2 = other.is_words()
            case3 = other.is_non_whitespace()

            if case1:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case2:
                return TranslatedMixedWordsPattern(self.data, other.data)
            elif case3:
                return TranslatedNonWhitespacesPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedSymbolsGroupPattern(TranslatedPattern):
    def __init__(self, data, *other):
        defined_patterns = [
            PATTERN.SYMBOLS_OR_GROUP,
            PATTERN.SYMBOLS_OR_FLEX_GROUP,
            PATTERN.SYMBOLS_FLEX_GROUP,
            PATTERN.SYMBOLS_GROUP
        ]
        super().__init__(data, *other, name=TEXT.SYMBOLS_GROUP,
                         defined_patterns=defined_patterns)

    def is_subset_of(self, other):
        chk = other.is_symbols_group() or other.is_mixed_word()
        chk = chk or other.is_mixed_words() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_symbol() or other.is_symbols()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_letter() or other.is_digit()
            case1 = case1 or other.is_alphabet_numeric() or other.is_graph()
            case1 = case1 or other.is_letters() or other.is_digits()
            case1 = case1 or other.is_number() or other.is_mixed_number()
            case1 = case1 or other.is_word() or other.is_words()

            case2 = other.is_non_whitespace() or other.is_non_whitespaces()

            if case1:
                return TranslatedMixedWordsPattern(self.data, other.data)
            elif case2:
                return TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedGraphPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.GRAPH,
                         defined_pattern=PATTERN.GRAPH)

    def is_subset_of(self, other):
        chk = other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespace() or other.is_non_whitespaces()
        chk = chk or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_letter() or other.is_digit()
        chk = chk or other.is_alphabet_numeric() or other.is_symbol()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_letters() or other.is_digits()
            case1 = case1 or other.is_number() or other.is_mixed_number()
            case1 = case1 or other.is_word()

            case2 = other.is_words()

            if case1:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case2:
                return TranslatedMixedWordsPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedWordPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.WORD,
                         defined_pattern=PATTERN.WORD)

    def is_subset_of(self, other):
        chk = other.is_word() or other.is_words()
        chk = chk or other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespaces() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_letter() or other.is_letters()
        chk = chk or other.is_digit() or other.is_digits()
        chk = chk or other.is_alphabet_numeric()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_number() or other.is_mixed_number()
            case2 = other.is_non_whitespace()

            if case1:
                return TranslatedMixedWordPattern(self.data, other.data)
            elif case2:
                return TranslatedNonWhitespacesPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedWordsPattern(TranslatedPattern):
    def __init__(self, data, *other):
        defined_patterns = [
            PATTERN.WORD_OR_WORDS,
            PATTERN.WORD_OR_FLEX_WORDS,
            PATTERN.FLEX_WORDS,
            PATTERN.WORDS
        ]
        super().__init__(data, *other, name=TEXT.WORDS,
                         defined_patterns=defined_patterns)

    def is_subset_of(self, other):
        chk = other.is_words() or other.is_mixed_words() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_letter() or other.is_letters()
        chk = chk or other.is_digit() or other.is_digits()
        chk = chk or other.is_alphabet_numeric() or other.is_word()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_number() or other.is_mixed_number()
            case2 = other.is_non_whitespace() or other.is_non_whitespaces()

            if case1:
                return TranslatedMixedWordsPattern(self.data, other.data)
            elif case2:
                return TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedMixedWordPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.MIXED_WORD,
                         defined_pattern=PATTERN.MIXED_WORD)

    def is_subset_of(self, other):
        chk = other.is_mixed_word() or other.is_mixed_words()
        chk = chk or other.is_non_whitespaces() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_letter() or other.is_letters()
        chk = chk or other.is_digit() or other.is_digits()
        chk = chk or other.is_alphabet_numeric() or other.is_word()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_words()
            case2 = other.is_non_whitespace()

            if case1:
                return TranslatedMixedWordsPattern(self.data, other.data)
            elif case2:
                return TranslatedNonWhitespacesPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedMixedWordsPattern(TranslatedPattern):
    def __init__(self, data, *other):
        defined_patterns = [
            PATTERN.MIXED_WORD_OR_WORDS,
            PATTERN.MIXED_WORD_OR_FLEX_WORDS,
            PATTERN.MIXED_FLEX_WORDS,
            PATTERN.MIXED_WORDS
        ]
        super().__init__(data, *other, name=TEXT.MIXED_WORDS,
                         defined_patterns=defined_patterns)

    def is_subset_of(self, other):
        chk = other.is_mixed_words() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_letter() or other.is_letters()
        chk = chk or other.is_digit() or other.is_digits()
        chk = chk or other.is_alphabet_numeric()
        chk = chk or other.is_word() or other.is_words() or other.is_mixed_word()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_non_whitespace() or other.is_non_whitespaces()

            if case1:
                return TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedNonWhitespacePattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.NON_WHITESPACE,
                         defined_pattern=PATTERN.NON_WHITESPACE)

    def is_subset_of(self, other):
        chk = other.is_non_whitespace() or other.is_non_whitespaces()
        chk = chk or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_letter() or other.is_digit()
        chk = chk or other.is_alphabet_numeric()
        chk = chk or other.is_symbol() or other.is_graph()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_letters() or other.is_digits() or other.is_symbols()
            case1 = case1 or other.is_number() or other.is_mixed_number()
            case1 = case1 or other.is_word() or other.is_mixed_word()

            case2 = other.is_words() or other.is_mixed_words()

            if case1:
                return TranslatedNonWhitespacesPattern(self.data, other.data)
            elif case2:
                return TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedNonWhitespacesPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.NON_WHITESPACES,
                         defined_pattern=PATTERN.NON_WHITESPACES)

    def is_subset_of(self, other):
        chk = other.is_non_whitespaces() or other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_digit() or other.is_digits()
        chk = chk or other.is_number() or other.is_mixed_number()
        chk = chk or other.is_letter() or other.is_letters()
        chk = chk or other.is_alphabet_numeric() or other.is_graph()
        chk = chk or other.is_symbol() or other.is_symbols()
        chk = chk or other.is_word() or other.is_mixed_word()
        chk = chk or other.is_non_whitespace()

        return chk

    def recommend(self, other):

        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            case1 = other.is_symbols_group() or other.is_words() or other.is_mixed_words()

            if case1:
                return TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            else:
                self.raise_recommend_exception(other)


class TranslatedNonWhitespacesGroupPattern(TranslatedPattern):
    def __init__(self, data, *other):
        defined_patterns = [
            PATTERN.NON_WHITESPACES_OR_GROUP,
            PATTERN.NON_WHITESPACES_OR_FLEX_GROUP,
            PATTERN.NON_WHITESPACES_FLEX_GROUP,
            PATTERN.NON_WHITESPACES_GROUP
        ]
        super().__init__(data, *other, name=TEXT.NON_WHITESPACES_GROUP,
                         defined_patterns=defined_patterns)

    def is_subset_of(self, other):
        chk = other.is_non_whitespaces_group()

        return chk

    def is_superset_of(self, other):
        chk = other.is_digit() or other.is_digits()
        chk = chk or other.is_number() or other.is_mixed_number()
        chk = chk or other.is_letter() or other.is_letters()
        chk = chk or other.is_alphabet_numeric() or other.is_graph()
        chk = chk or other.is_symbol() or other.is_symbols() or other.is_symbols_group()
        chk = chk or other.is_word() or other.is_mixed_word()
        chk = chk or other.is_words() or other.is_mixed_words()
        chk = chk or other.is_non_whitespace() or other.is_non_whitespaces()

        return chk

    def recommend(self, other):
        if self.is_subset_of(other) or self.is_superset_of(other):
            if self.is_subset_of(other):
                return self.get_new_subset(other)
            else:
                return self.get_new_superset(other)
        else:
            self.raise_recommend_exception(other)


class NDiffBaseText:
    def __init__(self, txt):
        self._lst = []
        self._lst_other = []
        self._is_common = False
        self._is_changed = False

        if txt.startswith(STRING.DOUBLE_SPACES):
            self._lst.append(txt.lstrip(STRING.SPACE_CHAR))
            self._is_common = True

        if txt.startswith('- ') or txt.startswith('+ '):
            txt.startswith('- ') and self._lst.append(txt.lstrip('- '))
            txt.startswith('+ ') and self._lst_other.append(txt.lstrip('+ '))
            self._is_changed = True

    def __len__(self):
        chk = bool(len(self._lst) or len(self._lst_other))
        return chk

    @property
    def is_common(self):
        return self._is_common

    @property
    def is_changed(self):
        return self._is_changed

    @property
    def name(self):
        return STRING.EMPTY

    @property
    def lst(self):
        return self._lst

    @property
    def lst_other(self):
        return self._lst_other

    def is_same_type(self, other):
        if self.name:
            chk = self.name == other.name
            return chk
        else:
            return False

    def extend(self, other):
        self._lst.extend(other.lst)
        self._lst_other.extend(other.lst_other)

    def readjust_lst(self, *lst_of_txt):
        if lst_of_txt:
            self._lst.clear()
            self._lst.extend(txt for txt in lst_of_txt if txt)

    def readjust_lst_other(self, *lst_of_other_txt):
        if lst_of_other_txt:
            self._lst_other.clear()
            self._lst_other.extend(txt for txt in lst_of_other_txt if txt)

    @classmethod
    def do_factory_create(cls, txt):
        if txt.startswith(STRING.DOUBLE_SPACES):
            return NDiffCommonText(txt)
        else:
            changed_node = NDiffChangedText(txt)
            node = changed_node if changed_node else None
        return node


class NDiffChangedText(NDiffBaseText):
    @property
    def name(self):
        name_ = 'ndiff_changed_text' if self else STRING.EMPTY
        return name_

    @property
    def is_containing_empty_changed(self):
        if self.lst and self.lst_other:
            return False
        elif self.lst or self.lst_other:
            return True
        else:
            return False

    def get_pattern(self, var=''):
        txt1 = str.join(STRING.DOUBLE_SPACES, self.lst)
        txt2 = str.join(STRING.DOUBLE_SPACES, self.lst_other)
        if txt1 or txt2:
            args = [txt1, txt2] if txt1 and txt2 else [txt1] if txt1 else [txt2]
            translated_obj = TranslatedPattern.do_factory_create(*args)
            pattern = translated_obj.pattern
        else:
            pattern = STRING.EMPTY

        empty_flag = '?' if self.is_containing_empty_changed else STRING.EMPTY

        if var:
            pattern = '(?P<%s>%s)%s' % (var, pattern, empty_flag)
        else:
            if pattern:
                pattern = '(%s)?' % pattern
        return pattern


class NDiffCommonText(NDiffBaseText):
    @property
    def name(self):
        name_ = 'ndiff_common_text' if self else STRING.EMPTY
        return name_

    def get_pattern(self, var=''):
        txt = str.join(STRING.DOUBLE_SPACES, self.lst)
        pattern = TextPattern(txt) if txt else STRING.EMPTY
        pattern = '(?P<%s>%s)' % (var, pattern) if var else pattern
        return pattern


class NDiffLinePattern:
    def __init__(self, line_a, line_b):
        self.is_leading = line_a.startswith(STRING.SPACE_CHAR)
        self.is_leading |= line_b.startswith(STRING.SPACE_CHAR)
        self.is_trailing = line_a.startswith(STRING.SPACE_CHAR)
        self.is_trailing |= line_b.startswith(STRING.SPACE_CHAR)
        self.line_a = line_a
        self.line_b = line_b

        self._line_a = self.line_a.strip()
        self._line_b = self.line_b.strip()

        self._pattern = STRING.EMPTY
        self.process()

    def __len__(self):
        return self._pattern != STRING.EMPTY

    def __call__(self, *args, **kwargs):
        new_instance = self.__class__(*args, **kwargs)
        return new_instance

    @property
    def pattern(self):
        return self._pattern

    def analyze_and_parse_empty_case(self):
        is_equal = self._line_a == self._line_b
        is_empty = self._line_a == STRING.EMPTY

        if is_empty and is_equal:
            if self.is_leading or self.is_trailing:
                self._pattern = PATTERN.SPACES
            return True
        return False

    def analyze_and_parse_identical_case(self):
        if self._line_a == self._line_b:
            self._pattern = TextPattern(self._line_a)
            if self.is_leading:
                self._pattern = '%s%s' % (PATTERN.ZOSPACES, self._pattern)
            if self.is_trailing:
                self._pattern = '%s%s' % (self._pattern, PATTERN.ZOSPACES)
        else:
            lst_a = re.split(PATTERN.SPACES, self._line_a)
            lst_b = re.split(PATTERN.SPACES, self._line_b)
            if lst_a == lst_b:
                self._pattern = TextPattern(str.join(STRING.DOUBLE_SPACES, lst_a))
                if self.is_leading:
                    self._pattern = '%s%s' % (PATTERN.ZOSPACES, self._pattern)
                if self.is_trailing:
                    self._pattern = '%s%s' % (self._pattern, PATTERN.ZOSPACES)
                return True
        return False

    def build_list_of_diff(self):
        lst_a = re.split(PATTERN.SPACES, self._line_a)
        lst_b = re.split(PATTERN.SPACES, self._line_b)

        diff = ndiff(lst_a, lst_b)
        lst = list(diff)

        result = []
        for item in lst:
            node = NDiffBaseText.do_factory_create(item)
            if result:
                prev_node = result[-NUMBER.ONE]
                if prev_node.is_same_type(node):
                    prev_node.extend(node)
                else:
                    result.append(node)
            else:
                result.append(node)
        return result

    def build_pattern_from_diff_list(self, lst):    # noqa
        total = len(lst)
        if total == NUMBER.ONE:
            item = lst[NUMBER.ZERO]
            if item.is_changed:
                pattern = item.get_pattern(var='v0')
            else:
                pattern = item.get_pattern()
            return pattern
        else:
            result = []
            count = 0
            spacer = PATTERN.SPACES
            for index, item in enumerate(lst):
                if index <= total - NUMBER.TWO:
                    if item.is_changed:
                        pat = item.get_pattern(var='v%s' % count)
                        count += 1
                        if item.is_containing_empty_changed:
                            result.extend([pat, '(%s)?' % spacer])
                        else:
                            result.extend([pat, spacer])
                    else:
                        pat = item.get_pattern()
                        result.extend([pat, spacer])
                else:
                    if item.is_changed:
                        pat = item.get_pattern(var='v%s' % count)
                        if item.is_containing_empty_changed:
                            result.pop()
                            result.extend(['(%s)?' % spacer, pat])
                        else:
                            result.append(pat)
                    else:
                        pat = item.get_pattern()
                        result.append(pat)
            pattern = str.join(STRING.EMPTY, result)
            return pattern

    def analyze_and_parse_diff_case(self):

        if self.analyze_and_parse_empty_case():
            return False
        elif self.analyze_and_parse_identical_case():
            return False
        else:
            lst = self.build_list_of_diff()
            self._pattern = self.build_pattern_from_diff_list(lst)
            return True

    def process(self):
        is_empty = self.analyze_and_parse_empty_case()
        is_similar = not is_empty and self.analyze_and_parse_identical_case()
        not is_similar and self.analyze_and_parse_diff_case()


class DiffLinePattern(RuntimeException):
    def __init__(self, line1, line2, *other_lines):
        self.raw_lines = []
        self.lines = []
        self._pattern = STRING.EMPTY
        self.prepare(line1, line2, *other_lines)
        self.process()

    def __len__(self):
        chk = bool(len(self._pattern))
        return int(chk)

    @property
    def pattern(self):
        pattern = self._pattern

        fmt = '%s%s'
        if self.is_leading:
            if self.are_all_leading:
                pattern = fmt % (PATTERN.SPACES, pattern)
            else:
                pattern = fmt % (PATTERN.ZOSPACES, pattern)

        if self.is_trailing:
            if self.are_all_trailing:
                pattern = fmt % (pattern, PATTERN.SPACES)
            else:
                pattern = fmt % (pattern, PATTERN.ZOSPACES)

        return pattern

    @property
    def are_all_leading(self):
        chk = all(line.startswith(STRING.SPACE_CHAR) for line in self.raw_lines)
        return chk

    @property
    def are_all_trailing(self):
        chk = all(line.endswith(STRING.SPACE_CHAR) for line in self.raw_lines)
        return chk

    @property
    def is_leading(self):
        chk = any(Misc.is_leading_line(line) for line in self.raw_lines)
        return chk

    @property
    def is_trailing(self):
        chk = any(Misc.is_trailing_line(line) for line in self.raw_lines)
        return chk

    def reset(self):
        self.lines.clear()
        self._pattern = STRING.EMPTY

    def prepare(self, line1, line2, *other_lines):

        lst = [line1, line2] + list(other_lines)

        raw_lines = []
        lines = []

        for line in lst:
            trim_line = line.strip()
            if trim_line:
                line not in raw_lines and raw_lines.append(line)
                trim_line not in lines and lines.append(trim_line)

        if len(lines) < NUMBER.TWO:
            fmt = ('CANT form pattern because provided '
                   'lines are less than two\n%s')
            lst = ['Line 1: %r' % line1, 'Line 2: %r' % line2]
            if other_lines:
                lst.append('Other Lines: %r' % other_lines)

            self.raise_runtime_error(msg=fmt % str.join(STRING.NEWLINE, lst))
        else:
            self.reset()
            self.lines.extend(lines)
            self.raw_lines.extend(raw_lines)

    def get_pattern_btw_two_lines(self, line_a, line_b):    # noqa

        is_leading_a = line_a.startswith(STRING.SPACE_CHAR)
        is_leading_b = line_b.startswith(STRING.SPACE_CHAR)

        is_both_leading = is_leading_a and is_leading_b
        is_leading = is_leading_a or is_leading_b

        is_trailing_a = line_a.endswith(STRING.SPACE_CHAR)
        is_trailing_b = line_b.endswith(STRING.SPACE_CHAR)

        is_both_trailing = is_trailing_a and is_trailing_b
        is_trailing = is_trailing_a or is_trailing_b

        diff_line_obj = NDiffLinePattern(line_a, line_b)
        pattern = diff_line_obj.pattern

        fmt = '%s%s'
        if is_both_leading:
            pattern = fmt % (PATTERN.SPACES, pattern)
        elif is_leading:
            pattern = fmt % (PATTERN.ZOSPACES, pattern)

        if is_both_trailing:
            pattern = fmt % (pattern, PATTERN.SPACES)
        elif is_trailing:
            pattern = fmt % (pattern, PATTERN.ZOSPACES)

        return pattern

    def is_matched_all(self, pattern):
        for line in self.lines:
            match = re.match(pattern, line)
            if not match:
                return False
            else:
                if match.group() != line:
                    return False
        return True

    def process(self):
        lines_count = len(self.lines)

        pairs = list(combinations(range(lines_count), NUMBER.TWO))

        lst = []

        for i, j in pairs:
            line_a = self.lines[i]
            line_b = self.lines[j]
            pattern = self.get_pattern_btw_two_lines(line_a, line_b)
            lst.append(pattern)
            if self.is_matched_all(pattern):
                self._pattern = pattern
                return

        fmt = 'built pattern(s) did not match text\n  %s'
        self.raise_runtime_error(msg=fmt % str.join('\n  ', [repr(item) for item in lst]))


class SnippetElement(RuntimeException):
    def __init__(self, element_txt, trailing=''):
        self.element_txt = element_txt
        self.trailing = trailing
        self.name = STRING.EMPTY
        self.var_name = STRING.EMPTY
        self.value = STRING.EMPTY

        self.is_captured = False
        self.is_kept = False
        self.is_empty = False

        self.parse()

    def __call__(self, *args, **kwargs):
        new_instance = self.__class__(*args, **kwargs)
        return new_instance

    @property
    def var_index(self):
        pat = '[0-9]+(_[0-9]+)?$'
        match = re.search(pat, self.var_name)
        if match:
            matched_txt = match.group()
            if matched_txt.isdigit():
                result = int(matched_txt)
            else:
                first, last = str.split(matched_txt, STRING.UNDERSCORE_CHAR, maxsplit=1)
                result = int(first) * NUMBER.TEN + int(last)

            return result
        else:
            return NUMBER.ZERO

    def parse(self):
        pat = ('(?P<name>[a-zA-Z]+(_[a-zA-Z]+)?)[(] *'
               '(?P<check>[cCkK]?var)=(?P<var_name>.+), +'
               'value=(?P<value>.+) *[)]')
        match = re.match(pat, self.element_txt)
        if not match:
            self.raise_runtime_error(msg='Invalid element text\n%s' % self.element_txt)

        check = match.group('check')
        if check.lower() == 'cvar':
            self.is_captured = True
            self.is_empty = check == 'Cvar'
        elif check.lower() == 'kvar':
            self.is_kept = True
            self.is_empty = check == 'Kvar'

        self.name = match.group('name')
        self.var_name = match.group('var_name')
        self.value = match.group('value')

    def set_captured(self):
        self.is_captured = True
        self.is_kept = False

    def set_kept(self):
        self.is_captured = False
        self.is_kept = True

    def set_empty(self):
        self.is_empty = True

    def split(self, splitter='', ref_index=0):

        if splitter:
            pat = '[%s]+' % re.escape(splitter)
        else:
            pat = PATTERN.SYMBOLS

        separators = re.findall(pat, self.value)
        items = re.split(pat, self.value)

        lst = []
        for index, item in enumerate(items):
            if index < len(items) - NUMBER.ONE:
                item and lst.append(item)
                lst.append(separators[index])
            else:
                item and lst.append(item)

        result = []
        for index, item in enumerate(lst):
            if ref_index:
                new_var_name = 'v%s' % (ref_index + index + 1)
            else:
                new_var_name = '%s%s' % (self.var_name, index)

            pat_obj = TranslatedPattern.do_factory_create(item)
            sub_editable_snippet = pat_obj.get_readable_snippet(var=new_var_name)

            trailing = self.trailing if index == len(lst) - NUMBER.ONE else STRING.EMPTY
            node = self(sub_editable_snippet, trailing=trailing)
            result.append(node)

        return result

    def join(self, *args):
        if args:
            txt = '%s%s' % (self.value, self.trailing)
            for arg in args:
                txt = '%s%s%s' % (txt, arg.value, arg.trailing)
            txt = txt.strip()
            new_pat_obj = TranslatedPattern.do_factory_create(txt)
            element_txt = new_pat_obj.get_readable_snippet(var=self.var_name)
            trailing = arg.trailing     # noqa
        else:
            element_txt = self.element_txt
            trailing = self.trailing
        new_instance = self(element_txt, trailing=trailing)
        return new_instance

    def to_regex(self):

        if not self.is_kept and not self.is_captured:
            txt = '%s%s' % (self.value, self.trailing)
            txt_pat = TextPattern(txt)
            return txt_pat
        else:
            tbl = {
                TEXT.DIGIT: PATTERN.DIGIT,
                TEXT.DIGITS: PATTERN.DIGITS,
                TEXT.NUMBER: PATTERN.NUMBER,
                TEXT.MIXED_NUMBER: PATTERN.MIXED_NUMBER,
                TEXT.LETTER: PATTERN.LETTER,
                TEXT.LETTERS: PATTERN.LETTERS,
                TEXT.ALPHABET_NUMERIC: PATTERN.ALPHABET_NUMERIC,
                TEXT.SYMBOL: PATTERN.SYMBOL,
                TEXT.SYMBOLS: PATTERN.SYMBOLS,
                TEXT.SYMBOLS_GROUP: PATTERN.SYMBOLS_OR_GROUP,
                TEXT.GRAPH: PATTERN.GRAPH,
                TEXT.WORD: PATTERN.WORD,
                TEXT.WORDS: PATTERN.WORD_OR_WORDS,
                TEXT.MIXED_WORD: PATTERN.MIXED_WORD,
                TEXT.MIXED_WORDS: PATTERN.MIXED_WORD_OR_WORDS,
                TEXT.NON_WHITESPACE: PATTERN.NON_WHITESPACE,
                TEXT.NON_WHITESPACES: PATTERN.NON_WHITESPACES,
                TEXT.NON_WHITESPACES_GROUP: PATTERN.NON_WHITESPACES_OR_GROUP
            }
            pat = tbl.get(self.name, PATTERN.MIXED_WORD_OR_WORDS)

            if self.is_captured:
                pat = '(?P<%s>%s)' % (self.var_name, pat)

            if self.is_empty:
                if self.trailing:
                    if re.match(PATTERN.SPACESATEOS, self.trailing):
                        pat = '(%s)?(%s)?' % (pat, TextPattern(self.trailing))
                    else:
                        pat = '(%s)?%s' % (pat, TextPattern(self.trailing))
                else:
                    pat = '(%s)?' % pat
            else:
                pat = pat + TextPattern(self.trailing)
            return pat

    def to_template_snippet(self):

        if not self.is_kept and not self.is_captured:
            txt = '%s%s' % (self.value, self.trailing)
            return txt
        else:
            if self.is_captured:
                tmpl_snippet = '%s(var_%s)' % (self.name, self.var_name)
            else:
                tmpl_snippet = '%s()' % self.name

            if self.is_empty:
                tmpl_snippet = '%s%s' % (tmpl_snippet, 'empty()')

            return tmpl_snippet

    def to_snippet(self):
        v = 'var'
        if self.is_captured or self.is_kept:
            v = 'cvar' if self.is_captured else 'kvar'
            v = v.title() if self.is_empty else v
        fmt = '%s(%s=%s, value=%s)'
        snippet = fmt % (self.name, v, self.var_name, self.value)
        snippet = snippet + self.trailing
        return snippet


class EditingSnippet(LData):
    def __init__(self, editing_snippet):    # noqa
        self.data = editing_snippet
        self.capture = STRING.EMPTY
        self.keep = STRING.EMPTY
        self.action = STRING.EMPTY
        self.raw_data = STRING.EMPTY
        self.snippet = STRING.EMPTY
        self.snippet_elements = []

        self.largest_index = 0

        self.is_action_applied = False
        self.is_keep_applied = False
        self.is_capture_applied = False

        self.process()

    def prepare(self):
        pat = (r'capture[(](?P<capture>[^\)]*)[)] '
               r'keep[(](?P<keep>[^\)]*)[)] '
               r'action[(](?P<action>[^\)]*)[)]: '
               r'(?P<snippet>.+)')

        match = re.match(pat, self.data)
        if not match:
            self.raise_runtime_error(msg='Invalid argument\n%s' % self.data)

        self.capture = match.group('capture').strip()
        self.keep = match.group('keep').strip()
        self.action = match.group('action').strip()
        self.raw_data = match.group('snippet')
        self.snippet = self.raw_data.strip()

        pat = r'\w+\([cCkK]?var=[^\)]+, value=[^\)]+\)'
        spacers = re.split(pat, self.snippet)[NUMBER.ONE:-NUMBER.ONE]
        items = re.findall(pat, self.snippet)
        total = len(items)

        for i, snippet_txt in enumerate(items):
            trailing = spacers[i] if i < total - NUMBER.ONE else STRING.EMPTY
            node = SnippetElement(snippet_txt, trailing=trailing)
            self.largest_index = max(self.largest_index, node.var_index)
            self.snippet_elements.append(node)

    def refresh_largest_index(self):
        for node in self.snippet_elements:
            self.largest_index = max(self.largest_index, node.var_index)

    def find_element(self, var_name):
        for index, node in enumerate(self.snippet_elements):
            if node.var_name == var_name:
                return index, node
        return -NUMBER.ZERO, None

    def apply_action_join(self, action_op):
        if not re.search('[_-]join', action_op, re.I):
            return False

        grp = re.split('[_-]join', action_op, re.I)[NUMBER.ZERO]

        if re.match(r'\d+:\d+$', grp):
            first, last = str.split(grp, STRING.COLON_CHAR, maxsplit=NUMBER.ONE)
            var_names = ['v%s' % i for i in range(int(first), int(last) + 1)]
            if not var_names:
                self.raise_runtime_error(
                    name='EditingSnippetActionJoinRTError',
                    msg='Invalid range (%s)' % action_op
                )
        elif re.match(r'\w+(,\w+)*', grp):
            var_names = ['v%s' % i if str.isdigit(i) else i for i in str.split(grp, STRING.COMMA_CHAR)]

        first_index, first_node = self.find_element(var_names[NUMBER.ZERO]) # noqa
        if first_index >= NUMBER.ZERO:
            remain_modes = []

            for var_name in var_names[NUMBER.ONE:]:
                index, node = self.find_element(var_name)
                if index >= NUMBER.ZERO:
                    remain_modes.append(node)
            joint_node = first_node.join(*remain_modes)
            self.snippet_elements[first_index] = joint_node
            self.is_action_applied = True

            for removed_node in remain_modes:
                removed_index = self.snippet_elements.index(removed_node)
                self.snippet_elements.pop(removed_index)
            self.refresh_largest_index()
            return True
        else:
            self.raise_runtime_error(
                name='EditingSnippetActionJoinRTError',
                msg='Not found index (%s)' % action_op
            )

    def apply_action_split(self, action_op):
        if not re.search('[_-]split', action_op, re.I):
            return False

        var_name, sep = re.split('[_-]split[-_]?', action_op, maxsplit=1, flags=re.I)
        sep = re.sub('_left_parenthesis_', SYMBOL.LEFT_PARENTHESIS, sep, flags=re.I)
        sep = re.sub('_right_parenthesis_', SYMBOL.RIGHT_PARENTHESIS, sep, flags=re.I)
        var_name = 'v%s' % var_name if var_name.isdigit() else var_name

        index, node = self.find_element(var_name)
        if index >= NUMBER.ZERO:
            self.refresh_largest_index()
            sub_lst = node.split(splitter=sep, ref_index=self.largest_index)
            left_sub_lst = self.snippet_elements[:index]
            right_sub_lst = self.snippet_elements[index + NUMBER.ONE:]
            self.snippet_elements = left_sub_lst + sub_lst + right_sub_lst
            self.is_action_applied = True
            self.refresh_largest_index()
        else:
            self.raise_runtime_error(
                name='EditingSnippetActionSplitRTError',
                msg='Not found index (%s)' % var_name
            )

    def apply_action(self):
        if not self.action:
            return

        action_ops = re.split(',? +', self.action)
        for action_op in action_ops:
            if not re.search('join|split', action_op, re.I):
                continue
            is_applied = self.apply_action_join(action_op)
            not is_applied and self.apply_action_split(action_op)

    def apply_keep(self):
        if not self.keep:
            return

        items = re.split(PATTERN.SPACES, self.keep)
        for item in items:
            item = item.strip(',')
            is_empty = bool(re.search('[_-]?or([_-]empty)?', item, re.I))
            item = re.sub('[_-]?or([_-]empty)?', STRING.EMPTY, item, re.I)

            if re.match(r'\d+:\d+$', item):
                first, last = str.split(item, STRING.COLON_CHAR, maxsplit=NUMBER.ONE)
                var_names = ['v%s' % i for i in range(int(first), int(last) + 1)]
                if not var_names:
                    self.raise_runtime_error(
                        name='EditingSnippetActionKeepRTError',
                        msg='Invalid range (%s)' % self.keep
                    )
            elif re.match(r'\w+(,\w+)*', item):
                var_names = ['v%s' % i if i.isdigit() else i for i in item.split(',')]

            for var_name in var_names:  # noqa
                index, node = self.find_element(var_name)
                if index >= NUMBER.ZERO:
                    node.set_kept()
                    is_empty and node.set_empty()
                    self.is_keep_applied = True
                else:
                    self.raise_runtime_error(
                        name='EditingSnippetActionKeepRTError',
                        msg='Not found index (%s)' % var_name
                    )

    def apply_capture(self):
        if not self.capture:
            return

        items = re.split(PATTERN.SPACES, self.capture)
        for item in items:
            item = item.strip(',')
            is_empty = bool(re.search('[_-]?or([_-]empty)?', item, re.I))
            item = re.sub('[_-]?or([_-]empty)?', STRING.EMPTY, item, re.I)

            if re.match(r'\d+:\d+$', item):
                first, last = item.split(':', NUMBER.ONE)
                var_names = ['v%s' % i for i in range(int(first), int(last) + 1)]
                if not var_names:
                    self.raise_runtime_error(
                        name='EditingSnippetActionCaptureRTError',
                        msg='Invalid range (%s)' % self.capture
                    )
            elif re.match(r'\w+(,\w+)*', item):
                var_names = ['v%s' % i if i.isdigit() else i for i in item.split(',')]

            for var_name in var_names:  # noqa
                index, node = self.find_element(var_name)
                if index >= NUMBER.ZERO:
                    node.set_captured()
                    is_empty and node.set_empty()
                    self.is_capture_applied = True
                else:
                    self.raise_runtime_error(
                        name='EditingSnippetActionCaptureRTError',
                        msg='Not found index (%s)' % var_name
                    )

    def process(self):
        self.prepare()
        if self.action:
            self.apply_action()
        else:
            self.apply_capture()
            self.apply_keep()

    def to_snippet(self):
        new_snippet = str.join(
            STRING.EMPTY, [elmt.to_snippet() for elmt in self.snippet_elements]
        )
        new_snippet = '%s%s%s' % (self.leading, new_snippet, self.trailing)

        cval = STRING.EMPTY if self.is_capture_applied else self.capture
        kval = STRING.EMPTY if self.is_keep_applied else self.keep
        aval = STRING.EMPTY if self.is_action_applied else self.action

        fmt = 'capture(%s) keep(%s) action(%s): %s'
        new_snippet = fmt % (cval, kval, aval, new_snippet)

        return new_snippet

    def to_regex(self):
        pattern = str.join(
            STRING.EMPTY, [elmt.to_regex() for elmt in self.snippet_elements]
        )
        if self.is_leading:
            pattern = '%s%s' % (PATTERN.ZOSPACES, pattern)

        if self.is_trailing:
            pattern = '%s%s' % (pattern, PATTERN.ZOSPACES)

        return pattern

    def to_template_snippet(self):
        tmpl_snippet = str.join(
            STRING.EMPTY, [elmt.to_template_snippet() for elmt in self.snippet_elements]
        )
        if self.is_leading:
            tmpl_snippet = '%s%s' % (PATTERN.ZOSPACES, tmpl_snippet)

        if self.is_trailing:
            tmpl_snippet = '%s%s' % (tmpl_snippet, PATTERN.ZOSPACES)

        return tmpl_snippet


class IterativeLinePattern(LData):
    def __init__(self, line, label=''):
        super().__init__(line)
        pat = r'[\x20-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+'
        self.label = re.sub(pat, '_', str(label))
        self._snippet = STRING.EMPTY
        self.process()

    def __len__(self):
        chk = bool(len(self._snippet))
        return int(chk)

    def symbolize(self):
        spaces = re.findall(PATTERN.SPACES, self.data)
        lst = []
        for index, item in enumerate(re.split(PATTERN.SPACES, self.data)):
            node = TranslatedPattern.do_factory_create(item)
            var_ = 'v%s%s' % (self.label, index)

            item_snippet = node.get_readable_snippet(var=var_)
            lst.append(item_snippet)
            if index < len(spaces):
                lst.append(spaces[index])

        snippet = str.join(STRING.EMPTY, lst)
        fmt = 'capture() keep() action(): %s%s%s'
        editing_snippet = fmt % (self.leading, snippet, self.trailing)
        return editing_snippet

    def is_line_editable_snippet(self):
        pat = r'capture[(][^\)]*[)] keep[(][^\)]*[)] action[(][^\)]*[)]:.+'
        match = re.match(pat, self.data)
        chk = bool(match)
        return chk

    def process(self):
        if self.is_line_editable_snippet():
            node = EditingSnippet(self.data)
            self._snippet = node.to_snippet()
        else:
            self._snippet = self.symbolize()

    def to_snippet(self):
        node = EditingSnippet(self._snippet)
        snippet = node.to_snippet()
        return snippet

    def to_regex(self):
        node = EditingSnippet(self._snippet)
        pattern = node.to_regex()
        return pattern

    def to_template_snippet(self):
        node = EditingSnippet(self._snippet)
        tmpl_snippet = node.to_template_snippet()
        return tmpl_snippet

    def is_captured_in_regex(self):
        data = self.to_regex()
        pat = r'[(][?]P<\w+>'
        chk = bool(re.search(pat, data))
        return chk

    def is_captured_in_template_snippet(self):
        data = self.to_template_snippet()
        pat = r'\b\w+[(][^\)]* *var_\w+'
        chk = bool(re.search(pat, data))
        return chk


class IterativeLinesPattern(RuntimeException):
    def __init__(self, *lines_or_snippets):
        self.lines_or_snippets = Misc.get_list_of_readonly_lines(*lines_or_snippets)

    def to_snippet(self):
        lst = []
        for index, line_or_snippet in enumerate(self.lines_or_snippets):
            if Misc.is_data_line(line_or_snippet):
                label = str(index) if index > 0 else STRING.EMPTY
                node = IterativeLinePattern(line_or_snippet, label=label)
                snippet = node.to_snippet()
                lst.append(snippet)
            else:
                lst.append(line_or_snippet)
        snippets = str.join('\n', lst)
        return snippets

    def to_regex(self):
        lst = []
        for snippet in self.lines_or_snippets:
            if Misc.is_data_line(snippet):
                node = IterativeLinePattern(snippet)
                pattern = node.to_regex()
                lst.append(pattern)
            else:
                lst.append(r'[ \t\v]*')

        if lst:
            pattern = str.join(r'(%s)' % PATTERN.CRNL, lst)
            return pattern
        else:
            return STRING.EMPTY

    def to_template_snippet(self):
        lst = []
        is_captured = False
        for snippet in self.lines_or_snippets:
            if Misc.is_data_line(snippet):
                node = IterativeLinePattern(snippet)
                tmpl_snippet = node.to_template_snippet()
                is_captured |= node.is_captured_in_template_snippet()
                lst.append(tmpl_snippet)

        if not is_captured:
            self.raise_runtime_error(
                msg='CANT form template snippet because no captured variable is created'
            )

        template_snippet = str.join(STRING.NEWLINE, lst)
        return template_snippet


class BaseCategoryPattern(LData):
    pass


class CategorySepPattern(BaseCategoryPattern):
    def __init__(self, sep):
        super().__init__(sep)

    def to_regex(self):
        node = IterativeLinePattern(self.raw_data)
        pattern = node.to_regex()
        return pattern

    def to_template_snippet(self):
        tmpl_snippet = '%s%s%s' % (self.leading, TextPattern(self.data), self.trailing)
        return tmpl_snippet


class CategorySpacerPattern(BaseCategoryPattern):
    def __init__(self, is_empty=False):
        super().__init__(STRING.EMPTY)
        self.is_empty = is_empty

    def to_regex(self):
        pattern = PATTERN.ZOSPACES if self.is_empty else PATTERN.SPACES
        return pattern

    def to_template_snippet(self):
        tmpl_snippet = 'zospaces()' if self.is_empty else STRING.DOUBLE_SPACES
        return tmpl_snippet


class CategoryLeftDataPattern(BaseCategoryPattern):

    def __init__(self, data):
        super().__init__(data)

    def to_regex(self):
        pattern = TextPattern(self.raw_data)
        return pattern

    def to_template_snippet(self):
        return self.raw_data


class CategoryRightDataPattern(BaseCategoryPattern):

    def __init__(self, data, var_txt):
        super().__init__(data)
        symbol_n_space_pat = '[ %s' % PATTERN.SYMBOLS[NUMBER.ONE:]
        self.var_name = re.sub(symbol_n_space_pat, '_', var_txt).strip('_')

    @property
    def is_empty(self):
        chk = self.data == STRING.EMPTY
        return chk

    def to_regex(self):
        if self.data:
            pat_obj = TranslatedPattern.do_factory_create(self.data)
            pattern = pat_obj.get_regex_pattern(var=self.var_name)
        else:
            pattern = '(?P<%s>.*|)' % self.var_name

        return pattern

    def to_template_snippet(self):
        if self.data:
            pat_obj = TranslatedPattern.do_factory_create(self.data)
            tmpl_snippet = pat_obj.get_template_snippet(var=self.var_name)
        else:
            tmpl_snippet = 'something(var_%s, or_empty)' % self.var_name

        return tmpl_snippet


class CategoryLinePattern(BaseCategoryPattern):
    def __init__(self, line, count=1, separator=':'):
        super().__init__(line)
        self.count = count
        self.separator = separator
        self.left_data = STRING.EMPTY
        self.right_data = STRING.EMPTY
        self._lst = []
        self.process()

    def __len__(self):
        chk = len(self._lst)
        return chk

    @property
    def parsed(self):
        chk = bool(self)
        return chk

    def to_regex(self):
        result = [PATTERN.ZOSPACES if self.is_leading else STRING.EMPTY]
        prev_item = None
        is_last_item_empty = False
        item = None
        for item in self._lst:
            pat = item.to_regex()
            if isinstance(item, CategoryRightDataPattern):
                if item.is_empty and prev_item and not prev_item.is_trailing:
                    pat = '%s%s' % (PATTERN.ZOSPACES, pat)
            result.append(pat)
            prev_item = item
        else:
            if isinstance(item, CategoryRightDataPattern) and item.is_empty:
                is_last_item_empty = True

        if is_last_item_empty:
            result.append(PATTERN.ZOSPACES if self.is_trailing else STRING.EMPTY)

        pattern = str.join(STRING.EMPTY, result)
        replaced_pat = r'( +)(something[\(]var_\w+, or_empty[\)])'
        pattern = re.sub(replaced_pat, r'zospaces()\2', pattern)

        return pattern

    def to_template_snippet(self):
        result = [self.leading]
        prev_item = None
        item = None
        is_last_item_empty = False
        for item in self._lst:
            _snippet = item.to_template_snippet()
            if isinstance(item, CategoryRightDataPattern):
                if item.is_empty and prev_item and not prev_item.is_trailing:
                    _snippet = 'zospaces()%s' % _snippet
            result.append(_snippet)
            prev_item = item
        else:
            if isinstance(item, CategoryRightDataPattern) and item.is_empty:
                is_last_item_empty = True

        is_last_item_empty and result.append(self.trailing)

        tmpl_snippet = str.join(STRING.EMPTY, result)
        replaced_pat = r'( +)(something[\(]var_\w+, or_empty[\)])'
        tmpl_snippet = re.sub(replaced_pat, r'zospaces()\2', tmpl_snippet)

        return tmpl_snippet

    def get_remaining_chars_by_pos(self, char_pos, direction='right'):

        if self.data[char_pos] == STRING.SPACE_CHAR:
            return char_pos

        total, i, j = len(self.data), char_pos, char_pos
        while NUMBER.ZERO <= i < total:
            if self.data[i] == STRING.SPACE_CHAR:
                return j
            j = i
            i = i + NUMBER.ONE if direction == 'right' else i - NUMBER.ONE

    def get_word_by_pos(self, char_pos):
        most_right_pos = self.get_remaining_chars_by_pos(char_pos, direction='right')
        most_left_pos = self.get_remaining_chars_by_pos(char_pos, direction='left')

        word = self.data[most_left_pos:most_right_pos]
        return word

    def get_triple_by_separator(self):
        v1, v2 = str.split(self.data, self.separator, maxsplit=1)
        node1 = LData(v1)
        node2 = LData(v2)
        left = '%s%s' % (node1.leading, node1.data)
        right = '%s%s' % (node2.data, node2.trailing)
        separator = '%s%s%s' % (node1.trailing, self.separator, node2.leading)
        return left, separator, right

    def raise_exception_if_not_category_pattern(self):
        if self.separator not in self.data:
            self.raise_runtime_error(msg='data DOESNT have separator')

        index = self.data.index(self.separator)
        if index == NUMBER.ZERO:
            self.raise_runtime_error(msg='data DOESNT have var text')

        chk_word = self.get_word_by_pos(index)
        if self.is_time_ipv6_or_mac_addr_format(chk_word):
            self.raise_runtime_error(msg='unsupported var text')

    def is_time_ipv6_or_mac_addr_format(self, data):    # noqa
        mac_pat = r'[a-f\d]{1,2}(:[a-f\d]{1,2}){2,5}'
        ipv6_pat = r'[a-f\d]{1,4}(:([a-f\d]{1,4})?)+:[a-f\d]{1,4}'

        is_time = bool(re.search(r'\d+(:\d+)+', data))
        is_mac_addr = bool(re.match(mac_pat, data, re.I))
        is_ipv6 = data.endswith('::') or data.startswith('::')

        is_ipv6 = is_ipv6 or bool(re.match(ipv6_pat, data, re.I))
        chk = is_time or is_mac_addr or is_ipv6
        return chk

    def try_to_get_value(self):
        next_count = self.count - NUMBER.ONE
        if not next_count or not self.right_data.strip():
            return self.right_data, STRING.EMPTY
        else:
            try:
                node = self(self.right_data, count=next_count, separator=self.separator)
                left_data = node.left_data
                pat = PATTERN.ATLONESPACES if STRING.DOUBLE_SPACES in left_data else PATTERN.SPACES
                if STRING.SPACE_CHAR in left_data:
                    val, remaining = re.split(pat, self.right_data, maxsplit=1)
                    return val, remaining
                else:
                    return STRING.EMPTY, self.right_data
            except Exception as ex: # noqa
                items = re.split(PATTERN.SPACES, self.right_data)
                lst = []
                for item in items:
                    chk1 = item == self.separator
                    chk2 = not self.is_time_ipv6_or_mac_addr_format(item)
                    chk2 = chk2 and item.endswith(self.separator)
                    lst.append(TextPattern(item))
                    if chk1 and chk2:
                        break
                other_pat = str.join(PATTERN.SPACES, lst)
                match = re.search(other_pat, self.right_data)
                other_left = match.group()
                other_remaining = self.right_data[len(other_left):]

                if STRING.DOUBLE_SPACES in other_left:
                    pat = PATTERN.ATLONESPACES
                    other_first, other_last = re.split(pat, other_left, maxsplit=1)
                    return other_first, '%s%s' % (other_last, other_remaining)
                else:
                    lst.clear()
                    for item in items:
                        lst.append(item)
                        if self.is_time_ipv6_or_mac_addr_format(item):
                            break

                    other_pat = str.join(PATTERN.SPACES, lst)
                    match = re.search(other_pat, self.right_data)
                    other_left = match.group()
                    other_remaining = self.right_data[len(other_left):]
                    return other_left, other_remaining

    def process(self):
        if not self.count:
            return

        self.raise_exception_if_not_category_pattern()

        var_txt, whole_sep, remaining = self.get_triple_by_separator()
        self.left_data = var_txt
        self.right_data = remaining

        self._lst.append(CategoryLeftDataPattern(var_txt))
        self._lst.append(CategorySepPattern(whole_sep))

        val, other_remaining = self.try_to_get_value()

        value_node = CategoryRightDataPattern(val, var_txt)
        self._lst.append(value_node)

        if other_remaining:
            try:
                other_node = self(other_remaining, count=self.count-1)
                if other_node.parsed:
                    self._lst.append(CategorySpacerPattern())
                    self._lst.append(other_node)
                else:
                    return
            except Exception as ex: # noqa
                return


class CategoryLinesPattern(RuntimeException):
    def __init__(self, *lines, options=None, count=1, separator=':'):
        self.lines = Misc.get_list_of_lines(*lines)
        self.options = options or dict()
        self.count = count
        self.separator = separator
        self.kwargs = dict(count=self.count, separator=self.separator)
        self._lst = []
        self.process()

    @property
    def is_category_format(self):
        chk = any(isinstance(item, CategoryLinePattern) for item in self._lst)
        return chk

    def __len__(self):
        chk = self.is_category_format
        return chk

    def process(self):
        for index, line in enumerate(self.lines):
            try:
                kwargs = self.options.get(str(index), self.kwargs)
                node = CategoryLinePattern(line, **kwargs)
                if node.parsed:
                    self._lst.append(node)
                else:
                    self._lst.append(line)
            except Exception as ex: # noqa
                self._lst.append(line)

    def raise_exception_if_not_category_format(self):
        if not self.is_category_format:
            self.raise_runtime_error(msg='text is not category format')

    def to_regex(self):
        self.raise_exception_if_not_category_format()

        result = []
        for item in self._lst:
            if isinstance(item, CategoryLinePattern):
                result.append(item.to_regex())
            else:
                result.append(TextPattern(item))
        pattern = str.join('(%s)' % PATTERN.CRNL, result)
        return pattern

    def to_template_snippet(self):
        self.raise_exception_if_not_category_format()
        result = []
        for item in self._lst:
            if isinstance(item, CategoryLinePattern):
                result.append(item.to_template_snippet())
            else:
                result.append(item)
        tmpl_snippet = str.join(STRING.NEWLINE, result)
        return tmpl_snippet


class TabularTextPattern(RuntimeException):
    def __init__(self, *lines, divider='', columns_count=0, col_widths=None,
                 header_names=None, headers_data=None, custom_headers_data='',
                 starting_from=None, ending_to=None):
        self.lines = Misc.get_list_of_lines(*lines)
        self.kwargs = dict(
            divider=divider,
            columns_count=columns_count,
            col_widths=col_widths,
            header_names=header_names,
            headers_data=headers_data,
            custom_headers_data=custom_headers_data
        )

        self.starting_from = starting_from
        self.ending_to = ending_to
        self.parser = None
        self.process()

    def __len__(self):
        chk = bool(self.parser)
        return chk

    def process(self):
        lines = self.lines[self.starting_from:self.ending_to]
        is_col_widths = bool(self.kwargs.get('col_widths'))
        cls = TabularTextPatternByFixedColumns if is_col_widths else TabularTextPatternByVarColumns
        self.parser = cls(*lines, **self.kwargs)

    def to_regex(self):
        pattern = self.parser.to_regex() if self.parser else STRING.EMPTY
        return pattern

    def to_template_snippet(self):
        tmpl_snippet = self.parser.to_template_snippet() if self.parser else STRING.EMPTY
        return tmpl_snippet


class TabularTextPatternByFixedColumns(RuntimeException):
    def __init__(self, *lines, col_widths=None, header_names=None, headers_data=None, **kwargs):
        self.lines = Misc.get_list_of_lines(*lines)
        self.col_widths = col_widths
        self.columns_count = len(col_widths) if Misc.is_list(col_widths) else NUMBER.ZERO
        self.raise_exception_if_columns_widths_not_provided()
        self.headers_data = headers_data
        self.raw_headers_data = []
        self.header_names = header_names
        self.variables = []
        self.kwargs = kwargs
        self.parse_headers()

    def __len__(self):
        return bool(self.columns_count)

    def get_default_variables(self):
        var_names = ['col%s' % i for i in range(self.columns_count)]
        return var_names

    def parse_headers_by_ref_data(self, reference_data):
        variables = []
        if not reference_data:
            return variables

        pat = '[0-9]+( *, *[0-9]+ *)*$'
        headers_lines = []
        if Misc.is_string(reference_data):
            if re.match(pat, reference_data):
                for i in str.split(reference_data, STRING.COMMA_CHAR):
                    index = int(i)
                    headers_lines.append(self.lines[index])
            else:
                headers_lines.extend(Misc.get_list_of_lines(reference_data))
        elif Misc.is_list(reference_data):
            for line in reference_data:
                is_number, pos = Misc.try_to_get_number(line, return_type=int)
                if is_number:
                    headers_lines.append(self.lines[pos])
                else:
                    headers_lines.append(line)
        else:
            variables = self.get_default_variables()
            return variables

        self.raw_headers_data.extend(headers_lines)

        pat = self.build_pattern()

        keys = self.get_default_variables()
        vals = [STRING.EMPTY] * self.columns_count
        tbl = OrderedDict(zip(keys, vals))
        for line in headers_lines:
            match = re.match(pat, line)
            if match:
                for key, val in match.groupdict().items():
                    val = val.strip()
                    prev_val = tbl.get(key)
                    tbl[key] = '%s %s' % (prev_val, val) if prev_val else val

        headers = list(tbl.values())
        variables = self.parse_headers_to_variables(headers)
        return variables

    def parse_headers_to_variables(self, header_names):
        variables = []
        if not header_names:
            return variables

        if Misc.is_string(header_names):
            header_names = re.split('[ ,]+', header_names.strip())

        if Misc.is_list(header_names) and len(header_names) == self.columns_count:
            repl = STRING.UNDERSCORE_CHAR
            for i, hdr in enumerate(header_names):
                new_hdr = re.sub(PATTERN.MULTI_SPACE_SYMBOLS, repl, hdr.strip())
                new_hdr = new_hdr if new_hdr == repl else new_hdr.rstrip(repl)
                if new_hdr in variables:
                    variables.append('%s%s' % (new_hdr, i))
                else:
                    variables.append(new_hdr)
        else:
            variables = self.get_default_variables()

        return variables

    def parse_headers(self):
        if self.header_names or self.headers_data:
            if self.header_names:
                self.variables = self.parse_headers_to_variables(self.header_names)
            else:
                self.variables = self.parse_headers_by_ref_data(self.headers_data)
        else:
            self.variables = self.get_default_variables()

    def build_pattern(self, is_default=True):
        lst = []
        for i in range(self.columns_count):
            col_width = int(self.col_widths[i])
            var_name = 'col%s' % i if is_default else self.variables[i]
            if i < self.columns_count - NUMBER.ONE:
                pat = '(?P<%s>.{%s})' % (var_name, col_width)
            else:
                pat = '(?P<%s>.*)' % var_name
            lst.append(pat)
        pattern = str.join(STRING.EMPTY, lst)
        return pattern

    def raise_exception_if_columns_widths_not_provided(self):
        if not self:
            self.raise_runtime_error(msg='col_widths MUST be provided')

    def to_regex(self):
        pattern = self.build_pattern(is_default=False)
        return pattern

    def to_template_snippet(self):
        lst = []
        for i, var_name in enumerate(self.variables):
            if i < self.columns_count - NUMBER.ONE:
                width = self.col_widths[i]
                sub_snippet = 'anything(var_%s, repetition_%s)' % (var_name, width)
                lst.append(sub_snippet)
            else:
                sub_snippet = 'something(var_%s)' % var_name
                lst.append(sub_snippet)
        snippet = '%s -> record' % str.join(STRING.EMPTY, lst)
        tmpl_snippet = str.join(STRING.NEWLINE, self.raw_headers_data + [snippet])
        return tmpl_snippet


class TabularTextPatternByVarColumns(RuntimeException):
    def __init__(self, *lines, divider='', columns_count=0,
                 header_names=None, headers_data=None, custom_headers_data='',
                 **kwargs):
        self._is_leading = None
        self._is_trailing = None
        self._is_start_with_divider = None
        self._is_end_with_divider = None

        self.lines = Misc.get_list_of_lines(*lines)
        self.total_lines = len(self.lines)
        self.divider = divider
        self.columns_count = columns_count
        self.raise_exception_if_columns_count_not_provided()
        self.headers_data = headers_data
        self.custom_headers_data = custom_headers_data
        self.raw_headers_data = []
        self.header_names = header_names
        self.variables = []

        self.kwargs = kwargs

        self.prepare_headers_data()

    def __len__(self):
        return bool(self.columns_count)

    @property
    def is_leading(self):
        if not self.total_lines:
            return False

        if self._is_leading is None:
            for line in self.lines:
                self._is_leading = Misc.is_leading_line(line)
                if self._is_leading:
                    break
        return self._is_leading

    @property
    def is_trailing(self):
        if not self.total_lines:
            return False

        if self._is_trailing is None:
            for line in self.lines:
                self._is_trailing = Misc.is_trailing_line(line)
                if self._is_trailing:
                    break
        return self._is_trailing

    @property
    def is_divider_a_symbol(self):
        chk = bool(re.match(PATTERN.CHECK_SYMBOL, self.divider))
        return chk

    @property
    def is_start_with_divider(self):
        if self._is_start_with_divider is None:
            if self.is_divider_a_symbol:
                count = 0
                for line in self.lines:
                    if line.strip().startswith(self.divider):
                        count += 1

                lines_count = len(self.lines)
                if count:
                    # chk = count > lines_count / NUMBER.TWO
                    chk = op.gt(count, op.truediv(lines_count, NUMBER.TWO))
                    self._is_start_with_divider = chk
                else:
                    self._is_start_with_divider = False
            else:
                self._is_start_with_divider = False
        return self._is_start_with_divider

    @property
    def is_end_with_divider(self):
        if self._is_end_with_divider is None:
            if self.is_divider_a_symbol:
                count = 0
                for line in self.lines:
                    if line.strip().endswith(self.divider):
                        count += 1

                lines_count = len(self.lines)
                if count:
                    # chk = count > lines_count / NUMBER.TWO
                    chk = op.gt(count, op.truediv(lines_count, NUMBER.TWO))
                    self._is_end_with_divider = chk
                else:
                    self._is_end_with_divider = False
            else:
                self._is_end_with_divider = False
        return self._is_end_with_divider

    def raise_exception_if_columns_count_not_provided(self):
        if not self:
            self.raise_runtime_error(msg='columns_count CANT be zero')

    def prepare_headers_data(self):
        lst = self.raw_headers_data
        data = self.headers_data
        total_lines = len(self.lines)
        if Misc.is_string(data):
            pat = ' *[0-9]+([ ,]+[0-9]+)* *$'
            if re.match(pat, data):
                for index in re.split('[ ,]+', data):
                    index = int(index)
                    if index < total_lines:
                        hdr_line = self.lines[index]
                        hdr_line not in lst and lst.append(hdr_line)
            else:
                for sub_line in str.splitlines(data):
                    for line in self.lines:
                        sub_line in line and line not in lst and lst.append(line)

        elif Misc.is_list(data):
            for item in data:
                is_number, index = Misc.try_to_get_number(item, return_type=int)
                if is_number and index < total_lines:
                    hdr_line = self.lines[index]
                    hdr_line not in lst and lst.append(hdr_line)
                else:
                    for line in self.lines:
                        item in line and line not in lst and lst.append(line)

    def parse_headers_to_variables(self):
        variables = []
        header_names = self.header_names
        if not header_names:
            return variables

        if Misc.is_string(header_names):
            header_names = re.split('[ ,]+', header_names.strip())

        if Misc.is_list(header_names) and len(header_names) == self.columns_count:
            pat = '[ %s' % PATTERN.SYMBOLS[1:]
            repl = STRING.UNDERSCORE_CHAR
            for i, hdr in enumerate(header_names):
                new_hdr = re.sub(pat, repl, hdr.strip())
                new_hdr = new_hdr if new_hdr == repl else new_hdr.rstrip(repl)
                if new_hdr in variables:
                    variables.append('%s%s' % (new_hdr, i))
                else:
                    variables.append(new_hdr)

        return variables

    def get_default_variables(self):  # noqa
        var_names = ['col%s' % i for i in range(self.columns_count)]
        return var_names

    def find_ref_row_by_symbols_divider(self, custom_line=''):
        fmt = ' *%(p)s( +%(p)s){%(rep)s} *$'
        repetition = self.columns_count - NUMBER.ONE
        pat = fmt % dict(p=PATTERN.SYMBOLS, rep=repetition)

        if custom_line:
            found_line = custom_line
        else:
            found_lines = [line for line in self.lines if re.match(pat, line)]
            found_line = found_lines[NUMBER.ZERO] if found_lines else STRING.EMPTY
            if not found_line:
                return None

        pattern = ' *%s *' % PATTERN.SYMBOLS
        ref_row = TabularRow.create_ref_row(
            found_line, pattern,
            case='findall',
            columns_count=self.columns_count
        )
        return ref_row

    def find_ref_row_by_separator_divider(self, custom_line=''):
        fmt = ' *%(sep)s?(%(p)s%(sep)s){%(rep)s}%(p)s%(sep)s? *$'
        kwargs = dict(
            p=r'[^%s]+' % self.divider,
            rep=self.columns_count - NUMBER.ONE,
            sep=re.escape(self.divider)
        )
        pat = fmt % kwargs

        if custom_line:
            found_line = custom_line
        else:
            found_lines = [line for line in self.lines if re.match(pat, line)]
            found_line = found_lines[NUMBER.ZERO] if found_lines else STRING.EMPTY
            if not found_line:
                return None

        ref_row = TabularRow.create_ref_row(
            found_line, self.divider,
            columns_count=self.columns_count,
            case='split'
        )
        return ref_row

    def find_ref_row_by_space_divider(self, spaces=' ', custom_line=''):
        repetition = self.columns_count - NUMBER.ONE
        kwargs = dict(
            p=PATTERN.NON_WHITESPACES_OR_PHRASE,
            rep=repetition,
        )
        fmt1 = ' *%(p)s( +%(p)s){%(rep)s} *$'
        fmt2 = ' *%(p)s(  +%(p)s){%(rep)s} *$'
        fmt = fmt1 if spaces == STRING.SPACE_CHAR else fmt2
        pat = fmt % kwargs

        if custom_line:
            found_line = custom_line
        else:
            found_lines = [line for line in self.lines if re.match(pat, line)]
            if not found_lines:
                return None
            found_line = found_lines[NUMBER.ZERO]

        pattern = ' *%s  +' % PATTERN.NON_WHITESPACES_OR_PHRASE
        ref_row = TabularRow.create_ref_row(
            found_line, pattern,
            columns_count=self.columns_count,
            case='finditer'
        )
        return ref_row

    def find_ref_row_by_blank_space_divider(self):
        ref_row = self.find_ref_row_by_space_divider()
        return ref_row

    def find_ref_row_by_multi_spaces_divider(self):
        ref_row = self.find_ref_row_by_space_divider(spaces='  ')
        return ref_row

    def find_ref_row_by_custom_headers_line(self):
        ref_row = self.find_ref_row_by_symbols_divider(custom_line=self.custom_headers_data)
        return ref_row

    def try_to_get_table_by_divider(self, case):
        methods = dict(
            symbols=self.find_ref_row_by_symbols_divider,
            separator=self.find_ref_row_by_separator_divider,
            multi_spaces=self.find_ref_row_by_multi_spaces_divider,
            blank_space=self.find_ref_row_by_blank_space_divider,
            custom=self.find_ref_row_by_custom_headers_line
        )
        default_method = self.find_ref_row_by_blank_space_divider
        ref_row = methods.get(case, default_method)()
        if ref_row:
            header_names = self.parse_headers_to_variables()
            table = TabularTable(
                *self.lines, ref_row=ref_row, divider=self.divider,
                header_names=header_names,
                raw_headers_data=self.raw_headers_data,
                is_leading=self.is_leading, is_trailing=self.is_trailing,
                is_start_with_divider=self.is_start_with_divider,
                is_end_with_divider=self.is_end_with_divider
            )
            return True, table
        else:
            return False, None

    def parse_table(self):
        case, err_msg = STRING.EMPTY, STRING.EMPTY
        if re.match('%s$' % PATTERN.SYMBOL, self.divider.strip()):
            case = 'separator'
            err_msg = 'Failed to parse tabular text by %r divider' % self.divider
        elif self.custom_headers_data:
            case = 'custom'
            err_msg = 'Failed to parse tabular text by custom headers data'
        elif self.divider == STRING.SPACE_CHAR:
            case = 'blank_space'
            err_msg = 'Failed to parse tabular text by blank space divider'
        elif re.match('  +$', self.divider):
            case = 'multi_spaces'
            err_msg = 'Failed to parse tabular text by multi-space divider'
        elif self.divider == STRING.EMPTY:
            case = 'symbols'
            err_msg = 'Failed to parse tabular text by symbols divider'
        else:
            msg = 'Unsupported divider %r' % self.divider
            self.raise_runtime_error(msg=msg)

        is_parsed, table = self.try_to_get_table_by_divider(case)
        if is_parsed:
            return table
        else:
            self.raise_runtime_error(msg=err_msg)

    def to_regex(self):
        table = self.parse_table()
        if not table:
            msg = ('CANT build regex pattern because provided '
                   'text might not be tabular text format')
            self.raise_runtime_error(msg=msg)
        pattern = table.to_regex()
        return pattern

    def to_template_snippet(self):
        table = self.parse_table()
        if not table:
            msg = ('CANT build template snippet because provided '
                   'text might not be tabular text format')
            self.raise_runtime_error(msg=msg)
        template_snippet = table.to_template_snippet()
        return template_snippet


class TabularCell(RuntimeException):
    def __init__(self, line, left_pos, right_pos, ref_cell=None):
        self.args = (line, left_pos, right_pos, ref_cell)

        self._leading = None
        self._trailing = None

        self.left = NUMBER.ZERO
        self.right = NUMBER.ZERO
        self.inner_left = NUMBER.ZERO
        self.inner_right = NUMBER.ZERO

        self.line = STRING.EMPTY
        self.data = STRING.EMPTY

        self.ref_cell = None

        self.process()

    def __len__(self):
        chk = self.left >= NUMBER.ZERO
        chk = chk and self.right > self.left
        return chk

    def __repr__(self):
        fmt = '%s(text=%r, data=%r, left=%s, right=%s)'
        cls_name = Misc.get_instance_class_name(self)
        result = fmt % (cls_name, self.text, self.data, self.left, self.right)
        return result

    @property
    def text(self):
        return self.data.strip()

    @property
    def leading(self):
        if self._leading is None:
            leading_spaces = Misc.get_leading_line(self.data)
            self._leading = leading_spaces
        return self._leading or STRING.EMPTY

    @property
    def trailing(self):
        if self._trailing is None:
            if self.is_empty:
                self._trailing = STRING.EMPTY
            else:
                lst = re.findall(PATTERN.SPACESATEOS, self.data)
                self._trailing = lst[NUMBER.ZERO] if lst else STRING.EMPTY
        return self._trailing or STRING.EMPTY

    @property
    def is_leading(self):
        chk = self.leading != STRING.EMPTY
        return chk

    @property
    def is_single_leading(self):
        chk = self.leading == STRING.SPACE_CHAR
        return chk

    @property
    def is_multi_leading(self):
        chk = len(self.leading) > NUMBER.ONE
        return chk

    @property
    def is_trailing(self):
        chk = self.trailing != STRING.EMPTY
        return chk

    @property
    def is_single_trailing(self):
        chk = self.trailing == STRING.SPACE_CHAR
        return chk

    @property
    def is_multi_trailing(self):
        chk = len(self.trailing) > NUMBER.ONE
        return chk

    @property
    def is_empty(self):
        chk = self.text == STRING.EMPTY
        return chk

    @property
    def is_just_chars(self):
        if self.is_empty:
            return False
        chk = STRING.SPACE_CHAR not in self.text
        return chk

    @property
    def is_group_of_chars(self):
        if self.is_empty:
            return False
        chk = STRING.SPACE_CHAR in self.text
        return chk

    @property
    def is_not_containing_space(self):
        chk = STRING.SPACE_CHAR not in self.text
        return chk

    @property
    def is_containing_space(self):
        chk = STRING.SPACE_CHAR in self.text
        return chk

    @property
    def items_count(self):
        if self.is_empty:
            return NUMBER.ZERO
        else:
            lst = re.split(PATTERN.SPACES, self.text)
            count = len(lst)
            return count

    @property
    def width(self):
        width = len(self.data)
        return width

    @property
    def is_containing_spaces(self):
        chk = STRING.DOUBLE_SPACES in self.text
        return chk

    def update_position(self, attr, val=0):
        attr = 'left' if attr.lower() == 'left' else 'right'
        setattr(self, attr, val)
        self.process()

    def get_possible_prefix(self):
        if self.is_empty or self.is_trailing:
            return STRING.EMPTY
        else:
            *chk, prefix = self.text.rsplit(STRING.SPACE_CHAR, maxsplit=NUMBER.ONE)
            return STRING.EMPTY if chk else prefix

    def get_postfix_data(self):
        if self.is_multi_trailing or not self.is_containing_space:
            return STRING.EMPTY

        spaces = STRING.DOUBLE_SPACES
        space = STRING.SPACE_CHAR
        repl = spaces if self.is_containing_spaces else space
        _, remaining_txt = str.rsplit(self.text, repl, maxsplit=NUMBER.ONE)
        ret_val = Misc.join_string(remaining_txt, self.trailing)

        if self.ref_cell:
            other_right = self.right - len(ret_val)
            if other_right > self.ref_cell.inner_right:
                return ret_val
            else:
                if space in remaining_txt:
                    _, remaining_txt1 = str.rsplit(remaining_txt, space, maxsplit=NUMBER.ONE)
                    ret_val = Misc.join_string(remaining_txt1, self.trailing)
                    return ret_val
                else:
                    return STRING.EMPTY
        else:
            return ret_val

    def do_first_pass_adjustment(self, prev_cell=None):
        if not isinstance(prev_cell, self.__class__):
            # skip adjustment
            return

        prefix = prev_cell.get_possible_prefix()
        prefix_length = len(prefix)
        if not self.is_leading and prefix:
            self.left = self.left - prefix_length
            prev_cell.right = prev_cell.right - prefix_length
            self.process()
            prev_cell.process()

    def readjust(self, prev_cell=None):
        if not isinstance(prev_cell, self.__class__):
            # skip adjustment
            return

        chk1 = prev_cell.is_multi_trailing
        chk2 = prev_cell.is_empty
        chk3 = prev_cell.is_single_trailing and self.is_leading

        if chk1 or chk2 and chk3:
            # skip adjustment
            return
        else:
            prefix = prev_cell.get_postfix_data()
            if prefix:
                width = len(prefix) + NUMBER.ONE
                self.update_position('left', val=self.left-width)
                prev_cell.update_position('right', val=self.right-width)
            else:
                # skip adjustment
                return

    def process(self):
        line, left_pos, right_pos, ref_cell = self.args

        is_left, left = Misc.try_to_get_number(left_pos, return_type=int)
        is_right, right = Misc.try_to_get_number(right_pos, return_type=int)

        not is_left and self.raise_runtime_error(msg='left position must be integer')
        not is_right and self.raise_runtime_error(msg='right position must be integer')

        self._leading = None
        self._trailing = None

        if isinstance(ref_cell, self.__class__) or ref_cell is None:
            self.ref_cell = ref_cell
        else:
            cls_name = Misc.get_instance_class_name(self)
            self.raise_runtime_error(msg='invalid ref_cell type (%s)' % cls_name)

        self.left = left
        self.right = len(line) if self.ref_cell and right == 999999 else right
        self.line = line
        self.data = self.line[self.left:self.right]

        self.inner_left = self.left + len(self.leading)
        self.inner_right = self.right - len(self.trailing)


class TabularRow(RuntimeException):
    def __init__(self, line, ref_row=None, aligned=True):
        self._is_symbols_group = None
        self.aligned = aligned
        self.line = line
        self.ref_row = ref_row
        self.cells = []
        self.process()

    def __len__(self):
        chk = bool(self.cells)
        return chk

    def __repr__(self):
        fmt = '%s(columns_count=%s)'
        cls_name = Misc.get_instance_class_name(self)
        result = fmt % (cls_name, len(self.cells))
        return result

    @property
    def cells_count(self):
        total = len(self.cells)
        return total

    @property
    def columns_count(self):
        return self.cells

    @property
    def is_group_of_symbols(self):
        if self._is_symbols_group is None:
            if self.cells:
                fmt = ' *%(p)s( +%(p)s)* *$'
                pat = fmt % dict(p=PATTERN.SYMBOLS)
                match = re.match(pat, self.line)
                self._is_symbols_group = bool(match)
            else:
                return False
        return self._is_symbols_group

    def append_new_cell(self, left_pos, right_pos):
        index = len(self.cells)
        ref_cell = self.ref_row.cells[index] if self.ref_row else None
        cell = TabularCell(self.line, left_pos, right_pos, ref_cell=ref_cell)
        if self.ref_row:
            prev_cell = self.cells[-NUMBER.ONE] if index else None
            self.ref_row.aligned and cell.do_first_pass_adjustment(prev_cell=prev_cell)
        self.cells.append(cell)
        return cell

    def process(self):
        self.cells.clear()
        if self.ref_row:
            for ref_cell in self.ref_row.cells:
                left_pos, right_pos = ref_cell.left, ref_cell.right
                self.append_new_cell(left_pos, right_pos)

    @classmethod
    def do_creating_ref_row(cls, line, pattern, lst, aligned=True):

        if not lst:
            RuntimeException.do_raise_runtime_error(
                obj=Misc.join_string(cls.__name__, 'RTError'),
                msg='Failed to parse\nPattern: %r\nLine: %r' % (pattern, line)
            )

        ref_row = cls(line, aligned=aligned)

        prev_right = 0
        cell = None
        for item in lst:
            left = prev_right
            prev_right = str.index(line, item) if cell is None else prev_right
            right = prev_right + len(item)
            prev_right = right
            cell = ref_row.append_new_cell(left, right)
        else:
            if cell:
                cell.right = 999999

        return ref_row

    @classmethod
    def do_creating_ref_row_by_findall(cls, line, pattern, columns_count=-1):
        lst = re.findall(pattern, line)

        total = len(lst)
        if columns_count > 0 and columns_count != total:
            fmt = ('(Parsed columns: %s) != (expected columns: %s)\n'
                   'Pattern: %r\nLine: %r')
            RuntimeException.do_raise_runtime_error(
                obj=Misc.join_string(cls.__name__, 'RTError'),
                msg=fmt % (total, columns_count, pattern, line)
            )

        ref_row = cls.do_creating_ref_row(line, pattern, lst)
        return ref_row

    @classmethod
    def do_creating_ref_row_by_splitting(cls, line, pattern, columns_count=1):
        separator = pattern
        pattern = re.escape(separator)
        lst = re.split(pattern, line)
        total = len(lst)
        if total == columns_count + NUMBER.TWO:
            prefix, first = lst.pop(NUMBER.ZERO), lst.pop(NUMBER.ZERO)
            new_first = Misc.join_string(prefix, first, sep=separator)
            lst.insert(NUMBER.ZERO, new_first)

            postfix, last = lst.pop(), lst.pop()
            new_last = Misc.join_string(last, postfix, sep=separator)
            lst.append(new_last)
            total = len(lst)

        elif total == columns_count + NUMBER.ONE:
            if line.strip().startswith(separator):
                prefix, first = lst.pop(NUMBER.ZERO), lst.pop(NUMBER.ZERO)
                new_first = Misc.join_string(prefix, first, sep=separator)
                lst.insert(NUMBER.ZERO, new_first)
            elif line.strip().endswith(separator):
                postfix, last = lst.pop(), lst.pop()
                new_last = Misc.join_string(last, postfix, sep=separator)
                lst.append(new_last)

            total = len(lst)

        if columns_count > 0 and columns_count != total:
            fmt = ('(Parsed columns: %s) != (expected columns: %s)\n'
                   'Pattern: %r\nLine: %r')
            RuntimeException.do_raise_runtime_error(
                obj=Misc.join_string(cls.__name__, 'RTError'),
                msg=fmt % (total, columns_count, pattern, line)
            )

        ref_row = cls.do_creating_ref_row(line, pattern, lst, aligned=False)
        return ref_row

    @classmethod
    def do_creating_ref_row_by_finditer(cls, line, pattern, columns_count=1):
        lst = []
        item = None
        for item in re.finditer(pattern, line):
            txt = item.group()
            lst.append(txt)
        else:
            if item:
                post_txt = line[item.end():]
                post_txt.strip() and lst.append(post_txt)

        if len(lst) > columns_count:
            index = columns_count - NUMBER.ONE
            last_sub_lst = lst[index:]
            lst = lst[:index]
            lst.append(Misc.join_string(*last_sub_lst))

        ref_row = cls.do_creating_ref_row(line, pattern, lst)
        return ref_row

    @classmethod
    def create_ref_row(cls, line, pattern, case='', columns_count=-1):
        args = (line, pattern)
        kwargs = dict(columns_count=columns_count)
        if case == 'findall':
            ref_row = cls.do_creating_ref_row_by_findall(*args, **kwargs)
            return ref_row
        elif case == 'finditer':
            ref_row = cls.do_creating_ref_row_by_finditer(*args, **kwargs)
            return ref_row
        elif case == 'split':
            ref_row = cls.do_creating_ref_row_by_splitting(*args, **kwargs)
            return ref_row
        else:
            RuntimeException.do_raise_runtime_error(
                obj=Misc.join_string(cls.__name__, 'RTError'),
                msg='Unsupported %r case create_ref_row' % case
            )


class TabularTable(RuntimeException):
    def __init__(self, *lines, ref_row=None, divider='',
                 header_names=None, raw_headers_data=None,
                 is_leading=False, is_trailing=False,
                 is_start_with_divider=False, is_end_with_divider=False):
        self.lines = Misc.get_list_of_lines(*lines)
        self.ref_row = ref_row
        self.divider = divider

        self.rows = []
        self.columns = []
        self.header_lines = []
        self.header_columns = []
        self.header_names = header_names or []
        self.raw_headers_data = raw_headers_data or []
        self.is_leading = is_leading
        self.is_trailing = is_trailing
        self.is_start_with_divider = is_start_with_divider
        self.is_end_with_divider = is_end_with_divider

        self.process()

    def __len__(self):
        chk = bool(self.rows) and bool(self.columns)
        return chk

    def __repr__(self):
        fmt = '%s(rows_count=%s, columns_count=%s)'
        cls_name = Misc.get_instance_class_name(self)
        result = fmt % (cls_name, len(self.rows), len(self.columns))
        return result

    @property
    def rows_count(self):
        total = len(self.rows)
        return total

    @property
    def columns_count(self):
        total = len(self.columns)
        return total

    def add_data_to_rows(self):
        self.rows.clear()
        for line in self.lines:
            row = TabularRow(line, ref_row=self.ref_row)
            self.rows.append(row)

    def add_data_to_columns(self):
        self.columns.clear()
        is_created = False

        for row in self.rows:
            prev_column = None
            for index, cell in enumerate(row.cells):
                new_col = TabularColumn(index=index)
                column = self.columns[index] if is_created else new_col
                not is_created and self.columns.append(column)
                column.left_column = prev_column
                column.append_cell(cell)

                if prev_column:
                    prev_column.right_column = column

                prev_column = column
            is_created = True
        for col in self.columns:
            col.analyze_and_update_alignment()

    def to_list_of_dict(self):
        lst_of_dict = []
        divider = self.divider
        for row_index, row in enumerate(self.rows):
            if row.is_group_of_symbols:
                continue
            dict_obj = dict()
            lst_of_dict.append(dict_obj)
            for col in self.columns:
                txt = col.cells[row_index].data.strip()
                txt = txt.strip(divider).strip() if divider else txt
                dict_obj[col.name] = txt
        return lst_of_dict

    def do_cleaning_data(self):
        if not self.ref_row:
            return

        ref_line = self.ref_row.line
        if ref_line in self.lines:
            row_pos = self.lines.index(ref_line)
            self.rows = self.rows[row_pos + NUMBER.ONE:]
            self.header_lines = self.lines[:row_pos + NUMBER.ONE]
            for col in self.columns:
                hdr_col = TabularColumn()
                hdr_col.cells = col.cells[:row_pos + NUMBER.ONE]
                self.header_columns.append(hdr_col)
                col.cells = col.cells[row_pos + NUMBER.ONE:]

    def build_and_update_headers(self):
        if not self.header_names:
            repl_char = STRING.UNDERSCORE_CHAR
            for index, hdr_col in enumerate(self.header_columns):
                col_name = str.join(repl_char, [cell.text for cell in hdr_col.cells])
                col_name = re.sub(PATTERN.MULTI_SPACE_SYMBOLS, repl_char, col_name)
                col_name = col_name.strip(repl_char).lower()
                self.header_names.append(col_name)
                self.columns[index].name = col_name

    def process(self):
        self.add_data_to_rows()
        self.add_data_to_columns()
        self.do_cleaning_data()
        self.build_and_update_headers()

    def to_regex(self):
        if not self:
            return STRING.EMPTY

        lst = []
        does_prev_col_has_empty_cell = False
        is_divider = bool(self.divider.strip())
        divider_pat = ' *%s *' % re.escape(self.divider)
        divider_leading_pat = '%s *' % re.escape(self.divider)
        divider_trailing_pat = ' *%s' % re.escape(self.divider)
        for column in self.columns:
            has_empty_cell = does_prev_col_has_empty_cell or column.has_empty_cell
            if is_divider:
                lst and lst.append(divider_pat)
            else:
                sep_pat = PATTERN.SPACE if has_empty_cell else PATTERN.SPACES
                lst and lst.append(sep_pat)
            col_pat = column.to_regex()
            lst.append(col_pat)
            does_prev_col_has_empty_cell = column.has_empty_cell

        self.is_start_with_divider and lst.insert(NUMBER.ZERO, divider_leading_pat)
        self.is_leading and lst.insert(NUMBER.ZERO, PATTERN.ZOSPACES)
        self.is_end_with_divider and lst.append(divider_trailing_pat)
        self.is_trailing and lst.append(PATTERN.ZOSPACES)
        pattern = Misc.join_string(*lst)
        return pattern

    def get_header_lines_snippet(self):
        headers_lines = self.raw_headers_data if self.raw_headers_data else self.header_lines

        lst = []
        for line in Misc.get_list_of_lines(*headers_lines):
            is_line_of_symbols = bool(re.match(PATTERN.CHECK_SYMBOLS_GROUP, line))
            is_header_line = Misc.is_data_line(line) and not is_line_of_symbols
            is_header_line and lst.append(line)

        snippet = Misc.join_string(*lst, sep=STRING.NEWLINE)
        return snippet

    def to_template_snippet(self):
        if not self:
            return STRING.EMPTY

        lst = []
        other_lst = []
        lst_of_column_status = []
        lst_of_snippet = []
        does_prev_col_has_empty_cell = False
        is_divider = bool(self.divider.strip())
        divider_snippet = 'zospaces()%szospaces()' % re.escape(self.divider)
        divider_leading_snippet = '%szospaces()' % re.escape(self.divider)
        divider_trailing_snippet = 'zospaces()%s' % re.escape(self.divider)

        pre_leading_data = 'start(space) ' if self.is_leading else 'start() '
        post_trailing_data = ' end(space) -> record' if self.is_trailing else ' end() -> record'

        for column in self.columns:
            has_empty_cell = does_prev_col_has_empty_cell or column.has_empty_cell
            lst_of_column_status.append(column.has_empty_cell)

            if is_divider:
                lst and lst.append(divider_snippet)
                other_lst and other_lst.append(divider_snippet)
            else:
                sep_snippet = STRING.SPACE_CHAR if has_empty_cell else STRING.DOUBLE_SPACES
                lst and lst.append(sep_snippet)
                other_lst and other_lst.append(sep_snippet)

            col_snippet = column.to_template_snippet()
            lst.append(col_snippet)
            other_lst.append(col_snippet)
            does_prev_col_has_empty_cell = column.has_empty_cell

        self.is_start_with_divider and lst.insert(NUMBER.ZERO, divider_leading_snippet)
        lst.insert(NUMBER.ZERO, pre_leading_data)
        self.is_end_with_divider and lst.append(divider_trailing_snippet)
        lst.append(post_trailing_data)

        headers_snippet = self.get_header_lines_snippet()
        main_snippet = Misc.join_string(*lst)

        headers_snippet and lst_of_snippet.append(headers_snippet)
        main_snippet and lst_of_snippet.append(main_snippet)

        index = NUMBER.ONE
        for col_status in lst_of_column_status[::-NUMBER.ONE][:-NUMBER.ONE]:
            subsidiary_lst = other_lst[:-index]
            if not col_status or not subsidiary_lst:
                break

            last_item = subsidiary_lst[-NUMBER.ONE]
            if not re.match(r'\w+[(][^)]*[)]$', last_item):
                subsidiary_lst.pop()
                index += NUMBER.ONE

            self.is_start_with_divider and subsidiary_lst.insert(NUMBER.ZERO, divider_leading_snippet)
            subsidiary_lst.insert(NUMBER.ZERO, pre_leading_data)
            self.is_end_with_divider and subsidiary_lst.append(divider_trailing_snippet)
            subsidiary_lst.append(post_trailing_data)
            subsidiary_snippet = Misc.join_string(*subsidiary_lst)
            if subsidiary_snippet and subsidiary_snippet not in lst_of_snippet:
                lst_of_snippet.append(subsidiary_snippet)
            index += NUMBER.ONE

        template_snippet = Misc.join_string(*lst_of_snippet, sep=STRING.NEWLINE)

        return template_snippet


class TabularColumn:
    def __init__(self, index=0, name='', left_column=None, right_column=None, is_last=False):
        self.left_column = left_column
        self.right_column = right_column
        self.is_last = is_last
        self.index = index
        self.name = name or 'col%s' % index
        self.cells = []
        self.left_border = NUMBER.ZERO
        self.right_border = NUMBER.ZERO

        self._alignment = 'left'

    def __len__(self):
        chk = bool(self.cells)
        return chk

    def __repr__(self):
        fmt = '%s(name=%r, cells_count=%s)'
        cls_name = Misc.get_instance_class_name(self)
        result = fmt % (cls_name, self.name, len(self.cells))
        return result

    @property
    def cells_count(self):
        total = len(self.cells)
        return total

    @property
    def rows_count(self):
        return self.cells_count

    @property
    def is_left_alignment(self):
        if not self:
            return False
        else:
            chk = self._alignment == 'left'
            return chk

    @property
    def is_right_alignment(self):
        if not self:
            return False
        else:
            chk = self._alignment == 'right'
            return chk

    @property
    def is_center_alignment(self):
        chk = not self.is_left_alignment or not self.is_right_alignment
        return chk

    @property
    def width(self):
        width = min(cell.width for cell in self.cells if cell.width)
        width = width or NUMBER.ONE
        return width

    @property
    def max_width(self):
        lst = []
        for cell in self.cells:
            leading = Misc.get_trailing_line(cell.line, end=cell.right)
            trailing = Misc.get_leading_line(cell.line, start=cell.left)
            leading_len, trailing_len = len(leading), len(trailing)
            if cell.text:
                width = leading_len + cell.width + trailing_len
            else:
                width = max(leading_len, trailing_len)
            lst.append(width)
        width = max(lst) if lst else NUMBER.TWO
        return width

    @property
    def has_empty_cell(self):
        chk = any(cell.is_empty for cell in self.cells)
        return chk

    def append_cell(self, cell):
        self.cells.append(cell)

    def analyze_and_update_alignment(self):
        if not self.cells:
            return

        lst_of_left = [cell.left for cell in self.cells]
        lst_of_right = [cell.right for cell in self.cells]
        are_all_left_same = len(set(lst_of_left)) == NUMBER.ONE
        are_all_right_same = len(set(lst_of_right)) == NUMBER.ONE

        tbl = {'11': 'right', '10': 'left', '01': 'right', '00': 'center'}
        key = Misc.join_string(str(int(are_all_left_same)), str(int(are_all_right_same)))
        self._alignment = tbl.get(key)

    def to_regex(self):
        if not self:
            return STRING.EMPTY

        lst_of_txt = [cell.text for cell in self.cells if cell.text]
        node = TranslatedPattern.do_factory_create(*lst_of_txt)
        pattern = node.get_regex_pattern(var=self.name)
        if node.is_group() and not self.is_last:
            max_items_count = max(cell.items_count for cell in self.cells)
            occurrence = max_items_count - NUMBER.ONE
            if occurrence > NUMBER.ZERO:
                pattern = '%s{,%s})' % (pattern[:-NUMBER.TWO], occurrence)

        if self.has_empty_cell:
            first, last = str.split(pattern, '>', maxsplit=1)
            fmt = '%s>( {%s,%s})|( *%s *))'
            pattern = fmt % (first, self.width, self.max_width, last[:-NUMBER.ONE])
        return pattern

    def to_template_snippet(self):
        if not self:
            return STRING.EMPTY

        lst_of_txt = [cell.text for cell in self.cells if cell.text]
        node = TranslatedPattern.do_factory_create(*lst_of_txt)
        tmpl_snippet = node.get_template_snippet(var=self.name)

        if node.is_group() and not self.is_last:
            max_items_count = max(cell.items_count for cell in self.cells)
            occurrence = max_items_count - NUMBER.ONE
            if occurrence > NUMBER.ZERO:
                tmpl_snippet = tmpl_snippet.replace('words', 'word')
                tmpl_snippet = tmpl_snippet.replace('_group', '')
                fmt = '%s, at_most_%s_group_occurrences)'
                tmpl_snippet = fmt % (tmpl_snippet[:-NUMBER.ONE], occurrence)

        if self.has_empty_cell:
            optional_flag = 'or_either_repeating_%s_%s_spaces' % (self.width, self.max_width)
            tmpl_snippet = '%s, %s)' % (tmpl_snippet[:-1], optional_flag)
        return tmpl_snippet
