import pytest           # noqa
from textwrap import dedent

from genericlib.gptabular import TabularTextPattern


def test_tabular_calculating_max_width():
    text = dedent("""
a        b      
-------- -------
val1.1   val1.2
         val2.2
val3.1
val4.1   val4.2
val5.1
    """).strip()

    expected_tmpl_snippet = dedent("""
    """).strip()

    node = TabularTextPattern(text)
    tmpl_snippet = node.to_template_snippet()
    assert tmpl_snippet == expected_tmpl_snippet
