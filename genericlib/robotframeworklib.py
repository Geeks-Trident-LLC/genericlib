from genericlib import File
from textwrap import dedent
import re


def to_robotframework_doc_str(func):
    doc_str = dedent(func.__doc__ or '').strip()
    if doc_str:
        lst = []
        for line in doc_str.splitlines():
            if line.strip():
                prefix = '' if line.startswith('|') else '| '
                lst.append('%s%s' % (prefix, line))
        if lst:
            func.__func__.__doc__ = str.join('\n', lst)


def update_robot_framework_lib(rf_cls, py_cls, pattern='rf_?generic_?lib_?'):
    for attr in dir(py_cls):
        obj = getattr(py_cls, attr)
        if callable(obj) and re.match(pattern, attr, re.I):
            setattr(rf_cls, attr, obj)
            to_robotframework_doc_str(obj)


class RFFile:
    pass


update_robot_framework_lib(RFFile, File)
