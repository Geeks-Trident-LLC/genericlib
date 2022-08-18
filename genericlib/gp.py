import re
# from difflib import SequenceMatcher

from genericlib import NUMBER
from genericlib import STRING
from genericlib import PATTERN
from genericlib import TEXT

from genericlib import Misc
from genericlib import MiscObject

from regexpro.collection import do_soft_regex_escape


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

    def get_reference_data(self, other):
        if isinstance(other, TranslatedPattern):
            is_curr_multiple = ' ' in self.data.strip()
            is_other_multiple = ' ' in other.data.strip()
            if self.name in other.name or other.name in self.name:
                return other.data
            else:
                if is_curr_multiple and is_other_multiple:
                    return self.data
                else:
                    result = self.data.split(' ')[NUMBER.ZERO]
                    return result
        else:
            return self.data

    def raise_recommend_exception(self, other):
        cls_name = Misc.get_instance_class_name(self)
        fmt = ('NotImplementPatternRecommendation - Need to implement '
               'this case (%r, %r) for %s')
        err_msg = fmt % (self.data, other.data, cls_name)
        raise Exception(err_msg)

    @classmethod
    def get_translated_pattern_object(cls, data, *other):
        classes = [
            TranslatedDigitPattern,
            TranslatedDigitsPattern,

            TranslatedNumberPattern,

            TranslatedLetterPattern,
            TranslatedLettersPattern,

            TranslatedAlphabetNumericPattern,

            TranslatedSymbolPattern,
            TranslatedSymbolsPattern,
            TranslatedSymbolsGroupPattern,

            TranslatedGraphPattern,

            TranslatedWordPattern,
            TranslatedWordsPattern,

            TranslatedMixedNumberPattern,
            TranslatedMixedWordPattern,

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
        translated_pat_obj1 = cls.get_translated_pattern_object(data1)
        translated_pat_obj2 = cls.get_translated_pattern_object(data2)
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

    def is_superset_of(self, other):    # noqa
        return False

    def recommend(self, other):

        is_new_pat_case1 = other.is_letter()
        is_new_pat_case2 = other.is_letters()
        is_new_pat_case3 = other.is_symbol()
        is_new_pat_case4 = other.is_symbols()
        is_new_pat_case5 = other.is_symbols_group()

        if self.is_subset_of(other):
            new_instance = self.get_new_subset(other)
            return new_instance
        elif self.is_superset_of(other):
            new_instance = self.get_new_superset(other)
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedAlphabetNumericPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case3:
            new_instance = TranslatedGraphPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case4:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case5:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        else:
            self.raise_recommend_exception(other)


class TranslatedDigitsPattern(TranslatedPattern):

    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.DIGITS,
                         defined_pattern=PATTERN.DIGITS)

    def recommend(self, other):

        is_subset_pat = other.is_digits()
        is_subset_pat |= other.is_number()
        is_subset_pat |= other.is_mixed_number()
        is_subset_pat |= other.is_word()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_words()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_digit()

        is_new_pat_case1 = other.is_letter() or other.is_letters()
        is_new_pat_case1 |= other.is_alphabet_numeric()

        is_new_pat_case2 = other.is_symbol() or other.is_symbols() or other.is_graph()
        is_new_pat_case3 = other.is_symbols_group()
        is_new_pat_case4 = other.is_non_whitespace()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case3:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case4:
            new_instance = TranslatedNonWhitespacesPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedNumberPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.NUMBER,
                         defined_pattern=PATTERN.NUMBER)

    def recommend(self, other):

        is_subset_pat = other.is_number()
        is_subset_pat |= other.is_mixed_number()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_digit() or other.is_digits()

        is_new_pat_case1 = other.is_letter() or other.is_letters()
        is_new_pat_case1 |= other.is_alphabet_numeric() or other.is_graph()
        is_new_pat_case1 |= other.is_symbol() or other.is_symbols()
        is_new_pat_case1 |= other.is_word()

        is_new_pat_case2 = other.is_words() or other.is_symbols_group()

        is_new_pat_case3 = other.is_non_whitespace()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case3:
            new_instance = TranslatedNonWhitespacesPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedMixedNumberPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.MIXED_NUMBER,
                         defined_pattern=PATTERN.MIXED_NUMBER)

    def recommend(self, other):

        is_subset_pat = other.is_mixed_number()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_digit() or other.is_digits() or other.is_number()

        is_new_pat_case1 = other.is_letter() or other.is_letters()
        is_new_pat_case1 |= other.is_alphabet_numeric() or other.is_graph()
        is_new_pat_case1 |= other.is_symbol() or other.is_symbols()
        is_new_pat_case1 |= other.is_word()

        is_new_pat_case2 = other.is_words() or other.is_symbols_group()

        is_new_pat_case3 = other.is_non_whitespace()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        if is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case3:
            new_instance = TranslatedNonWhitespacesPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedLetterPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.LETTER,
                         defined_pattern=PATTERN.LETTER)

    def recommend(self, other):

        is_subset_pat = other.is_letter() or other.is_letters()
        is_subset_pat |= other.is_alphabet_numeric() or other.is_graph()
        is_subset_pat |= other.is_word() or other.is_words()
        is_subset_pat |= other.is_mixed_word() or other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespace()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_new_pat_case1 = other.is_digit()
        is_new_pat_case2 = other.is_digits()
        is_new_pat_case3 = other.is_number() or other.is_mixed_number()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedAlphabetNumericPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case3:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedLettersPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.LETTERS,
                         defined_pattern=PATTERN.LETTERS)

    def recommend(self, other):

        is_subset_pat = other.is_letters()
        is_subset_pat |= other.is_word()
        is_subset_pat |= other.is_words()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_letter()

        is_new_pat_case1 = other.is_digit() or other.is_digits()

        is_new_pat_case2 = other.is_number() or other.is_mixed_number()
        is_new_pat_case2 |= other.is_alphabet_numeric()
        is_new_pat_case2 |= other.is_symbol() or other.is_symbols()

        is_new_pat_case3 = other.is_symbols_group()

        is_new_pat_case4 = other.is_non_whitespace()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case3:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case4:
            new_instance = TranslatedNonWhitespacesPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedAlphabetNumericPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.ALPHABET_NUMERIC,
                         defined_pattern=PATTERN.ALPHABET_NUMERIC)

    def recommend(self, other):

        is_subset_pat = other.is_alphabet_numeric()
        is_subset_pat |= other.is_word()
        is_subset_pat |= other.is_words()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespace()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_letter() or other.is_letters() or other.is_digit()

        is_new_pat_case1 = other.is_digits()
        is_new_pat_case2 = other.is_number() or other.is_mixed_number()
        is_new_pat_case2 |= other.is_symbol() or other.is_symbols()
        is_new_pat_case3 = other.is_symbols_group()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case3:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedSymbolPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.SYMBOL,
                         defined_pattern=PATTERN.SYMBOL)

    def recommend(self, other):

        is_subset_pat = other.is_symbol()
        is_subset_pat |= other.is_graph()
        is_subset_pat |= other.is_symbols()
        is_subset_pat |= other.is_symbols_group()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespace()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_new_pat_case1 = other.is_letter() or other.is_digit()
        is_new_pat_case1 |= other.is_alphabet_numeric()

        is_new_pat_case2 = other.is_letters() or other.is_digits()
        is_new_pat_case2 |= other.is_number() or other.is_mixed_number()
        is_new_pat_case2 |= other.is_word()

        is_new_pat_case3 = other.is_words()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedGraphPattern(self.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case3:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedSymbolsPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.SYMBOLS,
                         defined_pattern=PATTERN.SYMBOLS)

    def recommend(self, other):

        is_subset_pat = other.is_symbols()
        is_subset_pat |= other.is_symbols_group()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_symbol()

        is_new_pat_case1 = other.is_letter() or other.is_digit()
        is_new_pat_case1 |= other.is_alphabet_numeric() or other.is_graph()
        is_new_pat_case1 |= other.is_letters() or other.is_digits()
        is_new_pat_case1 |= other.is_number() or other.is_mixed_number()
        is_new_pat_case1 |= other.is_word()

        is_new_pat_case2 = other.is_words()

        is_new_pat_case3 = other.is_non_whitespace()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case3:
            new_instance = TranslatedNonWhitespacesPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedSymbolsGroupPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.SYMBOLS_GROUP,
                         defined_patterns=[PATTERN.SYMBOLS_OR_GROUP,
                                           PATTERN.SYMBOLS_GROUP])

    def recommend(self, other):

        is_subset_pat = other.is_symbols_group()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_symbol() or other.is_symbols()

        is_new_pat_case1 = other.is_letter() or other.is_digit()
        is_new_pat_case1 |= other.is_alphabet_numeric() or other.is_graph()
        is_new_pat_case1 |= other.is_letters() or other.is_digits()
        is_new_pat_case1 |= other.is_number() or other.is_mixed_number()
        is_new_pat_case1 |= other.is_word() or other.is_words()

        is_new_pat_case2 = other.is_non_whitespace() or other.is_non_whitespaces()

        if is_subset_pat:
            new_instance = other(self.data, other.data)
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, other.data)
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedGraphPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.GRAPH,
                         defined_pattern=PATTERN.GRAPH)

    def recommend(self, other):

        is_subset_pat = other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespace()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_letter() or other.is_digit()
        is_superset_pat |= other.is_alphabet_numeric() or other.is_symbol()

        is_new_pat_case1 = other.is_letters() or other.is_digits()
        is_new_pat_case1 |= other.is_number() or other.is_mixed_number()
        is_new_pat_case1 |= other.is_word()

        is_new_pat_case2 = other.is_words()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedWordPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.WORD,
                         defined_pattern=PATTERN.WORD)

    def recommend(self, other):

        is_subset_pat = other.is_word()
        is_subset_pat |= other.is_words()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_letter()
        is_superset_pat |= other.is_letters()
        is_superset_pat |= other.is_digit()
        is_superset_pat |= other.is_digits()
        is_superset_pat |= other.is_alphabet_numeric()

        is_new_pat_case1 = other.is_number() or other.is_mixed_number()

        is_new_pat_case2 = other.is_non_whitespace()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedMixedWordPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedNonWhitespacesPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedWordsPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.WORDS,
                         defined_patterns=[PATTERN.WORD_OR_WORDS, PATTERN.WORDS])

    def recommend(self, other):

        is_subset_pat = other.is_words()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_letter()
        is_superset_pat |= other.is_letters()
        is_superset_pat |= other.is_digit()
        is_superset_pat |= other.is_digits()
        is_superset_pat |= other.is_alphabet_numeric()
        is_superset_pat |= other.is_word()

        is_new_pat_case1 = other.is_number() or other.is_mixed_number()

        is_new_pat_case2 = other.is_non_whitespace() or other.is_non_whitespaces()

        if is_subset_pat:
            new_instance = other(self.data, other.data)
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, other.data)
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedMixedWordPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.MIXED_WORD,
                         defined_pattern=PATTERN.MIXED_WORD)

    def recommend(self, other):

        is_subset_pat = other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()

        is_superset_pat = other.is_letter()
        is_superset_pat |= other.is_letters()
        is_superset_pat |= other.is_digit()
        is_superset_pat |= other.is_digits()
        is_superset_pat |= other.is_alphabet_numeric()
        is_superset_pat |= other.is_word()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_new_pat_case1 = other.is_words()

        is_new_pat_case2 = other.is_non_whitespace()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedMixedWordsPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedNonWhitespacesPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedMixedWordsPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.MIXED_WORDS,
                         defined_patterns=[PATTERN.MIXED_WORD_OR_WORDS,
                                           PATTERN.MIXED_WORDS])

    def recommend(self, other):

        is_subset_pat = other.is_mixed_words()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_letter()
        is_superset_pat |= other.is_letters()
        is_superset_pat |= other.is_digit()
        is_superset_pat |= other.is_digits()
        is_superset_pat |= other.is_alphabet_numeric()
        is_superset_pat |= other.is_word()
        is_superset_pat |= other.is_words()
        is_superset_pat |= other.is_mixed_word()

        is_new_pat = other.is_non_whitespace() or other.is_non_whitespaces()

        if is_subset_pat:
            new_instance = other(self.data, other.data)
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, other.data)
            return new_instance
        elif is_new_pat:
            new_instance = TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedNonWhitespacePattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.NON_WHITESPACE,
                         defined_pattern=PATTERN.NON_WHITESPACE)

    def recommend(self, other):

        is_subset_pat = other.is_non_whitespace()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_superset_pat = other.is_letter()
        is_superset_pat |= other.is_digit()
        is_superset_pat |= other.is_alphabet_numeric()
        is_superset_pat |= other.is_symbol()
        is_superset_pat |= other.is_graph()

        is_new_pat_case1 = other.is_letters()
        is_new_pat_case1 |= other.is_digits()
        is_new_pat_case1 |= other.is_symbols()
        is_new_pat_case1 |= other.is_number()
        is_new_pat_case1 |= other.is_mixed_number()
        is_new_pat_case1 |= other.is_word()
        is_new_pat_case1 |= other.is_mixed_word()

        is_new_pat_case2 = other.is_words()
        is_new_pat_case2 |= other.is_mixed_words()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_superset_pat:
            new_instance = self(self.data, self.get_reference_data(other))
            return new_instance
        elif is_new_pat_case1:
            new_instance = TranslatedNonWhitespacesPattern(self.data, other.data)
            return new_instance
        elif is_new_pat_case2:
            new_instance = TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            return new_instance
        else:
            cls_name = Misc.get_instance_class_name(self)
            fmt = 'Need to implement this case (%r, %r) for %s'
            err_msg = fmt % (self.data, other.data, cls_name)
            raise Exception(err_msg)


class TranslatedNonWhitespacesPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.NON_WHITESPACES,
                         defined_pattern=PATTERN.NON_WHITESPACES)

    def recommend(self, other):
        is_subset_pat = other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespaces_group()

        is_new_pat = other.is_words() or other.is_mixed_words()

        if is_subset_pat:
            new_instance = other(other.data, other.get_reference_data(self))
            return new_instance
        elif is_new_pat:
            new_instance = TranslatedNonWhitespacesGroupPattern(self.data, other.data)
            return new_instance
        else:
            new_instance = self(self.data, other.data)
            return new_instance


class TranslatedNonWhitespacesGroupPattern(TranslatedPattern):
    def __init__(self, data, *other):
        super().__init__(data, *other, name=TEXT.NON_WHITESPACES_GROUP,
                         defined_patterns=[PATTERN.NON_WHITESPACES_OR_GROUP,
                                           PATTERN.NON_WHITESPACES_GROUP])

    def recommend(self, other):
        new_instance = self(self.data, other.data)
        return new_instance


class CommonText:
    def __init__(self, value, is_generic=False, is_flex_space=False):
        self._value = value
        self.is_generic = is_generic
        self.is_flex_space = is_flex_space

        self.pattern = self.process()

    def get_partial_pattern(self, data):
        if self.is_generic:
            pattern = 'TODO: need to implement this pattern'
        else:
            pattern = do_soft_regex_escape(data)

        return pattern

    def process(self):

        value = self._value

        if not value:
            return STRING.EMPTY
        elif re.match(' +$', value):
            return self.is_flex_space and PATTERN.SPACES or value

        if STRING.SPACE_CHAR not in value:
            pattern = do_soft_regex_escape(value)
            return pattern

        match1 = re.match(PATTERN.SPACES, value)
        match2 = re.search(' +$', value)
        prefix = match1 and match1.group() or STRING.EMPTY
        prefix = prefix and self.is_flex_space and PATTERN.SPACES or prefix
        postfix = match2 and match2.group() or STRING.EMPTY
        postfix = postfix and self.is_flex_space and PATTERN.SPACES or postfix

        value = value.strip()

        start = NUMBER.ZERO
        lst = [prefix]

        for item in re.finditer(PATTERN.SPACES, value):
            pre_matched = value[start: item.start()]
            matched_txt = item.group()
            pre_matched_pat = self.get_partial_pattern(pre_matched)
            lst.append(pre_matched_pat)
            lst.append(PATTERN.SPACES if self.is_flex_space else matched_txt)
            start = item.end()

        if lst:
            post_matched = value[start:]
            post_matched_pat = self.get_partial_pattern(post_matched)
            lst.append(post_matched_pat)
        else:
            pat = self.get_partial_pattern(value)
            lst.append(pat)

        lst.append(postfix)

        pattern = str.join(STRING.EMPTY, lst)

        return pattern


class DiffText:
    def __init__(self, value1, value2, *args):
        self._values = [value1, value2] + list(args)


class LineWordDiff:
    pass
