"""Module containing the logic for utilities."""

import platform

import subprocess

from textwrap import wrap

import typing

from genericlib.constant import ECODE
from genericlib.text import Text
from genericlib.collection import DotObject


class Printer:
    """A printer class.

    Methods
    Printer.get(data, header='', footer='', failure_msg='', width=80, width_limit=20) -> str
    Printer.print(data, header='', footer='', failure_msg='', width=80, width_limit=20, print_func=None) -> None
    """
    @classmethod
    def get(cls, data, header='', footer='',
            width=80, width_limit=20, failure_msg=''):
        """Decorate data by organizing header, data, footer, and failure_msg

        Parameters
        ----------
        data (str, list): a text or a list of text.
        header (str): a header text.  Default is empty.
        footer (str): a footer text.  Default is empty.
        width (int): width of displayed text.  Default is 80.
        width_limit (int): minimum width of displayed text.  Default is 20.
        failure_msg (str): a failure message.  Default is empty.
        """
        headers = str(header).splitlines()
        footers = str(footer).splitlines()
        data = data if Misc.is_mutable_sequence(data) else [data]
        lst = []
        result = []

        right_bound = width - 4

        for item in data:
            if width >= width_limit:
                for line in str(item).splitlines():
                    lst.extend(wrap(line, width=right_bound))
            else:
                lst.extend(line.rstrip() for line in str(item).splitlines())
        length = max(len(str(i)) for i in lst + headers + footers)

        if width >= width_limit:
            length = right_bound if right_bound > length else length

        result.append(Text.format('+-{}-+', '-' * length))
        if header:
            for item in headers:
                result.append(Text.format('| {} |', item.ljust(length)))
            result.append(Text.format('+-{}-+', '-' * length))

        for item in lst:
            result.append(Text.format('| {} |', item.ljust(length)))
        result.append(Text.format('+-{}-+', '-' * length))

        if footer:
            for item in footers:
                result.append(Text.format('| {} |', item.ljust(length)))
            result.append(Text.format('+-{}-+', '-' * length))

        if failure_msg:
            result.append(failure_msg)

        txt = '\n'.join(result)
        return txt

    @classmethod
    def print(cls, data, header='', footer='',
              width=80, width_limit=20, failure_msg='', print_func=None):
        """Decorate data by organizing header, data, footer, and failure_msg

        Parameters
        ----------
        data (str, list): a text or a list of text.
        header (str): a header text.  Default is empty.
        footer (str): a footer text.  Default is empty.
        width (int): width of displayed text.  Default is 80.
        width_limit (int): minimum width of displayed text.  Default is 20.
        failure_msg (str): a failure message.  Default is empty.
        print_func (function): a print function.  Default is None.
        """

        txt = Printer.get(data, header=header, footer=footer,
                          failure_msg=failure_msg, width=width,
                          width_limit=width_limit)

        print_func = print_func if callable(print_func) else print
        print_func(txt)

    @classmethod
    def get_message(cls, fmt, *args, style='format', prefix=''):
        """Get a message

        Parameters
        ----------
        fmt (str): string format.
        args (tuple): list of parameters for string interpolation.
        style (str): either format or %.
        prefix (str): a prefix.

        Returns
        -------
        str: a message.
        """

        if args:
            message = fmt.format(*args) if style == 'format' else fmt % args
        else:
            message = fmt

        message = '{} {}'.format(prefix, message) if prefix else message
        return message

    @classmethod
    def print_message(cls, fmt, *args, style='format', prefix='', print_func=None):
        """Print a message

        Parameters
        ----------
        fmt (str): string format.
        args (tuple): list of parameters for string interpolation.
        style (str): either format or %.
        prefix (str): a prefix.
        print_func (function): a print function.
        """
        message = cls.get_message(fmt, *args, style=style, prefix=prefix)
        print_func = print_func if callable(print_func) else print
        print_func(message)


class Misc:

    message = ''

    @classmethod
    def is_dict(cls, obj):
        return isinstance(obj, typing.Dict)

    @classmethod
    def is_mapping(cls, obj):
        return isinstance(obj, typing.Mapping)

    @classmethod
    def is_list(cls, obj):
        return isinstance(obj, typing.List)

    @classmethod
    def is_mutable_sequence(cls, obj):
        return isinstance(obj, (typing.List, typing.Tuple, typing.Set))

    @classmethod
    def is_sequence(cls, obj):
        return isinstance(obj, typing.Sequence)

    @classmethod
    def try_to_get_number(cls, obj, return_type=None):
        """Try to get a number

        Parameters
        ----------
        obj (object): a number or text number.
        return_type (int, float, bool): a referred return type.

        Returns
        -------
        tuple: status of number and value of number per referred return type
        """
        chk_lst = [int, float, bool]

        if cls.is_string(obj):
            data = obj.strip()
            try:
                if data.lower() == 'true' or data.lower() == 'false':
                    result = True if data.lower() == 'true' else False
                else:
                    result = float(data) if '.' in data else int(data)

                num = return_type(result) if return_type in chk_lst else result
                return True, num
            except Exception as ex:     # noqa
                cls.message = Text(ex)
                return False, obj
        else:
            is_number = cls.is_number(obj)
            num = return_type(obj) if return_type in chk_lst else obj

            if not is_number:
                txt = obj if cls.is_class(obj) else type(obj)
                cls.message = Text.format('Expecting number type, but got {}', txt)
            return is_number, num

    @classmethod
    def is_integer(cls, obj):
        if isinstance(obj, int):
            return True
        elif cls.is_string(obj):
            chk = obj.strip().isdigit()
            return chk
        else:
            return False

    @classmethod
    def is_boolean(cls, obj):
        if isinstance(obj, bool):
            return True
        elif cls.is_string(obj):
            val = obj.strip().lower()
            chk = val == 'true' or val == 'false'
            return chk
        elif cls.is_integer(obj):
            chk = int(obj) == 0 or int(obj) == 1
            return chk
        elif cls.is_float(obj):
            chk = float(obj) == 0 or float(obj) == 1
            return chk
        else:
            return False

    @classmethod
    def is_float(cls, obj):
        if isinstance(obj, (float, int)):
            return True
        elif cls.is_string(obj):
            try:
                float(obj)
                return True
            except Exception as ex:     # noqa
                return False
        else:
            return False

    @classmethod
    def is_number(cls, obj):
        result = cls.is_boolean(obj)
        result |= cls.is_integer(obj)
        result |= cls.is_float(obj)
        return result

    @classmethod
    def is_string(cls, obj):
        return isinstance(obj, typing.Text)

    @classmethod
    def is_class(cls, obj):
        return isinstance(obj, typing.Type)     # noqa

    @classmethod
    def is_callable(cls, obj):
        return isinstance(obj, typing.Callable)

    @classmethod
    def is_iterator(cls, obj):
        return isinstance(obj, typing.Iterator)

    @classmethod
    def is_generator(cls, obj):
        return isinstance(obj, typing.Generator)

    @classmethod
    def is_iterable(cls, obj):
        return isinstance(obj, typing.Iterable)

    @classmethod
    def join_string(cls, *args, **kwargs):
        if not args:
            return ''
        if len(args) == 1:
            return str(args[0])

        sep = kwargs.get('separator', '')
        sep = kwargs.get('sep', sep)
        return sep.join(str(item) for item in args)

    @classmethod
    def skip_first_line(cls, data):
        if not cls.is_string(data):
            return data
        else:
            new_data = '\n'.join(data.splitlines()[1:])
            return new_data

    @classmethod
    def is_window_os(cls):
        chk = platform.system().lower() == 'windows'
        return chk

    @classmethod
    def is_mac_os(cls):
        chk = platform.system().lower() == 'darwin'
        return chk

    @classmethod
    def is_linux_os(cls):
        chk = platform.system().lower() == 'linux'
        return chk

    @classmethod
    def is_nix_os(cls):
        chk = cls.is_linux_os() or cls.is_mac_os()
        return chk


class MiscOutput:
    @classmethod
    def execute_shell_command(cls, cmdline):
        exit_code, output = subprocess.getstatusoutput(cmdline)
        result = DotObject(
            output=output,
            exit_code=exit_code,
            is_success=exit_code == ECODE.SUCCESS
        )
        return result
