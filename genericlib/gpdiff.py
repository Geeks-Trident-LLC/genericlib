import re
from difflib import ndiff
from itertools import combinations

from regexpro import TextPattern

from genericlib import STRING, PATTERN, Misc, NUMBER
from genericlib.gp import RuntimeException, TranslatedPattern


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
