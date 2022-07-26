import re

from .utils import Misc
from .constant import STRING
from .constnum import NUMBER


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
            start = match.groupdict().get('start', STRING.EMPTY)
            end = match.groupdict().get('end', STRING.EMPTY)
            middle = match.groupdict().get('middle', STRING.EMPTY)
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

    def parse_shell_expansion(self, data):      # noqa
        match1 = re.match(r'(?i)\{(?P<first>[a-z])[.]{2}(?P<last>[a-z])\}', data)
        match2 = re.match(r'(?i)\{(?P<first>-?\d)[.]{2}(?P<last>-?\d)\}', data)
        match3 = re.match(r'(?i)\{[^,]+(,[^,]+)+\}', data)

        if match1:
            first = match1.group('first')
            last = match1.group('last')
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
            first = int(match2.group('first'))
            last = int(match2.group('last'))
            v1 = first if first < last else last
            v2 = last if first < last else first
            max_num = max(abs(v1), abs(v2))
            width = len(str(max_num))
            other = '-?' if v1 < 0 or v2 < 0 else ''

            if width == 1:
                if v1 <= 0 and v2 <= 0:
                    pattern = '-[%s-%s]' % (abs(v2), abs(v1))
                elif v1 >= 0 and v2 >= 0:
                    pattern = '[%s-%s]' % (v1, v2)
                if other:
                    pattern = '%s[0-%s]' % (other, max_num)
                return pattern
            else:
                pattern = '%s[0-9]{1,%s}' % (other, width)
                return pattern

        elif match3:
            lst = [re.escape(i) for i in data[1:-1].split(',')]
            pattern = '(%s)' % '|'.join(lst)
            return pattern
        else:
            pattern = re.escape(data)
            return pattern

    def escape_data(self, data):
        uniq_str = Misc.get_uniq_number_str()
        repl1 = 'star_%s' % uniq_str
        repl2 = 'question_%s' % uniq_str
        data = data.replace('*', repl1)
        data = data.replace('?', repl2)

        if re.search(r'\{.+?\}', data):
            lst = []
            start = 0
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
            data = ''.join(lst)
        else:
            data = re.escape(data)
        data = data.replace(repl1, '.*')
        data = data.replace(repl2, '.?')
        return data

    def parse_data(self, data):
        if re.match(' +$', data):
            return data if len(data) <= 1 else ' +'

        start = 0
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

        pattern = ''.join(lst)
        return pattern

    def parse_single_line(self, data):
        line = data
        if not line:
            return ''
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

        pattern = ''.join(lst)
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
