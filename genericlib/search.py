import re

from .utils import Misc
from .constant import STRING
from .constnum import NUMBER
from .constsymbol import SYMBOL
from .constpattern import PATTERN


class Wildcard:
    def __init__(self, data, is_prefix=True, is_postfix=True, ignore_case=True):
        self.data = str(data)
        self.is_prefix = is_prefix
        self.is_postfix = is_postfix
        self.ignore_case = ignore_case
        self.is_multiline = bool(re.search(PATTERN.CRNL, self.data))

        self._pattern = STRING.EMPTY
        self.failure_fmt = 'unsupported parsing integers (%s, %s)'
        self.process()

    @property
    def pattern(self):
        return self._pattern

    def process(self):
        p = r'(?i)(?P<start>^ *--regex *)|(?P<end> +--regex *$)|(?P<middle> *--regex +)'
        match = re.search(p, self.data)
        if match:
            start = match.groupdict().get(STRING.START, STRING.EMPTY)
            end = match.groupdict().get(STRING.END, STRING.EMPTY)
            middle = match.groupdict().get(STRING.MIDDLE, STRING.EMPTY)
            if start:
                replaced = PATTERN.SPACES_BUT if len(start) > NUMBER.EIGHT else STRING.EMPTY
            elif end:
                replaced = PATTERN.SPACES_BUT if len(end) > NUMBER.EIGHT else STRING.EMPTY
            else:
                replaced = PATTERN.SPACES_BUT if len(middle) > NUMBER.EIGHT else STRING.EMPTY
            self._pattern = re.sub(p, replaced, self.data)
        else:
            method = self.parse_multiline if self.is_multiline else self.parse_single_line
            pat = method(self.data)
            pattern = '^%s$' % pat
            if self.ignore_case:
                pattern = '(?i)%s' % pattern
            self._pattern = pattern

    def get_pattern_for_two_unsigned_int(self, v1, v2):     # noqa
        small, large = min(v1, v2), max(v1, v2)
        first_small = int(Misc.get_first_char(small))
        last_small = int(Misc.get_last_char(small))
        first_large = int(Misc.get_first_char(large))
        last_large = int(Misc.get_last_char(large))
        small_width, large_width = len(str(small)), len(str(large))

        repl_pat = r'(\[(\d)-\2\])'
        repl_val = r'\2'

        if v1 == v2:
            return str(v1)
        elif small_width == NUMBER.ONE and large_width == NUMBER.ONE:
            pattern = '[%s-%s]' % (small, large)
            return pattern
        elif small_width == NUMBER.ONE and large_width == NUMBER.TWO:
            if first_large == NUMBER.ONE:
                args = (small, last_large)
                pattern = '[%s-9]|(1[0-%s])' % args
                pattern = re.sub(repl_pat, repl_val, pattern)
                return pattern
            elif first_large == NUMBER.TWO:
                if last_large != NUMBER.NINE:
                    args = (small, first_large, last_large)
                    pattern = '[%s-9]|(1[0-9])|(%s[0-%s])' % args
                    pattern = re.sub(repl_pat, repl_val, pattern)
                    return pattern
                else:
                    pattern = '[%s-9]|([1-2][0-9])' % small
                    pattern = re.sub(repl_pat, repl_val, pattern)
                    return pattern
            else:
                if last_large != NUMBER.NINE:
                    args = (small, first_large - NUMBER.ONE, first_large, last_large)
                    pattern = '[%s-9]|([1-%s][0-9])|(%s[0-%s])' % args
                    pattern = re.sub(repl_pat, repl_val, pattern)
                    return pattern
                else:
                    args = (small, first_large)
                    pattern = '[%s-9]|([1-%s][0-9])' % args
                    pattern = re.sub(repl_pat, repl_val, pattern)
                    return pattern

        elif small_width == NUMBER.TWO and large_width == NUMBER.TWO:
            if first_small == first_large:
                args = (first_small, last_small, last_large)
                pattern = '%s[%s-%s]' % args
                pattern = re.sub(repl_pat, repl_val, pattern)
                return pattern
            elif first_small + NUMBER.ONE == first_large:
                args = (first_small, last_small,
                        first_large, last_large)
                pattern = '(%s[%s-9])|(%s[0-%s])' % args
                pattern = re.sub(repl_pat, repl_val, pattern)
                return pattern
            else:
                if last_large != NUMBER.NINE:
                    args = (first_small,
                            last_small, first_small + NUMBER.ONE,
                            first_large - NUMBER.ONE, first_large, last_large)
                    pattern = '(%s[%s-9])|([%s-%s][0-9])|(%s[0-%s])' % args
                    pattern = re.sub(repl_pat, repl_val, pattern)
                    return pattern
                else:
                    args = (first_small, last_small, first_small + 1, first_large)
                    pattern = '(%s[%s-9])|([%s-%s][0-9])' % args
                    pattern = re.sub(repl_pat, repl_val, pattern)
                    return pattern

        elif small < NUMBER.HUNDRED and large == NUMBER.HUNDRED:
            pattern = self.get_pattern_for_two_unsigned_int(small, 99)
            pattern = ('(%s)|(100)' if pattern.isdigit() else '%s|(100)') % pattern
            pattern = re.sub(repl_pat, repl_val, pattern)
            return pattern

        return self.failure_fmt

    def get_pattern_for_two_numbers(self, v1, v2):
        lst = [int(v1), int(v2)]
        small, large = min(lst), max(lst)

        if small == large:
            pattern = str(small)
            return pattern
        if small >= NUMBER.ZERO and large >= NUMBER.ZERO:
            pattern = self.get_pattern_for_two_unsigned_int(small, large)
            if pattern.startswith(STRING.UNSUPPORTED_PARSING):
                failure = self.failure_fmt % (small, large)
                return failure
            pattern = '(%s)' % pattern if SYMBOL.LEFT_PARENTHESIS in pattern else pattern
            return pattern
        elif small <= NUMBER.ZERO and large <= NUMBER.ZERO:
            pattern = self.get_pattern_for_two_numbers(abs(small), abs(large))
            if pattern.startswith(STRING.UNSUPPORTED_PARSING):
                failure = self.failure_fmt % (small, large)
                return failure
            pattern = '(-%s)' % pattern if pattern else pattern
            return pattern
        else:
            pattern1 = self.get_pattern_for_two_numbers(NUMBER.ZERO, small)
            pattern2 = self.get_pattern_for_two_numbers(NUMBER.ZERO, large)
            if pattern1.startswith(STRING.UNSUPPORTED_PARSING):
                failure = self.failure_fmt % (small, large)
                return failure
            if pattern2.startswith(STRING.UNSUPPORTED_PARSING):
                failure = self.failure_fmt % (small, large)
                return failure

            pattern1 = '(%s)' % pattern1 if pattern1[:NUMBER.ONE] == '-' else pattern1
            pattern = '(%s|%s)' % (pattern1, pattern2)
            return pattern

    def parse_shell_expansion(self, data):
        match1 = re.match(r'(?i)\{(?P<first>[a-z])[.]{2}(?P<last>[a-z])\}', data)
        match2 = re.match(r'(?i)\{(?P<first>-?\d+)[.]{2}(?P<last>-?\d+)\}', data)
        match3 = re.match(r'(?i)\{[^,]*(,[^,]*)+\}', data)

        if match1:
            first = match1.group(STRING.FIRST)
            last = match1.group(STRING.LAST)
            v1 = first if first < last else last
            v2 = last if first < last else first
            total = ord(v2) - ord(v1)
            if total > 26:
                other = re.escape('[\\]^_`')
                pattern = '[%s-Za-%s%s]' % (v1, v2, other)
            else:
                pattern = '[%s-%s]' % (v1, v2)
            return pattern
        elif match2:
            first = int(match2.group(STRING.FIRST))
            last = int(match2.group(STRING.LAST))
            pattern = self.get_pattern_for_two_numbers(first, last)
            return pattern
        elif match3:
            is_empty_item = False
            lst = []
            for item in data[1:-1].split(SYMBOL.COMMA):
                if item:
                    lst.append(re.escape(item))
                else:
                    is_empty_item = True
            if lst:
                pattern = '(%s)' % SYMBOL.VERTICAL_LINE.join(lst)
                pattern = '%s?' % pattern if is_empty_item else pattern
                return pattern
            else:
                return STRING.EMPTY
        else:
            pattern = re.escape(data)
            return pattern

    def escape_data(self, data):
        uniq_str = Misc.get_uniq_number_str()
        repl1 = 'star_%s' % uniq_str
        repl2 = 'question_%s' % uniq_str
        data = data.replace(SYMBOL.ASTERISK, repl1)
        data = data.replace(SYMBOL.QUESTION_MARK, repl2)

        if re.search(r'\{.+?\}', data):
            lst = []
            start = NUMBER.ZERO
            item = None
            for item in re.finditer(r'(\\?)[{][^}]+\1[}]', data):
                pre_matched = data[start:item.start()]
                escaped_txt = re.escape(pre_matched)
                lst.append(escaped_txt)
                matched_txt = item.group()
                match_a = re.match(r'(\\?)[{] *(, *)+\1[}]', matched_txt)
                match1 = re.match(r'(\\?)[{] *\d+ *\1[}]', matched_txt)
                match2 = re.match(r'(\\?)[{] *\d* *, *\d* *\1[}]', matched_txt)
                match3 = re.match(r'[{][^}]+[}]', matched_txt)

                if match_a:
                    lst.append(STRING.EMPTY)
                elif match1 or match2:
                    new_matched_txt = matched_txt.replace('\\', '')
                    lst.append(new_matched_txt)
                elif match3:
                    expanded_txt = self.parse_shell_expansion(matched_txt)
                    lst.append(expanded_txt)
                else:
                    escaped_txt = re.escape(matched_txt)
                    lst.append(escaped_txt)
                start = item.end()
            if lst:
                post_matched = data[item.end():]
                escaped_txt = re.escape(post_matched)
                lst.append(escaped_txt)
            else:
                escaped_txt = re.escape(data)
                lst.append(escaped_txt)
            data = STRING.EMPTY.join(lst)
        else:
            data = re.escape(data)
        data = data.replace(repl1, PATTERN.SOMETHING)
        data = data.replace(repl2, PATTERN.ANYTHING_BUT)
        return data

    def parse_data(self, data):
        if re.match(PATTERN.SPACES_AT_END_OF_STR, data):
            return data if len(data) <= NUMBER.ONE else PATTERN.SPACES

        start = NUMBER.ZERO
        item = None
        lst = []
        for item in re.finditer(PATTERN.SPACES, data):
            pre_matched = data[start:item.start()]
            lst.append(self.escape_data(pre_matched))
            lst.append(PATTERN.SPACE if len(item.group()) == NUMBER.ONE else PATTERN.SPACES)
            start = item.end()

        if lst:
            post_matched = data[item.end():]
            lst.append(self.escape_data(post_matched))
        else:
            lst.append(self.escape_data(data))

        pattern = STRING.EMPTY.join(lst)
        return pattern

    def parse_single_line(self, data):
        line = data
        if not line:
            return STRING.EMPTY
        elif re.match(PATTERN.SPACES_AT_END_OF_STR, line):
            return PATTERN.SPACES

        is_started_space = bool(re.match(PATTERN.SPACE, line))
        is_ended_space = bool(re.search(PATTERN.SPACE_AT_END_OF_STR, line))
        line = line.strip()

        line = re.sub(r'(?i)\[:digit:\]', '0-9', line)
        line = re.sub(r'(?i)\[:alpha:\]', 'a-zA-Z', line)
        line = re.sub(r'(?i)\[:alnum:\]', 'a-zA-Z0-9', line)

        lst = []
        start = NUMBER.ZERO
        item = None
        for item in re.finditer(r'\[.+?\]', line):
            pre_matched = line[start:item.start()]
            lst.append(self.parse_data(pre_matched))
            matched_txt = item.group()
            if matched_txt.startswith('[!'):
                matched_txt = '[^%s' % matched_txt[2:]
            lst.append(matched_txt)
            start = item.end()

        if lst:
            post_matched = line[item.end():]
            lst.append(self.parse_data(post_matched))
        else:
            lst.append(self.parse_data(line))

        pattern = STRING.EMPTY.join(lst)
        if is_started_space or self.is_prefix:
            pattern = ' *%s' % pattern
        if is_ended_space or self.is_postfix:
            pattern = '%s *' % pattern

        return pattern

    def parse_multiline(self, data):
        lst = []
        for line in re.split(PATTERN.MULTI_CRNL, data):
            pat = self.parse_single_line(line)
            lst.append(pat)

        pattern = PATTERN.MULTI_CRNL.join(lst)
        return pattern
