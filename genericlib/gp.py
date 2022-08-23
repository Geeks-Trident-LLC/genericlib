import re

from itertools import combinations

from difflib import ndiff

from genericlib import NUMBER
from genericlib import STRING
from genericlib import PATTERN
from genericlib import TEXT

from genericlib import Misc

from regexpro import TextPattern


class TranslatedPattern:

    def __init__(self, data, *other, name='',
                 defined_pattern='', defined_patterns=None):
        self.data = str(data)
        self.other_data = other[NUMBER.ZERO] if other else STRING.EMPTY
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
            for pat in self.defined_patterns[::-NUMBER.ONE]:
                matched_pat = self.check_matching(pat)
                if matched_pat:
                    self._pattern = matched_pat
                    break
        else:
            matched_pat = self.check_matching(self.defined_pattern)
            self._pattern = matched_pat

    def check_matching(self, pattern):
        pat = '%s$' % pattern
        match = re.match(pat, self.data)
        if self.other_data:
            other_match = re.match(pat, self.other_data)
            matched_pat = pattern if match and other_match else STRING.EMPTY
        else:
            matched_pat = pattern if match else STRING.EMPTY

        return matched_pat

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
        chk = STRING.SPACE_CHAR in self.data.strip()
        return chk

    def get_reference_data(self, other):
        if isinstance(other, TranslatedPattern):
            if self.is_subset_of(other) or self.is_superset_of(other):
                return other.data
            else:
                if self.is_plural() and other.is_plural():
                    return self.data
                else:
                    result = self.data.split(STRING.SPACE_CHAR)[NUMBER.ZERO]
                    return result
        else:
            return self.data

    def raise_recommend_exception(self, other):
        cls_name = Misc.get_instance_class_name(self)
        fmt = ('NotImplementRecommendedPattern - Need to implement '
               'this case (%r, %r) for %s')
        err_msg = fmt % (self.data, other.data, cls_name)
        raise Exception(err_msg)

    def get_readable_snippet(self, var=''):
        if not self.name:
            error = 'TranslatedPatternSnippetError - CANT create snippet without name'
            raise Exception(error)

        value = self.data
        value = value.replace('(', '_SYMBOL_LEFT_PARENTHESIS_')
        value = value.replace(')', '_SYMBOL_RIGHT_PARENTHESIS_')

        if var:
            snippet = '%s(var=%s, value=%s)' % (self.name, var, value)
        else:
            snippet = '%s(value=%s)' % (self.name, value)
        return snippet

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

        fmt = 'FactoryTranslatedPatternIssue - Need to implement this case (%r, %r)'
        err_msg = fmt % (data, other)
        raise Exception(err_msg)

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

        if txt.startswith('  '):
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
        if txt.startswith('  '):
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
        txt1 = '  '.join(self.lst)
        txt2 = '  '.join(self.lst_other)
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
        txt = '  '.join(self.lst)
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

        self._pattern = ''
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
                self._pattern = '%s%s' % (PATTERN.SPACES_BUT, self._pattern)
            if self.is_trailing:
                self._pattern = '%s%s' % (self._pattern, PATTERN.SPACES_BUT)
        else:
            lst_a = re.split(PATTERN.SPACES, self._line_a)
            lst_b = re.split(PATTERN.SPACES, self._line_b)
            if lst_a == lst_b:
                self._pattern = TextPattern('  '.join(lst_a))
                if self.is_leading:
                    self._pattern = '%s%s' % (PATTERN.SPACES_BUT, self._pattern)
                if self.is_trailing:
                    self._pattern = '%s%s' % (self._pattern, PATTERN.SPACES_BUT)
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
            pattern = STRING.EMPTY.join(result)
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


class DiffLinePattern:
    def __init__(self, line1, line2, *other_lines):
        self.raw_lines = []
        self.lines = []
        self._pattern = ''
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
                pattern = fmt % (PATTERN.SPACES_BUT, pattern)

        if self.is_trailing:
            if self.are_all_trailing:
                pattern = fmt % (pattern, PATTERN.SPACES)
            else:
                pattern = fmt % (pattern, PATTERN.SPACES_BUT)

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
        self._pattern = ''

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
            fmt = ('DiffLinePatternError - CANT form pattern because provided '
                   'lines are less than two\n%s')
            lst = ['Line 1: %r' % line1, 'Line 2: %r' % line2]
            if other_lines:
                lst.append('Other Lines: %r' % other_lines)
            error = fmt % '\n'.join(lst)
            raise Exception(error)
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
            pattern = fmt % (PATTERN.SPACES_BUT, pattern)

        if is_both_trailing:
            pattern = fmt % (pattern, PATTERN.SPACES)
        elif is_trailing:
            pattern = fmt % (pattern, PATTERN.SPACES_BUT)

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

        fmt = 'DiffLinePatternError - built pattern(s) did not match text\n  %s'
        error = fmt % '\n  '.join(repr(item) for item in lst)
        raise Exception(error)


class IterativeLinePattern:
    def __init__(self, line):
        self.raw_line = line
        self.line = line.strip()
        self._pattern = ''

    def __len__(self):
        chk = bool(len(self._pattern))
        return int(chk)

    @property
    def pattern(self):
        pattern = self._pattern

        fmt = '%s%s'
        if self.is_leading:
            pattern = fmt % (PATTERN.SPACES_BUT, pattern)

        if self.is_trailing:
            pattern = fmt % (pattern, PATTERN.SPACES_BUT)

        return pattern

    @property
    def is_leading(self):
        chk = self.raw_line.startswith(STRING.SPACE_CHAR)
        return chk

    @property
    def is_trailing(self):
        chk = self.raw_line.endswith(STRING.SPACE_CHAR)
        return chk

    def get_editable_snippet(self, label=''):
        pat = r'[\x20-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+'
        label = re.sub(pat, '_', str(label))
        spaces = re.findall(PATTERN.SPACES, self.line)
        lst = []
        for index, item in enumerate(re.split(PATTERN.SPACES, self.line)):
            node = TranslatedPattern.do_factory_create(item)
            var_ = 'v%s%s' % (label, index)

            item_snippet = node.get_readable_snippet(var=var_)
            lst.append(item_snippet)
            if index < len(spaces):
                lst.append(spaces[index])

        snippet = STRING.EMPTY.join(lst)
        editing_snippet = 'capture() regex(): %s' % snippet
        return editing_snippet
