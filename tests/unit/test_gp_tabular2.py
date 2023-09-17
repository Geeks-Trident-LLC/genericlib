import pytest           # noqa
from textwrap import dedent

from genericlib.gptabular import TabularTextPattern

#
# def test_starting_from_and_ending_to_arguments():
#     text = dedent("""
# line 1: blab 123 blab
# line 2: 1.1.2 blab blab
# index     col1            col2
# 1         item1.1         item1.2
# 2         item2.1         item2.2
# 3         ?               item3.2
# line k: 123 blab blab
# index     col1            col2
# 4         item4.1         item4.2
# 5         item5.1         item5.2
# 6         ?               item6.2
#     """).strip()
#
#     expected_tmpl_snippet = dedent("""
# index     col1            col2 -> Table
# Table
# start() digit(var_index)  non_whitespaces(var_col)  mixed_word(var_col2) end() -> record
# line k: digits() blab blab -> EOF
#     """).strip()
#
#     node = TabularTextPattern(text, col_widths="10, 15,", starting_from=2, ending_to=6)
#     tmpl_snippet = node.to_template_snippet()
#     assert tmpl_snippet == expected_tmpl_snippet


def test_tabular_emtpy_every_column():
    text = dedent("""
one       two       three
--------  --------  ---------- 
item1.1   item1.2   item1.3
item2.1   item2.2
item3.1             item3.3
          item4.2   item4.3
item5.1
          item6.2
                    item7.3
    """).strip()

    expected_tmpl_snippet = dedent("""
one       two       three
start(space) mixed_word(var_one, or_either_repeating_7_20_spaces) mixed_word(var_two, or_either_repeating_7_20_spaces) mixed_word(var_three, or_either_repeating_7_7_spaces) end(space) -> record
start(space) mixed_word(var_one, or_either_repeating_7_20_spaces) mixed_word(var_two, or_either_repeating_7_20_spaces) end(space) -> record
start(space) mixed_word(var_one, or_either_repeating_7_20_spaces) end(space) -> record
    """).strip()    # noqa

    node = TabularTextPattern(text)
    tmpl_snippet = node.to_template_snippet()
    assert tmpl_snippet == expected_tmpl_snippet


def test_tabular_user_marker_one_line():
    text = dedent("""
a        b       c
-------- ------- -------------
val1.1   val1.2  val1.3
<user-marker-one-line>val2.1-very-long-text
         val2.2  val2.3
val3.1   val3.2  val3.3
    """).strip()

    expected_tmpl_snippet = dedent("""
a        b       c
start() mixed_word(var_a) end(space) -> Next
start() space(repetition_6_10)  mixed_word(var_b)  mixed_word(var_c) end() -> record
start() mixed_word(var_a)  mixed_word(var_b)  mixed_word(var_c) end() -> record
    """).strip()    # noqa

    node = TabularTextPattern(text)
    tmpl_snippet = node.to_template_snippet()
    assert tmpl_snippet == expected_tmpl_snippet


def test_tabular_user_marker_multi_line():
    text = dedent("""
a        b       c
-------- ------- -------------
val1.1   val1.2  val1.3
<user-marker-multi-line>val2.1   val2.2  val2.3
                 continue-val2.4
                 continue-val2.5
val3.1   val3.2  val3.3
    """).strip()

    expected_tmpl_snippet = dedent("""
a        b       c
start() mixed_word()zero_or_spaces() -> continue.record
start() mixed_word(var_a)  mixed_word(var_b)  mixed_word(var_c, meta_data_list) end(space) -> continue
start() space(repetition_11_19)  mixed_word(var_c, meta_data_list) end(space) -> continue
    """).strip()    # noqa

    node = TabularTextPattern(text)
    tmpl_snippet = node.to_template_snippet()
    assert tmpl_snippet == expected_tmpl_snippet
