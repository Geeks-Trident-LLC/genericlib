import re

from .utils import Misc
from .constant import STRING
from .constnum import NUMBER
from .constsymbol import SYMBOL


class Wildcard:
    def __init__(self, data, is_prefix=True, is_postfix=True, ignore_case=True):
        self.data = str(data)
        self.is_prefix = is_prefix
        self.is_postfix = is_postfix
        self.ignore_case = ignore_case
        self.is_multiline = bool(re.search(r'[\r\n]', self.data))

        self._pattern = STRING.EMPTY
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
                replaced = ' *' if len(start) > NUMBER.EIGHT else STRING.EMPTY
            elif end:
                replaced = ' *' if len(end) > NUMBER.EIGHT else STRING.EMPTY
            else:
                replaced = ' *' if len(middle) > NUMBER.EIGHT else STRING.EMPTY
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

        fmt = 'Unsupported parsing two integers (%s, %s)'
        return fmt

    def get_pattern_for_two_numbers(self, v1, v2):
        lst = [int(v1), int(v2)]
        small, large = min(lst), max(lst)

        if small == large:
            pattern = str(small)
            return pattern
        if small >= NUMBER.ZERO and large >= NUMBER.ZERO:
            pattern = self.get_pattern_for_two_unsigned_int(small, large)
            if pattern.startswith('Unsupported parsing'):
                return pattern % (small, large)
            pattern = '(%s)' % pattern if SYMBOL.LEFT_PARENTHESIS in pattern else pattern
            return pattern
        elif small <= 0 and large <= 0:
            pattern = self.get_pattern_for_two_numbers(abs(small), abs(large))
            if pattern.startswith('Unsupported parsing'):
                return pattern % (small, large)
            pattern = '(-%s)' % pattern if pattern else pattern
            return pattern
        else:
            pattern1 = self.get_pattern_for_two_numbers(NUMBER.ZERO, small)
            pattern2 = self.get_pattern_for_two_numbers(NUMBER.ZERO, large)
            if pattern1.startswith('Unsupported parsing'):
                return pattern1 % (small, large)
            if pattern2.startswith('Unsupported parsing'):
                return pattern2 % (small, large)

            pattern1 = '(%s)' % pattern1 if pattern1[:NUMBER.ONE] == '-' else pattern1
            pattern = '(%s|%s)' % (pattern1, pattern2)
            return pattern

    def parse_shell_expansion(self, data):
        match1 = re.match(r'(?i)\{(?P<first>[a-z])[.]{2}(?P<last>[a-z])\}', data)
        match2 = re.match(r'(?i)\{(?P<first>-?\d+)[.]{2}(?P<last>-?\d+)\}', data)
        match3 = re.match(r'(?i)\{[^,]+(,[^,]+)+\}', data)

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
            lst = [re.escape(i) for i in data[1:-1].split(SYMBOL.COMMA)]
            pattern = '(%s)' % SYMBOL.VERTICAL_LINE.join(lst)
            return pattern
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
            for item in re.finditer(r'\{.+?\}', data):
                pre_matched = data[start:item.start()]
                lst.append(re.escape(pre_matched))
                matched_txt = item.group()
                lst.append(self.parse_shell_expansion(matched_txt))
                start = item.end()
            if lst:
                post_matched = data[item.end():]
                lst.append(re.escape(post_matched))
            else:
                lst.append(re.escape(data))
            data = STRING.EMPTY.join(lst)
        else:
            data = re.escape(data)
        data = data.replace(repl1, '.*')
        data = data.replace(repl2, '.?')
        return data

    def parse_data(self, data):
        if re.match(' +$', data):
            return data if len(data) <= 1 else ' +'

        start = NUMBER.ZERO
        item = None
        lst = []
        for item in re.finditer(' +', data):
            pre_matched = data[start:item.start()]
            lst.append(self.escape_data(pre_matched))
            lst.append(' ' if len(item.group()) == 1 else ' +')
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
        elif re.match(' +$', line):
            return ' +'

        is_started_space = bool(re.match(' ', line))
        is_ended_space = bool(re.search(' $', line))
        line = line.strip()

        line = re.sub(r'(?i)\[:digit:\]', '0-9', line)
        line = re.sub(r'(?i)\[:alpha:\]', 'a-zA-Z', line)
        line = re.sub(r'(?i)\[:alnum:\]', 'a-zA-Z0-9', line)

        lst = []
        start = 0
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
        for line in re.split(r'[\r\n]+', data):
            pat = self.parse_single_line(line)
            lst.append(pat)

        pattern = r'[\r\n]+'.join(lst)
        return pattern
