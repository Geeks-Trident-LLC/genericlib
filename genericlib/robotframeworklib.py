from genericlib import File
from textwrap import dedent
import re
import types


def to_robotframework_doc_str(py_func, rf_func=None):
    if hasattr(py_func, '__func__'):
        doc_str = dedent(py_func.__func__.__doc__ or '').strip()
    elif hasattr(py_func, '__doc__'):
        doc_str = dedent(py_func.__doc__ or '').strip()
    else:
        return

    if doc_str:
        lst = []
        for line in doc_str.splitlines():
            if line.strip():
                prefix = '' if line.startswith('|') else '| '
                lst.append('%s%s' % (prefix, line))
        if lst:
            rf_func = rf_func or py_func
            new_doc_str = str.join('\n', lst)
            if hasattr(rf_func, '__func__'):
                rf_func.__func__.__doc__ = new_doc_str
            elif hasattr(py_func, '__doc__'):
                rf_func.__doc__ = new_doc_str


def update_robot_framework_lib(rf_cls, py_cls, pattern='rf_?generic_?lib_?'):
    for attr in dir(py_cls):
        py_func = getattr(py_cls, attr)
        if callable(py_func) and re.match(pattern, attr, re.I):
            if isinstance(py_cls, types.ModuleType):
                setattr(rf_cls, attr, staticmethod(py_func))
            else:
                setattr(rf_cls, attr, py_func)
            to_robotframework_doc_str(py_func)


class RFFile:
    pass


update_robot_framework_lib(RFFile, File)
