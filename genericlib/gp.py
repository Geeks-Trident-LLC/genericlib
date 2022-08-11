import re
from copy import copy
# from difflib import SequenceMatcher

from genericlib import NUMBER
from genericlib import STRING
from genericlib import PATTERN


from regexpro.collection import do_soft_regex_escape


class PatternObject:
    parent_type = None
    child_type = None

    def is_same_type(self, other):
        curr_cls_name = type(self).__name__
        other_cls_name = type(other).__name__
        chk = curr_cls_name == other_cls_name
        return chk

    @classmethod
    def get_pattern_object(cls):
        pass

    @classmethod
    def generalize_patterns(cls, pat1, pat2):
        generalized_pat = pat1.generalize_with(pat2)
        return generalized_pat


class DigitPattern:

    def generalize_with(self, other):
        if isinstance(other, type(self)):
            return copy(self)


class DigitsPattern:
    pass


class LetterPattern:
    pass


class LettersPattern:
    pass


class WordPattern:
    pass


class WordsPattern:
    pass


class FlexWordsPattern:
    pass


class MixedWordPattern:
    pass


class MixedWordsPattern:
    pass


class FlexMixedWordsPattern:
    pass


class PunctuationPattern:
    pass


class PunctuationsPattern:
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
