# from time import time
from .constant import STRING
import re

from .exceptions import LineArgumentError


class BaseText(str):
    def __new__(cls, *args, **kwargs):
        arg0 = args[0] if args else None
        if args and isinstance(arg0, BaseException):
            txt = str.__new__(cls, '{}: {}'.format(type(arg0).__name__, arg0))
            return txt
        else:
            txt = str.__new__(cls, *args, **kwargs)
            return txt


class Text(BaseText):
    @classmethod
    def format(cls, *args, **kwargs):
        if not args:
            text = ''
            return text
        else:
            if kwargs:
                fmt = args[0]
                try:
                    text = str(fmt).format(args[1:], **kwargs)
                    return text
                except Exception as ex:
                    text = cls(ex)
                    return text
            else:
                if len(args) == 1:
                    text = cls(args[0])
                    return text
                else:
                    fmt = args[0]
                    t_args = tuple(args[1:])
                    try:
                        if len(t_args) == 1 and isinstance(t_args[0], dict):
                            text = str(fmt) % t_args[0]
                        else:
                            text = str(fmt) % t_args

                        if text == fmt:
                            text = str(fmt).format(*t_args)
                        return text
                    except Exception as ex1:
                        try:
                            text = str(fmt).format(*t_args)
                            return text
                        except Exception as ex2:
                            text = '%s\n%s' % (cls(ex1), cls(ex2))
                            return text

    @classmethod
    def wrap_html(cls, tag, data, *args):
        data = str(data)
        tag = str(tag).strip()
        attributes = [str(arg).strip() for arg in args if str(arg).strip()]
        if attributes:
            attrs_txt = str.join(STRING.SPACE_CHAR, attributes)
            if data.strip():
                result = '<{0} {1}>{2}</{0}>'.format(tag, attrs_txt, data)
            else:
                result = '<{0} {1}/>'.format(tag, attrs_txt)
        else:
            if data.strip():
                result = '<{0}>{1}</{0}>'.format(tag, data)
            else:
                result = '<{0}/>'.format(tag)
        return result


class Line(BaseText):
    def __init__(self, data):
        type(self).is_line(data, on_failure=True)
        lines = str(data).splitlines(keepends=True)
        self.__line = lines[0] if lines else ''
        self.__data = re.match(r"([^\r\n]+)?", self.__line)
        self.__joiner = re.search(r"([\r\n]+)?$", self.__line)
        super().__init__(self.__data)

    @property
    def joiner(self):
        return self.__joiner

    @property
    def raw_data(self):
        return self.__line

    @property
    def clean_line(self):
        return self.strip()

    @property
    def is_empty(self):
        return self == ""

    @property
    def is_optional_empty(self):
        return bool(re.match(r"\s+$", self))

    @property
    def leading(self):
        leading_chars = re.match(r'(\s+)?', self).group()
        return leading_chars

    @property
    def trailing(self):
        trailing_chars = re.search(r'(\s+)?$', self).group()
        return trailing_chars

    @property
    def is_leading(self):
        return len(self.leading) > 0

    @property
    def is_trailing(self):
        return len(self.trailing) > 0

    @classmethod
    def is_line(cls, data, on_failure=False):
        lines = str(data).splitlines(keepends=True)
        if len(lines) == 1:
            return True

        if on_failure:
            error = "data argument is multi-lines.  MUST be a single line."
            raise LineArgumentError(error)
        else:
            return False


def get_generic_error_msg(instance, fmt, *other):
    args = ['%sError' % instance.__class__.__name__]
    args.extend(other)
    new_fmt = '%%s - %s' % fmt
    err_msg = new_fmt % tuple(args)
    return err_msg


def get_whitespace_chars(k=8, to_list=True):
    lst = [chr(i) for i in range(pow(2, k)) if re.search(r"\s", chr(i))]
    return frozenset(lst) if to_list else str.join('', lst)


ASCII_WHITESPACE_CHARS = get_whitespace_chars(k=8, to_list=True)
ASCII_WHITESPACE_STRING = get_whitespace_chars(k=8, to_list=False)
WHITESPACE_CHARS = get_whitespace_chars(k=16, to_list=True)
WHITESPACE_STRING = get_whitespace_chars(k=16, to_list=False)


def get_non_whitespace_chars(k=8, to_list=True):
    lst = [chr(i) for i in range(pow(2, k)) if not re.search(r"\s", chr(i))]
    return frozenset(lst) if to_list else str.join('', lst)


ASCII_NON_WHITESPACE_CHARS = get_non_whitespace_chars(k=8, to_list=True)
ASCII_NON_WHITESPACE_STRING = get_non_whitespace_chars(k=8, to_list=False)
NON_WHITESPACE_CHARS = get_non_whitespace_chars(k=16, to_list=True)
NON_WHITESPACE_STRING = get_non_whitespace_chars(k=16, to_list=False)