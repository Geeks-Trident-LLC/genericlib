import re
from copy import deepcopy
# from difflib import SequenceMatcher

from genericlib import NUMBER
from genericlib import STRING
from genericlib import PATTERN
from genericlib import TEXT

from genericlib import Misc


from regexpro.collection import do_soft_regex_escape


class TranslatedPattern:

    def __init__(self, data):
        self.data = str(data)
        self._pattern = STRING.EMPTY
        self.name = STRING.EMPTY
        self.process()

    def __len__(self):
        chk = self._pattern == STRING.EMPTY
        return chk

    @property
    def translated(self):
        chk = self._pattern != STRING.EMPTY
        return chk

    @property
    def pattern(self):
        return self._pattern

    def process(self):
        self._pattern = ''

    def is_same_type(self, other):
        curr_cls_name = Misc.get_instance_class_name(self)
        other_cls_name = Misc.get_instance_class_name(other)
        chk = curr_cls_name == other_cls_name
        return chk

    def is_same_group(self, other):
        chk = self.name != STRING.EMPTY
        chk &= other.name in self.name
        chk |= self.name in other.name
        return chk

    def is_multiple_of(self, other):
        if not self.is_same_group(other):
            return False
        chk = other.name != self.name
        chk &= other.name in self.name
        return chk

    def is_singular_of(self, other):
        if not self.is_same_group(other):
            return False

        chk = self.name != other.name
        chk &= other.name in self.name
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

    def is_word(self):
        return self.name == TEXT.WORD

    def is_words(self):
        return self.name == TEXT.WORDS

    def is_flex_words(self):
        return self.name == TEXT.FLEX_WORDS

    def is_mixed_word(self):
        return self.name == TEXT.MIXED_WORD

    def is_mixed_words(self):
        return self.name == TEXT.MIXED_WORDS

    def is_mixed_flex_words(self):
        return self.name == TEXT.MIXED_FLEX_WORDS

    def is_non_whitespace(self):
        return self.name == TEXT.NON_WHITESPACE

    def is_non_whitespaces(self):
        return self.name == TEXT.NON_WHITESPACES

    def is_non_whitespace_group(self):
        return self.name == TEXT.NON_WHITESPACE_GROUP

    def is_flex_non_whitespace_group(self):
        return self.name == TEXT.FLEX_NON_WHITESPACE_GROUP

    @classmethod
    def get_translated_pattern_object(cls, data):
        classes = [
            TranslatedDigitPattern,
            TranslatedDigitsPattern,

            TranslatedNumberPattern,

            TranslatedLetterPattern,
            TranslatedLettersPattern,

            TranslatedAlphabetNumericPattern,

            TranslatedWordPattern,
            TranslatedWordsPattern,

            TranslatedMixedNumberPattern,
            TranslatedMixedWordPattern,

            TranslatedMixedWordsPattern,
            TranslatedMixedFlexWordsPattern,

            TranslatedNonWhiteSpace,
            TranslatedNonWhiteSpaces,
            TranslatedNonWhiteSpaceGroup,
            TranslatedFlexNonWhiteSpaceGroup
        ]
        for class_ in classes:
            node = class_(data)
            if node.translated:
                return node
        raise Exception('TODO: add exception here')

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

    def __init__(self, data):
        super().__init__(data)
        self.name = TEXT.DIGIT

    def process(self):
        match = re.match('[0-9]$', self.data)   # noqa
        if match:
            self._pattern = '[0-9]'

    def recommend(self, other):

        is_subset_pat = other.is_digit()
        is_subset_pat |= other.is_digits()
        is_subset_pat |= other.is_number()
        is_subset_pat |= other.is_mixed_number()
        is_subset_pat |= other.is_alphabet_numeric()
        is_subset_pat |= other.is_word()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_words()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_mixed_flex_words()
        is_subset_pat |= other.is_non_whitespace()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespace_group()
        is_subset_pat |= other.is_flex_non_whitespace_group()

        if is_subset_pat:
            new_instance = deepcopy(other)
            return new_instance
        elif other.is_letter():
            new_instance = TranslatedAlphabetNumericPattern(other.data)
            return new_instance
        elif other.is_letters():
            new_instance = TranslatedWordPattern(other.data)
            return new_instance
        else:
            raise Exception('TODO: add exception here')


class TranslatedDigitsPattern(TranslatedPattern):

    def __init__(self, data):
        super().__init__(data)
        self.name = TEXT.DIGITS

    def process(self):
        match = re.match('[0-9]+$', self.data)   # noqa
        if match:
            self._pattern = '[0-9]+'

    def recommend(self, other):

        is_subset_pat = other.is_digits()
        is_subset_pat |= other.is_number()
        is_subset_pat |= other.is_mixed_number()
        is_subset_pat |= other.is_word()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_words()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_mixed_flex_words()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespace_group()
        is_subset_pat |= other.is_flex_non_whitespace_group()

        if other.is_digit():
            new_instance = deepcopy(self)
            return new_instance
        elif is_subset_pat:
            new_instance = deepcopy(other)
            return new_instance
        elif other.is_letter() or other.is_letters() or other.is_alphabet_numeric():
            new_instance = TranslatedWordPattern(other.data)
            return new_instance

        elif other.is_non_whitespace():
            new_instance = TranslatedNonWhiteSpaces(other.data)
            return new_instance
        else:
            raise Exception('TODO: add exception here')


class TranslatedNumberPattern(TranslatedPattern):
    def __init__(self, data):
        super().__init__(data)
        self.name = TEXT.NUMBER

    def process(self):
        pat = '[0-9]*[.]?[0-9]+'
        match = re.match('%s$' % pat, self.data)
        if match:
            self._pattern = pat

    def recommend(self, other):

        is_subset_pat = other.is_number()
        is_subset_pat |= other.is_mixed_number()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_mixed_flex_words()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespace_group()
        is_subset_pat |= other.is_flex_non_whitespace_group()

        is_singular_unrelated_pat = other.is_letter()
        is_singular_unrelated_pat |= other.is_letters()
        is_singular_unrelated_pat |= other.is_alphabet_numeric()
        is_singular_unrelated_pat |= other.is_word()

        if other.is_digit() or other.is_digits():
            new_instance = deepcopy(self)
            return new_instance
        elif is_subset_pat:
            new_instance = deepcopy(other)
            return new_instance
        elif is_singular_unrelated_pat:
            new_instance = TranslatedMixedWordPattern(other.data)
            return new_instance
        elif other.is_words():
            new_instance = TranslatedMixedWordsPattern(other.data)
            return new_instance
        elif other.is_non_whitespace():
            new_instance = TranslatedNonWhiteSpaces(other.data)
            return new_instance
        else:
            raise Exception('TODO: add exception here')


class TranslatedMixedNumberPattern(TranslatedPattern):
    def __init__(self, data):
        super().__init__(data)
        self.name = TEXT.MIXED_NUMBER

    def process(self):
        pat = r'[\(+-]?[0-9]*[.]?[0-9]+[)]?'
        match = re.match('%s$' % pat, self.data)
        if match:
            self._pattern = pat

    def recommend(self, other):

        is_subset_pat = other.is_mixed_number()
        is_subset_pat |= other.is_mixed_word()
        is_subset_pat |= other.is_mixed_words()
        is_subset_pat |= other.is_mixed_flex_words()
        is_subset_pat |= other.is_non_whitespaces()
        is_subset_pat |= other.is_non_whitespace_group()
        is_subset_pat |= other.is_flex_non_whitespace_group()

        is_singular_unrelated_pat = other.is_letter()
        is_singular_unrelated_pat |= other.is_letters()
        is_singular_unrelated_pat |= other.is_alphabet_numeric()
        is_singular_unrelated_pat |= other.is_word()

        if other.is_digit() or other.is_digits() or other.is_number():
            new_instance = deepcopy(self)
            return new_instance
        elif is_subset_pat:
            new_instance = deepcopy(other)
            return new_instance
        elif is_singular_unrelated_pat:
            new_instance = TranslatedMixedWordPattern(other.data)
            return new_instance
        elif other.is_words():
            new_instance = TranslatedMixedWordsPattern(other.data)
            return new_instance
        elif other.is_non_whitespace():
            new_instance = TranslatedNonWhiteSpaces(other.data)
            return new_instance
        else:
            raise Exception('TODO: add exception here')


class TranslatedLetterPattern(TranslatedPattern):
    pass


class TranslatedLettersPattern(TranslatedPattern):
    pass


class TranslatedAlphabetNumericPattern(TranslatedPattern):
    pass


class TranslatedWordPattern(TranslatedPattern):
    pass


class TranslatedWordsPattern(TranslatedPattern):
    pass


class TranslatedFlexWordsPattern(TranslatedPattern):
    pass


class TranslatedMixedWordPattern(TranslatedPattern):
    pass


class TranslatedMixedWordsPattern(TranslatedPattern):
    pass


class TranslatedMixedFlexWordsPattern(TranslatedPattern):
    pass


class TranslatedNonWhiteSpace(TranslatedPattern):
    pass


class TranslatedNonWhiteSpaces(TranslatedPattern):
    pass


class TranslatedNonWhiteSpaceGroup(TranslatedPattern):
    pass


class TranslatedFlexNonWhiteSpaceGroup(TranslatedPattern):
    pass


class CommonPhrase:
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


class DiffPhrase:
    def __init__(self, value1, value2, *args):
        self._values = [value1, value2] + list(args)


class LineWordDiff:
    pass
