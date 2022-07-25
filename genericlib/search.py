import re
import fnmatch

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

    def parse_single_line(self, data):
        line = data
        if not line:
            return ''
        elif re.match(' +$', line):
            return ' +'
        else:
            is_started_space = bool(re.match(' ', line))
            is_ended_space = bool(re.search(' $', line))
            replaced_pat = r'[(][?]+s:(.*)[)][\\]Z$'
            lst = []
            for item in re.split(' +', line.strip()):
                if '*' in item:
                    sub_lst = []
                    for sub_item in re.split('[*]+', item):
                        if sub_item:
                            sub_pat = fnmatch.translate(sub_item)
                            new_sub_pat = re.sub(replaced_pat, r'\1', sub_pat)
                            sub_lst.append(new_sub_pat)
                        else:
                            sub_lst.append('')

                    new_pat = '.*'.join(sub_lst)
                    lst.append(new_pat)
                else:
                    if item:
                        pat = fnmatch.translate(item)
                        new_pat = re.sub(replaced_pat, r'\1', pat)
                        lst.append(new_pat)
                    else:
                        lst.append('')

            pattern = r' +'.join(lst)
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
