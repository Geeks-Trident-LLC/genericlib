import pytest           # noqa
from textwrap import dedent

from genericlib.gptabular import TabularTextPattern


class TestTabularTextPattern:
    """Test class for TabularTextPattern"""

    def test_starting_from_and_ending_to_arguments(self):
        text = dedent("""
line 1: blab 123 blab
line 2: 1.1.2 blab blab
index     col1            col2
1         item1.1         item1.2
2         item2.1         item2.2
3         ?               item3.2
line k: 123 blab blab
index     col1            col2
4         item4.1         item4.2
5         item5.1         item5.2
6         ?               item6.2
        """).strip()

        expected_tmpl_snippet = dedent("""
index     col1            col2 -> Table
Table
start() digit(var_index)  non_whitespaces(var_col)  mixed_word(var_col2) end() -> record
line k: digits() blab blab -> EOF
        """).strip()

        node = TabularTextPattern(text, col_widths="10, 15,", starting_from=2, ending_to=6)
        tmpl_snippet = node.to_template_snippet()
        assert tmpl_snippet == expected_tmpl_snippet

