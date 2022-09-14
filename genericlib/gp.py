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
           expected_rows_count=None, expected_result=None):
    builder = TemplateBuilder(user_data=template_snippet, test_data=test_data)
    is_verified = builder.verify(expected_rows_count=expected_rows_count,
                                 expected_result=expected_result)
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
        match = re.match(PATTERN.SPACES, self.raw_data)
        return match.group() if match else STRING.EMPTY

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
                if self.is_plural():
                    self._pattern = self.defined_patterns[-NUMBER.ONE]
                else:
                    self._pattern = self.defined_patterns[NUMBER.ZERO]
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
        super().__init__(data, *other, name=TEXT.SYMBOLS_GROUP,
                         defined_patterns=[PATTERN.SYMBOLS_OR_GROUP,
                                           PATTERN.SYMBOLS_GROUP])

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
        super().__init__(data, *other, name=TEXT.WORDS,
                         defined_patterns=[PATTERN.WORD_OR_WORDS, PATTERN.WORDS])

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
        super().__init__(data, *other, name=TEXT.MIXED_WORDS,
                         defined_patterns=[PATTERN.MIXED_WORD_OR_WORDS,
                                           PATTERN.MIXED_WORDS])

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
        super().__init__(data, *other, name=TEXT.NON_WHITESPACES_GROUP,
                         defined_patterns=[PATTERN.NON_WHITESPACES_OR_GROUP,
                                           PATTERN.NON_WHITESPACES_GROUP])

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
        chk = any(line.startswith(STRING.SPACE_CHAR) for line in self.raw_lines)
        return chk

    @property
    def is_trailing(self):
        chk = any(line.endswith(STRING.SPACE_CHAR) for line in self.raw_lines)
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
    def __init__(self, *lines, col_widths_as_ref='', separator_as_ref='',
                 symbols_group_as_ref=False, lines_as_col_names='',
                 skipped_symbol_line=True):
        self.lines = Misc.get_list_of_lines(*lines)
        self.kwargs = DotObject(
            col_widths_as_ref=col_widths_as_ref,
            separator_as_ref=str(separator_as_ref),
            symbols_group_as_ref=str(symbols_group_as_ref),
            lines_as_col_names=lines_as_col_names,
            skipped_symbol_line=skipped_symbol_line
        )
        self.columns_widths = []
        self.columns_widths_snippet = STRING.EMPTY
        self.sep_snippet = STRING.EMPTY
        self.symbols_group_snippet = STRING.EMPTY
        self._is_leading = None
        self._is_trailing = None
        self.process()

    def __len__(self):
        chk = bool(self.columns_widths_snippet or
                   self.sep_snippet or
                   self.symbols_group_snippet)
        return chk

    @property
    def longest_line_length(self):
        max_len = max(len(line) for line in self.lines)
        return max_len

    @property
    def is_leading(self):
        if self._is_leading is None:
            for line in self.lines:
                if line.strip() and line.startswith(STRING.SPACE_CHAR):
                    self._is_leading = True
                    return self._is_leading
        return self._is_leading

    @property
    def is_trailing(self):
        if self._is_trailing is None:
            for line in self.lines:
                if line.strip() and line.startswith(STRING.SPACE_CHAR):
                    self._is_trailing = True
                    return self._is_trailing
        return self._is_trailing

    def prepare_columns_width(self):
        error_msg = 'col_widths_as_ref MUST BE string/list datatype of group of digit(s)'
        data = self.kwargs.col_widths_as_ref
        if not data:
            return

        if Misc.is_string(data) or Misc.is_list(data):
            if Misc.is_string(data):
                pat = '(?: *, *)|(?: +)'
                lst = [item or '0' for item in re.split(pat, str.strip(data))]
            else:
                lst = [str(item) for item in data]

            chk = all(str(item).isdigit() for item in lst)
            if chk:
                self.columns_widths = [int(item) for item in lst[:-1]]
                self.columns_widths.append(0)
            else:
                self.raise_runtime_error(msg=error_msg)
        else:
            self.raise_runtime_error(msg=error_msg)

    def generate_columns_width_snippet(self):
        self.prepare_columns_width()
        if not self.columns_widths:
            return False

        result = []

        for item in self.columns_widths:
            pass

        return True

    def generate_separator_snippet(self):
        is_empty = self.kwargs.separator_as_ref == STRING.EMPTY
        if is_empty:
            return False

        return True

    def generate_symbols_group_snippet(self):
        is_empty = self.kwargs.symbols_group_as_ref == STRING.EMPTY
        if is_empty:
            return False

        return True

    def process(self):
        is_generated = self.generate_columns_width_snippet()
        is_generated = is_generated and self.generate_symbols_group_snippet()
        is_generated and self.generate_separator_snippet()

    def raise_exception_if_not_ready(self):
        if not self:
            self.raise_runtime_error(msg='text is not tabular data')

    def to_regex(self):
        self.raise_exception_if_not_ready()
        
        return ''

    def to_template_snippet(self):
        self.raise_exception_if_not_ready()
        
        return ''


class TabularTextPatternByFixedColumns(RuntimeException):
    def __init__(self, *lines, col_widths=None, headers=None, headers_data=None):
        self.lines = Misc.get_list_of_lines(*lines)
        self.col_widths = col_widths
        self.columns_count = len(col_widths) if Misc.is_list(col_widths) else NUMBER.ZERO
        self.raise_exception_if_columns_widths_not_provided()
        self.headers_data = headers_data
        self.raw_headers_data = []
        self.headers = headers
        self.variables = []
        self.parse_headers()

    def __len__(self):
        return bool(self.columns_count)

    def get_default_variables(self):  # noqa
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

    def parse_headers_to_variables(self, headers):
        variables = []
        if not headers:
            return variables

        if Misc.is_string(headers):
            headers = re.split(' *, *', headers)

        if Misc.is_list(headers) and len(headers) == self.columns_count:
            pat = '[ %s' % PATTERN.SYMBOLS[1:]
            repl = STRING.UNDERSCORE_CHAR
            for i, hdr in enumerate(headers):
                new_hdr = re.sub(pat, repl, hdr.strip())
                new_hdr = new_hdr if new_hdr == repl else new_hdr.rstrip(repl)
                if new_hdr in variables:
                    variables.append('%s%s' % (new_hdr, i))
                else:
                    variables.append(new_hdr)
        else:
            variables = self.get_default_variables()

        return variables

    def parse_headers(self):
        if self.headers or self.headers_data:
            if self.headers:
                self.variables = self.parse_headers_to_variables(self.headers)
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
    def __init__(self, *lines, divider=' ', columns_count=0,
                 headers=None, headers_data=None):
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
        self.raw_headers_data = []
        self.headers = headers
        self.variables = []
        # self.parse_headers()

    def __len__(self):
        return bool(self.columns_count)

    @property
    def is_leading(self):
        if not self.total_lines:
            return False
        if self._is_leading is None:
            for line in self.lines:
                if line.strip() and line.startswith(STRING.SPACE_CHAR):
                    self._is_leading = True
                    return self._is_leading
            else:
                self._is_leading = False
        return self._is_leading

    @property
    def is_trailing(self):
        if not self.total_lines:
            return False
        if self._is_trailing is None:
            for line in self.lines:
                if line.strip() and line.startswith(STRING.SPACE_CHAR):
                    self._is_trailing = True
                    return self._is_trailing
            else:
                self._is_trailing = False
        return self._is_trailing

    @property
    def is_start_with_divider(self):
        if self._is_start_with_divider is None:
            count = 0
            for line in self.lines:
                if line.startswith(self.divider):
                    count += 1

            lines_count = len(self.lines)
            if count:
                # chk = count > lines_count / NUMBER.TWO
                chk = op.gt(count, op.truediv(lines_count, NUMBER.TWO))
                self._is_start_with_divider = chk
            else:
                self._is_start_with_divider = False
        return self._is_start_with_divider

    @property
    def is_end_with_divider(self):
        if self._is_end_with_divider is None:
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
        return self._is_end_with_divider

    def raise_exception_if_columns_count_not_provided(self):
        if not self:
            self.raise_runtime_error(msg='columns_count CANT be zero')

    def get_default_variables(self):  # noqa
        var_names = ['col%s' % i for i in range(self.columns_count)]
        return var_names

    def try_to_get_cells_info_by_space_symbols_divider(self):
        fmt = ' *%(p)s( +%(p)s){%(rep)s} *$'
        repetition = self.columns_count - NUMBER.ONE
        pat = fmt % dict(p=PATTERN.SYMBOLS, rep=repetition)
        found_line = STRING.EMPTY

        for line in self.lines:
            match = re.match(pat, line)
            if match:
                found_line = line
                break

        if not found_line:
            return False, None

        pat = ' * %s*' % PATTERN.SYMBOLS
        lst = re.findall(pat, found_line)

        lst_of_pos_info = []
        prev_right = 0
        for item in lst:
            curr_width = len(item)
            left = prev_right
            right = left + curr_width - NUMBER.ONE
            prev_right = right
            pair = TabularCell(found_line, left, right)
            lst_of_pos_info.append(pair)
        else:
            if lst_of_pos_info:
                pair.right = pair.right + NUMBER.ONE

        lst_of_cells_data = []

        for line in self.lines:
            cells_data = []
            prev_sub_txt = STRING.EMPTY
            for pos_info in lst_of_pos_info:
                sub_txt = line[pos_info.left:pos_info.right]
                if cells_data and prev_sub_txt.strip():
                    if prev_sub_txt[-NUMBER.ONE:] == STRING.SPACE_CHAR:
                        cells_data.append(sub_txt)
                    else:
                        space, spaces = STRING.SPACE_CHAR, STRING.DOUBLE_SPACES
                        if space in prev_sub_txt:
                            split_chars = spaces if spaces in prev_sub_txt else space
                            _, last = prev_sub_txt.rsplit(split_chars, maxsplit=1)
                            prev_data = prev_sub_txt[:-len(last) - NUMBER.ONE]
                            new_sub_txt = ' %s%s' % (last, sub_txt)
                            cells_data.pop()
                            cells_data.append(prev_data)
                            cells_data.append(new_sub_txt)
                        else:
                            cells_data.append(sub_txt)
                else:
                    cells_data.append(sub_txt)
                prev_sub_txt = sub_txt
            lst_of_cells_data.append(cells_data)

        return True, []

    def try_to_get_cells_info_by_space_mixed_words_divider(self):
        fmt = ' *%(p)s( +%(p)s){%(rep)s} *$'
        repetition = self.columns_count - NUMBER.ONE
        pat = fmt % dict(p=PATTERN.MIXED_WORD_OR_WORDS, rep=repetition)

        found_lines = []
        for line in self.lines:
            match = re.match(pat, line)
            if match:
                found_lines.append(line)

        if not found_lines:
            return False, None

        return True, []

    def get_cells_info_by_space_divider(self):
        parsed, cells_info = self.try_to_get_cells_info_by_space_symbols_divider()
        if not parsed:
            parsed, cells_info = self.try_to_get_cells_info_by_space_mixed_words_divider()
            if not parsed:
                raise Exception('')
        return cells_info

    def get_cells_info_by_symbol_divider(self):
        divider_pat = re.escape(self.divider.strip())
        repetition = self.columns_count - NUMBER.ONE
        fmt = r' *(%(d)s)? *%(p)s( *%(d)s *%(p)s){%(rep)s} *(%(d)s)? *$'
        pat = fmt % dict(d=divider_pat, p=PATTERN.EVERYTHING, rep=repetition)

        found_line = ''
        for line in self.lines:
            match = re.match(pat, line)
            if match:
                found_line = line
                break
        if not found_line:
            return False, []

        return True, []

    def get_cells_info(self):
        divider = self.divider.strip()
        if divider == STRING.EMPTY:
            cells_info = self.get_cells_info_by_space_divider()
            return cells_info

        elif re.match(PATTERN.SYMBOLS, divider):
            cells_info = self.get_cells_info_by_symbol_divider()
            return cells_info
        else:
            self.raise_runtime_error(msg='Unsupported divider %r' % self.divider)


class TabularCell(RuntimeException):
    def __init__(self, line, left_pos, right_pos, ref_cell=None):
        self.args = (line, left_pos, right_pos, ref_cell)

        self._leading = None
        self._trailing = None

        self.left = NUMBER.ZERO
        self.right = NUMBER.ZERO
        self.left_bound = NUMBER.ZERO
        self.right_bound = NUMBER.ZERO

        self.line = STRING.EMPTY
        self.data = STRING.EMPTY
        self.text = STRING.EMPTY

        self.ref_cell = None

        self.process()

    def __len__(self):
        chk = self.left >= NUMBER.ZERO
        chk = chk and self.right > self.left
        return chk

    @property
    def leading(self):
        if self._leading is None:
            if self.is_empty:
                self._leading = STRING.EMPTY
            else:
                lst = re.findall(PATTERN.SPACESATSOS, self.data)
                self._leading = lst[NUMBER.ZERO] if lst else STRING.EMPTY
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
        chk = self.text = STRING.EMPTY
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
            if other_right > self.ref_cell.right_bound:
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

    def readjust(self, prev_cell=None):
        if not isinstance(prev_cell, self.__class__):
            # dont readjust
            return

        chk1 = prev_cell.is_multi_trailing
        chk2 = prev_cell.is_empty
        chk3 = prev_cell.is_single_trailing and self.is_leading

        if chk1 or chk2 and chk3:
            # dont readjust
            return
        else:
            prefix = prev_cell.get_postfix_data()
            if prefix:
                width = len(prefix) + NUMBER.ONE
                self.update_position('left', val=self.left-width)
                prev_cell.update_position('right', val=self.right-width)
            else:
                # dont readjust
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
        self.right = right
        self.line = line
        self.data = self.line[self.left:self.right]
        self.text = self.data.strip()

        self.left_bound = self.left + len(self.leading)
        self.right_bound = self.right - len(self.trailing)


class TabularRow(RuntimeException):
    def __init__(self, line, ref_row=None):
        self.line = line
        self.ref_row = ref_row
        self.cells = []

    def __len__(self):
        chk = bool(self.cells)
        return chk

    def append_new_cell(self, left_pos, right_pos):
        index = len(self.cells)
        ref_cell = self.ref_row[index] if self.ref_row else None
        tabular_cell = TabularCell(self.line, left_pos, right_pos, ref_cell=ref_cell)
        self.cells.append(tabular_cell)

    @classmethod
    def create_ref_row(cls, line, pattern):
        lst = re.findall(pattern, line)
        if not lst:
            RuntimeException.do_raise_runtime_error(
                obj=Misc.join_string(cls.__name__, 'RTError'),
                msg='Failed to parse\nPattern: %r\nLine: %r' % (pattern, line)
            )

        ref_tabular_row = cls(line)

        prev_right = NUMBER.ZERO
        for count, item in enumerate(lst, NUMBER.ONE):
            left, right = prev_right, prev_right + len(item)
            prev_right = right
            ref_tabular_row.append_new_cell(left, right)

        return ref_tabular_row


class TabularRows(RuntimeException):
    def __init__(self, *lines, ref_row=None):
        self.lines = Misc.get_list_of_lines(*lines)
        self.ref_row = ref_row

        self.rows = []

    def process(self):
        for line in self.lines:
            row = TabularRow(line, ref_row=self.ref_row)
            self.rows.append(row)


class TabularColumn:
    def __init__(self, index=0, name='', left_column=None, right_column=None):
        self.left_column = left_column
        self.right_column = right_column
        self.index = index
        self.name = name
        self.tabular_cells = []
        self.left_pos = 0
        self.right_pos = 1

    def update_left_pos(self, pos):
        self.left_pos = pos

    def update_right_pos(self, pos):
        self.right_pos = pos

    def update_cells_data(self, *lst_of_data):
        for index, data in lst_of_data:
            cell = self.tabular_cells[index]
            cell.update_data(data)

    def update_cell_data(self, data, pos):
        cell = self.tabular_cells[pos]
        cell.update_data(data)
