import re

import pytest           # noqa
from textwrap import dedent

from genericlib import Misc
from genericlib import MiscObject

from genericlib import get_data_as_tabular

from genericlib.gp import verify
from genericlib.gp import get_textfsm_template

from genericlib.gp import TabularTextPatternByVarColumns


class TestTabularTextPatternByVarColumns:
    """Test class for TabularTextPatternByVarColumns"""

    @pytest.mark.parametrize(
        "text,columns_count,expected_result,expected_result_as_tabular_text",
        [
            (
                dedent("""
                    LastWriteTime          Name
                    -------------          ----
                    9/1/2021 6:13:50 AM    reference
                    10/5/2021 9:13:50 PM   dsc
                    11/2/2021 11:58:45 PM  README.md
                    12/16/2021 12:30:59 PM CONTRIBUTING.md
                """).strip(),
                2,
                [
                    {'lastwritetime': '9/1/2021 6:13:50 AM', 'name': 'reference'},
                    {'lastwritetime': '10/5/2021 9:13:50 PM', 'name': 'dsc'},
                    {'lastwritetime': '11/2/2021 11:58:45 PM', 'name': 'README.md'},
                    {'lastwritetime': '12/16/2021 12:30:59 PM', 'name': 'CONTRIBUTING.md'}
                ],
                dedent("""
                    +------------------------+-----------------+
                    | lastwritetime          | name            |
                    +------------------------+-----------------+
                    | 9/1/2021 6:13:50 AM    | reference       |
                    | 10/5/2021 9:13:50 PM   | dsc             |
                    | 11/2/2021 11:58:45 PM  | README.md       |
                    | 12/16/2021 12:30:59 PM | CONTRIBUTING.md |
                    +------------------------+-----------------+
                """).strip()
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    --------  ------    ------------
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                3,
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'}
                ],
                dedent("""
                    +--------+------+------------+
                    | fruits | meat | drinks     |
                    +--------+------+------------+
                    | orange | pork | water      |
                    | peach  |      | pepsi soda |
                    +--------+------+------------+
                """).strip()
            ),
        ]
    )
    def test_parse_table_for_symbols_divider_case(
        self, text, columns_count, expected_result, expected_result_as_tabular_text
    ):
        node = TabularTextPatternByVarColumns(text, columns_count=columns_count)
        table = node.parse_table()
        assert table

        lst_of_dict = table.to_list_of_dict()
        assert lst_of_dict == expected_result

        tabular_txt = get_data_as_tabular(lst_of_dict)
        assert tabular_txt == expected_result_as_tabular_text

    @pytest.mark.parametrize(
        "text,columns_count,divider,expected_result,expected_result_as_tabular_text",
        [
            (
                dedent("""
                    LastWriteTime           Name
                    ----------------------|--------------------
                    9/1/2021 6:13:50 AM   | reference
                    10/5/2021 9:13:50 PM  | dsc
                    11/2/2021 11:58:45 PM | README.md
                    12/16/2021 12:30:59 PM| CONTRIBUTING.md
                """).strip(),
                2,
                '|',
                [
                    {'lastwritetime': '9/1/2021 6:13:50 AM', 'name': 'reference'},
                    {'lastwritetime': '10/5/2021 9:13:50 PM', 'name': 'dsc'},
                    {'lastwritetime': '11/2/2021 11:58:45 PM', 'name': 'README.md'},
                    {'lastwritetime': '12/16/2021 12:30:59 PM', 'name': 'CONTRIBUTING.md'}
                ],
                dedent("""
                    +------------------------+-----------------+
                    | lastwritetime          | name            |
                    +------------------------+-----------------+
                    | 9/1/2021 6:13:50 AM    | reference       |
                    | 10/5/2021 9:13:50 PM   | dsc             |
                    | 11/2/2021 11:58:45 PM  | README.md       |
                    | 12/16/2021 12:30:59 PM | CONTRIBUTING.md |
                    +------------------------+-----------------+
                """).strip()
            ),
            (
                dedent("""
                    fruits   | meat    | drinks
                    ---------|---------|------------
                    orange   | pork    | water
                    peach    |         | pepsi soda
                """).strip(),
                3,
                '|',
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'}
                ],
                dedent("""
                    +--------+------+------------+
                    | fruits | meat | drinks     |
                    +--------+------+------------+
                    | orange | pork | water      |
                    | peach  |      | pepsi soda |
                    +--------+------+------------+
                """).strip()
            ),
            (
                dedent("""
                    +------------+-------------+---------------+
                    | fruits     |    meat     |        drinks |
                    +------------+-------------+---------------+
                    | orange     |    pork     |         water |
                    | peach      |             |    pepsi soda |
                    +------------+-------------+---------------+
                """).strip(),
                3,
                '|',
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'}
                ],
                dedent("""
                    +--------+------+------------+
                    | fruits | meat | drinks     |
                    +--------+------+------------+
                    | orange | pork | water      |
                    | peach  |      | pepsi soda |
                    +--------+------+------------+
                """).strip()
            ),
            (
                dedent("""
                    ------------+-------------+---------------+
                     fruits     |    meat     |        drinks |
                    ------------+-------------+---------------+
                     orange     |    pork     |         water |
                     peach      |             |    pepsi soda |
                    ------------+-------------+---------------+
                """).strip(),
                3,
                '|',
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'}
                ],
                dedent("""
                    +--------+------+------------+
                    | fruits | meat | drinks     |
                    +--------+------+------------+
                    | orange | pork | water      |
                    | peach  |      | pepsi soda |
                    +--------+------+------------+
                """).strip()
            ),
            (
                dedent("""
                    +------------+-------------+---------------
                    | fruits     |    meat     |        drinks        
                    +------------+-------------+---------------
                    | orange     |    pork     |         water 
                    | peach      |             |    pepsi soda 
                    +------------+-------------+---------------
                """).strip(),
                3,
                '|',
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'}
                ],
                dedent("""
                    +--------+------+------------+
                    | fruits | meat | drinks     |
                    +--------+------+------------+
                    | orange | pork | water      |
                    | peach  |      | pepsi soda |
                    +--------+------+------------+
                """).strip()
            ),
        ]
    )
    def test_parse_table_for_separator_divider_case(
        self, text, columns_count, divider, expected_result, expected_result_as_tabular_text
    ):
        node = TabularTextPatternByVarColumns(text, columns_count=columns_count, divider=divider)
        table = node.parse_table()
        assert table

        lst_of_dict = table.to_list_of_dict()
        assert lst_of_dict == expected_result

        tabular_txt = get_data_as_tabular(lst_of_dict)
        assert tabular_txt == expected_result_as_tabular_text

    @pytest.mark.parametrize(
        "text,columns_count,expected_result,expected_result_as_tabular_text",
        [
            (
                dedent("""
                    LastWriteTime          Name
                    9/1/2021 6:13:50 AM    reference
                    10/5/2021 9:13:50 PM   dsc
                    11/2/2021 11:58:45 PM  README.md
                    12/16/2021 12:30:59 PM CONTRIBUTING.md
                """).strip(),
                2,
                [
                    {'lastwritetime': '9/1/2021 6:13:50 AM', 'name': 'reference'},
                    {'lastwritetime': '10/5/2021 9:13:50 PM', 'name': 'dsc'},
                    {'lastwritetime': '11/2/2021 11:58:45 PM', 'name': 'README.md'},
                    {'lastwritetime': '12/16/2021 12:30:59 PM', 'name': 'CONTRIBUTING.md'}
                ],
                dedent("""
                    +------------------------+-----------------+
                    | lastwritetime          | name            |
                    +------------------------+-----------------+
                    | 9/1/2021 6:13:50 AM    | reference       |
                    | 10/5/2021 9:13:50 PM   | dsc             |
                    | 11/2/2021 11:58:45 PM  | README.md       |
                    | 12/16/2021 12:30:59 PM | CONTRIBUTING.md |
                    +------------------------+-----------------+
                """).strip()
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                3,
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'}
                ],
                dedent("""
                    +--------+------+------------+
                    | fruits | meat | drinks     |
                    +--------+------+------------+
                    | orange | pork | water      |
                    | peach  |      | pepsi soda |
                    +--------+------+------------+
                """).strip()
            ),
        ]
    )
    def test_parse_table_for_multi_spaces_case(
        self, text, columns_count, expected_result, expected_result_as_tabular_text
    ):
        node = TabularTextPatternByVarColumns(text, columns_count=columns_count, divider='  ')
        table = node.parse_table()
        assert table

        lst_of_dict = table.to_list_of_dict()
        assert lst_of_dict == expected_result

        tabular_txt = get_data_as_tabular(lst_of_dict)
        assert tabular_txt == expected_result_as_tabular_text

    @pytest.mark.parametrize(
        "text,columns_count,expected_result,expected_result_as_tabular_text",
        [
            (
                dedent("""
                    LastWriteTime          Name
                    9/1/2021 6:13:50 AM    reference
                    10/5/2021 9:13:50 PM   dsc
                    11/2/2021 11:58:45 PM  README.md
                    12/16/2021 12:30:59 PM CONTRIBUTING.md
                """).strip(),
                2,
                [
                    {'lastwritetime': '9/1/2021 6:13:50 AM', 'name': 'reference'},
                    {'lastwritetime': '10/5/2021 9:13:50 PM', 'name': 'dsc'},
                    {'lastwritetime': '11/2/2021 11:58:45 PM', 'name': 'README.md'},
                    {'lastwritetime': '12/16/2021 12:30:59 PM', 'name': 'CONTRIBUTING.md'}
                ],
                dedent("""
                    +------------------------+-----------------+
                    | lastwritetime          | name            |
                    +------------------------+-----------------+
                    | 9/1/2021 6:13:50 AM    | reference       |
                    | 10/5/2021 9:13:50 PM   | dsc             |
                    | 11/2/2021 11:58:45 PM  | README.md       |
                    | 12/16/2021 12:30:59 PM | CONTRIBUTING.md |
                    +------------------------+-----------------+
                """).strip()
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                3,
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'}
                ],
                dedent("""
                    +--------+------+------------+
                    | fruits | meat | drinks     |
                    +--------+------+------------+
                    | orange | pork | water      |
                    | peach  |      | pepsi soda |
                    +--------+------+------------+
                """).strip()
            ),
        ]
    )
    def test_parse_table_for_blank_space_case(
        self, text, columns_count, expected_result, expected_result_as_tabular_text
    ):
        node = TabularTextPatternByVarColumns(text, columns_count=columns_count, divider=' ')
        table = node.parse_table()
        assert table

        lst_of_dict = table.to_list_of_dict()
        assert lst_of_dict == expected_result

        tabular_txt = get_data_as_tabular(lst_of_dict)
        assert tabular_txt == expected_result_as_tabular_text

    @pytest.mark.parametrize(
        "text,columns_count,custom_headers_data,expected_result,expected_result_as_tabular_text",
        [
            (
                dedent("""
                    LastWriteTime          Name
                    9/1/2021 6:13:50 AM    reference
                    10/5/2021 9:13:50 PM   dsc
                    11/2/2021 11:58:45 PM  README.md
                    12/16/2021 12:30:59 PM CONTRIBUTING.md
                """).strip(),
                2,
                '---------------------- ---------------',
                [
                    {'col0': 'LastWriteTime', 'col1': 'Name'},
                    {'col0': '9/1/2021 6:13:50 AM', 'col1': 'reference'},
                    {'col0': '10/5/2021 9:13:50 PM', 'col1': 'dsc'},
                    {'col0': '11/2/2021 11:58:45 PM', 'col1': 'README.md'},
                    {'col0': '12/16/2021 12:30:59 PM', 'col1': 'CONTRIBUTING.md'}
                ],
                dedent("""
                    +------------------------+-----------------+
                    | col0                   | col1            |
                    +------------------------+-----------------+
                    | LastWriteTime          | Name            |
                    | 9/1/2021 6:13:50 AM    | reference       |
                    | 10/5/2021 9:13:50 PM   | dsc             |
                    | 11/2/2021 11:58:45 PM  | README.md       |
                    | 12/16/2021 12:30:59 PM | CONTRIBUTING.md |
                    +------------------------+-----------------+
                """).strip()
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                3,
                '--------- --------- -----------',
                [
                    {'col0': 'fruits', 'col1': 'meat', 'col2': 'drinks'},
                    {'col0': 'orange', 'col1': 'pork', 'col2': 'water'},
                    {'col0': 'peach', 'col1': '', 'col2': 'pepsi soda'}
                ],
                dedent("""
                    +--------+------+------------+
                    | col0   | col1 | col2       |
                    +--------+------+------------+
                    | fruits | meat | drinks     |
                    | orange | pork | water      |
                    | peach  |      | pepsi soda |
                    +--------+------+------------+
                """).strip()
            ),
        ]
    )
    def test_parse_table_for_blank_space_case(
        self, text, columns_count, custom_headers_data,
        expected_result, expected_result_as_tabular_text
    ):
        node = TabularTextPatternByVarColumns(text, columns_count=columns_count,
                                              custom_headers_data=custom_headers_data)
        table = node.parse_table()
        assert table

        lst_of_dict = table.to_list_of_dict()
        assert lst_of_dict == expected_result

        tabular_txt = get_data_as_tabular(lst_of_dict)
        assert tabular_txt == expected_result_as_tabular_text

    @pytest.mark.parametrize(
        "text,columns_count,expected_pattern,expected_results",
        [
            (
                dedent("""
                    LastWriteTime          Name
                    9/1/2021 6:13:50 AM    reference
                    10/5/2021 9:13:50 PM   dsc
                    11/2/2021 11:58:45 PM  README.md
                    12/16/2021 12:30:59 PM CONTRIBUTING.md
                """).strip(),
                2,
                r'(?P<lastwritetime>[\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*){,2}) +(?P<name>[\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)', # noqa
                [
                    {'lastwritetime': 'LastWriteTime', 'name': 'Name'},
                    {'lastwritetime': '9/1/2021 6:13:50 AM', 'name': 'reference'},
                    {'lastwritetime': '10/5/2021 9:13:50 PM', 'name': 'dsc'},
                    {'lastwritetime': '11/2/2021 11:58:45 PM', 'name': 'README.md'},
                    {'lastwritetime': '12/16/2021 12:30:59 PM', 'name': 'CONTRIBUTING.md'}
                ],
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                3,
                r'(?P<fruits>[a-zA-Z]+) (?P<meat>( {10,16})|( *[a-zA-Z]+ *)) (?P<drinks>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*){,1})',  # noqa
                [
                    {'fruits': 'fruits', 'meat': 'meat', 'drinks': 'drinks'},
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'}
                ],
            ),
        ]
    )
    def test_to_regex(
        self, text, columns_count, expected_pattern, expected_results
    ):
        node = TabularTextPatternByVarColumns(text, columns_count=columns_count, divider='  ')
        pattern = node.to_regex()
        assert pattern == expected_pattern
        for index, line in enumerate(Misc.get_list_of_lines(text)):
            expected_result = expected_results[index]
            match = re.match(pattern, line)
            if match:
                lst_of_dict = MiscObject.cleanup_list_of_dict([match.groupdict()])
                result = lst_of_dict.pop()
                assert result == expected_result
            else:
                assert False, 'Failed to match this line: %r' % line

    @pytest.mark.parametrize(
        "text,divider,columns_count,headers_data,expected_template_snippet,expected_template,expected_result",
        [
            (
                dedent("""
                    LastWriteTime          Name
                    9/1/2021 6:13:50 AM    reference
                    10/5/2021 9:13:50 PM   dsc
                    11/2/2021 11:58:45 PM  README.md
                    12/16/2021 12:30:59 PM CONTRIBUTING.md
                """).strip(),
                '  ',
                2,
                'LastWriteTime          Name',
                dedent("""
                    LastWriteTime          Name
                    start() mixed_phrase(var_lastwritetime, at_most_2_group_occurrences)  mixed_word(var_name) end() -> record
                """).strip(),   # noqa
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value lastwritetime ([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)+( +[\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)+){,2})
                    Value name ([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)
                    
                    Start
                      ^LastWriteTime +Name
                      ^${lastwritetime} +${name}$$ -> Record
                """).strip(),
                [
                    {'lastwritetime': '9/1/2021 6:13:50 AM', 'name': 'reference'},
                    {'lastwritetime': '10/5/2021 9:13:50 PM', 'name': 'dsc'},
                    {'lastwritetime': '11/2/2021 11:58:45 PM', 'name': 'README.md'},
                    {'lastwritetime': '12/16/2021 12:30:59 PM', 'name': 'CONTRIBUTING.md'}
                ],
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    orange    pork      water
                    peach               pepsi soda
                """).strip(),
                '  ',
                3,
                '0',
                dedent("""
                    fruits    meat      drinks
                    start() letters(var_fruits) letters(var_meat, or_either_repeating_10_16_spaces) word(var_drinks, at_most_1_group_occurrences) end() -> record
                """).strip(),   # noqa
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits ([a-zA-Z]+)
                    Value meat (( {10,16})|( *[a-zA-Z]+ *))
                    Value drinks ([a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*){,1})

                    Start
                      ^fruits +meat +drinks
                      ^${fruits} ${meat} ${drinks}$$ -> Record
                """).strip(),
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'}
                ]
            ),
            (
                dedent("""
                    fruits    meat      drinks
                    ------    --------  -------
                    orange    pork      water
                    peach               pepsi soda
                    mango     chicken
                """).strip(),
                '',
                3,
                '',
                dedent("""
                    fruits    meat      drinks
                    start() letters(var_fruits) letters(var_meat, or_either_repeating_7_16_spaces) word(var_drinks, at_most_1_group_occurrences, or_either_repeating_5_10_spaces) end() -> record
                    start() letters(var_fruits) letters(var_meat, or_either_repeating_7_16_spaces) end() -> record
                    start() letters(var_fruits) end() -> record
                """).strip(),   # noqa
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits ([a-zA-Z]+)
                    Value meat (( {7,16})|( *[a-zA-Z]+ *))
                    Value drinks (( {5,10})|( *[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*){,1} *))

                    Start
                      ^fruits +meat +drinks
                      ^${fruits} ${meat} ${drinks}$$ -> Record
                      ^${fruits} ${meat}$$ -> Record
                      ^${fruits}$$ -> Record
                """).strip(),
                [
                    {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'},
                    {'fruits': 'peach', 'meat': '', 'drinks': 'pepsi soda'},
                    {'fruits': 'mango', 'meat': 'chicken', 'drinks': ''}
                ]
            ),
        ]
    )
    def test_to_template_snippet(
        self, text, divider, columns_count, headers_data,
        expected_template_snippet, expected_template,
        expected_result
    ):
        node = TabularTextPatternByVarColumns(
            text, divider=divider, columns_count=columns_count, headers_data=headers_data
        )
        tmpl_snippet = node.to_template_snippet()
        assert tmpl_snippet == expected_template_snippet

        template = get_textfsm_template(tmpl_snippet)
        template = re.sub(r'date: \d{4}-\d\d-\d\d', 'date: YYYY-mm-dd', template)
        assert template == expected_template

        test_data = text
        is_verified = verify(tmpl_snippet, test_data,
                             expected_result=expected_result)
        assert is_verified
