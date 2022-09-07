import re

import pytest           # noqa
from textwrap import dedent

from genericlib import Misc
from genericlib import MiscObject

from genericlib.gp import verify
from genericlib.gp import get_textfsm_template

from genericlib.gp import TabularTextPatternByFixedColumns


class TestTabularTextPatternByFixedColumns:
    """Test class for CategoryLinesPattern"""

    @pytest.mark.parametrize(
        "text,col_widths,headers,headers_data,expected_pattern,expected_result",
        [
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                '',
                '',
                '(?P<col0>.{10})(?P<col1>.{10})(?P<col2>.*)',
                [
                    {'col0': 'fruits', 'col1': 'meat', 'col2': 'drinks'},
                    {'col0': 'orange', 'col1': 'pork', 'col2': 'water'},
                    {'col0': 'peach', 'col1': '', 'col2': 'pepsi soda'},
                 ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                ['fruits', 'meat', 'drinks'],
                '',
                '(?P<fruits>.{10})(?P<meat>.{10})(?P<drinks>.*)',
                [
                    {'fruits': 'fruits', 'meat': 'meat', 'drinks': 'drinks'},
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                'fruits, meat, drinks',
                '',
                '(?P<fruits>.{10})(?P<meat>.{10})(?P<drinks>.*)',
                [
                    {'fruits': 'fruits', 'meat': 'meat', 'drinks': 'drinks'},
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                '',
                'fruits    meat      drinks',
                '(?P<fruits>.{10})(?P<meat>.{10})(?P<drinks>.*)',
                [
                    {'fruits': 'fruits', 'meat': 'meat', 'drinks': 'drinks'},
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                '',
                '0',
                '(?P<fruits>.{10})(?P<meat>.{10})(?P<drinks>.*)',
                [
                    {'fruits': 'fruits', 'meat': 'meat', 'drinks': 'drinks'},
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                '',
                [0],
                '(?P<fruits>.{10})(?P<meat>.{10})(?P<drinks>.*)',
                [
                    {'fruits': 'fruits', 'meat': 'meat', 'drinks': 'drinks'},
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
        ]
    )
    def test_to_regex(self, text, col_widths, headers, headers_data,
                      expected_pattern, expected_result):
        node = TabularTextPatternByFixedColumns(
            text, col_widths=col_widths, headers=headers, headers_data=headers_data
        )
        pattern = node.to_regex()
        assert pattern == expected_pattern

        lst_of_dict_result = []
        lines = Misc.get_list_of_lines(text)
        for line in lines:
            match = re.search(pattern, line)
            if match:
                lst_of_dict_result.append(match.groupdict())
        lst_of_dict_result = MiscObject.cleanup_list_of_dict(lst_of_dict_result)
        assert lst_of_dict_result == expected_result

    @pytest.mark.parametrize(
        "text,col_widths,headers,headers_data,expected_template_snippet,expected_template,expected_result",
        [
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                '',
                '',
                'anything(var_col0, repetition_10)anything(var_col1, repetition_10)something(var_col2) -> record',
                dedent("""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value col0 (.{10})
                    Value col1 (.{10})
                    Value col2 (.*)

                    Start
                      ^${col0}${col1}${col2} -> Record
                """).strip(),
                [
                    {'col0': 'fruits', 'col1': 'meat', 'col2': 'drinks'},
                    {'col0': 'orange', 'col1': 'pork', 'col2': 'water'},
                    {'col0': 'peach', 'col1': '', 'col2': 'pepsi soda'},
                 ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                ['fruits', 'meat', 'drinks'],
                '',
                'anything(var_fruits, repetition_10)anything(var_meat, repetition_10)something(var_drinks) -> record',
                dedent("""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits (.{10})
                    Value meat (.{10})
                    Value drinks (.*)

                    Start
                      ^${fruits}${meat}${drinks} -> Record
                """).strip(),
                [
                    {'fruits': 'fruits', 'meat': 'meat', 'drinks': 'drinks'},
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                'fruits, meat, drinks',
                '',
                'anything(var_fruits, repetition_10)anything(var_meat, repetition_10)something(var_drinks) -> record',
                dedent("""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits (.{10})
                    Value meat (.{10})
                    Value drinks (.*)

                    Start
                      ^${fruits}${meat}${drinks} -> Record
                """).strip(),
                [
                    {'fruits': 'fruits', 'meat': 'meat', 'drinks': 'drinks'},
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                '',
                'fruits    meat      drinks',
                dedent("""
                    fruits    meat      drinks
                    anything(var_fruits, repetition_10)anything(var_meat, repetition_10)something(var_drinks) -> record
                """).strip(),
                dedent("""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits (.{10})
                    Value meat (.{10})
                    Value drinks (.*)

                    Start
                      ^fruits +meat +drinks
                      ^${fruits}${meat}${drinks} -> Record
                """).strip(),
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                '',
                '0',
                dedent("""
                    fruits    meat      drinks
                    anything(var_fruits, repetition_10)anything(var_meat, repetition_10)something(var_drinks) -> record
                """).strip(),
                dedent("""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits (.{10})
                    Value meat (.{10})
                    Value drinks (.*)

                    Start
                      ^fruits +meat +drinks
                      ^${fruits}${meat}${drinks} -> Record
                """).strip(),
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                [10, 10, 0],
                '',
                [0],
                dedent("""
                    fruits    meat      drinks
                    anything(var_fruits, repetition_10)anything(var_meat, repetition_10)something(var_drinks) -> record
                """).strip(),
                dedent("""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits (.{10})
                    Value meat (.{10})
                    Value drinks (.*)

                    Start
                      ^fruits +meat +drinks
                      ^${fruits}${meat}${drinks} -> Record
                """).strip(),
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                ]
            ),
        ]
    )
    def test_to_regex(self, text, col_widths, headers, headers_data,
                      expected_template_snippet, expected_template,
                      expected_result):
        node = TabularTextPatternByFixedColumns(
            text, col_widths=col_widths, headers=headers, headers_data=headers_data
        )
        tmpl_snippet = node.to_template_snippet()

        assert tmpl_snippet == expected_template_snippet
        template = get_textfsm_template(tmpl_snippet)
        template = re.sub(r'\d{4}-\d\d-\d\d', 'YYYY-mm-dd', template)
        assert template == expected_template
        verify(tmpl_snippet, text, expected_result=expected_result)
