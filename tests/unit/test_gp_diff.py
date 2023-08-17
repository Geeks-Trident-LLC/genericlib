import re

import pytest           # noqa
from textwrap import dedent

from genericlib.gp import verify
from genericlib.gp import get_textfsm_template

from genericlib.gp import DiffLinePattern
from genericlib.gp import CategoryLinePattern


class TestDiffLinePattern:
    """Test class for DiffLinePattern"""
    @pytest.mark.parametrize(
        "lines,expected_total_lines_count",
        [
            (['line 1', 'line 2'], 2),
            (['line 1', 'line 2', 'line 3'], 3),
            (['line 1', '', 'line 3', 'line4'], 3),
            (['line 1', '', '      ', 'line4'], 2),
        ]
    )
    def test_prepare(self, lines, expected_total_lines_count):
        node = DiffLinePattern('a', 'b')
        node.reset()
        node.prepare(*lines)
        total_lines_count = len(node.lines)
        assert total_lines_count == expected_total_lines_count

    @pytest.mark.parametrize(
        "lines",
        [
            ('line 1', ''),
            (' ', 'line2'),
            (' ', '    '),
            ('', ''),
        ]
    )
    def test_prepare_catch_exception(self, lines):
        node = DiffLinePattern('a', 'b')

        with pytest.raises(Exception):
            node.prepare(*lines)

    @pytest.mark.parametrize(
        "line_a,line_b,expected_pattern",
        [
            ('a', '@', r'(?P<v0>[\x21-\x7e])'),
            ('a b', '@', '(?P<v0>\\S+( +\\S+)*)'),
            ('a b', 'x','(?P<v0>[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)*)'),
            (
                'line one is a first line',
                'line ore is a second line',
                'line +(?P<v0>[a-zA-Z]+) +is +a +(?P<v1>[a-zA-Z]+) +line'
            ),
            (
                '  line one is a first line',
                'line ore is a second line',
                ' *line +(?P<v0>[a-zA-Z]+) +is +a +(?P<v1>[a-zA-Z]+) +line'
            ),
            (
                '  line one is a first line',
                '    line ore is a second line',
                ' +line +(?P<v0>[a-zA-Z]+) +is +a +(?P<v1>[a-zA-Z]+) +line'
            ),
            (
                '  line one is a first line  ',
                '    line ore is a second line',
                ' +line +(?P<v0>[a-zA-Z]+) +is +a +(?P<v1>[a-zA-Z]+) +line *'
            ),
            (
                'this line one is a first line',
                'line ore is a second bad line',
                '(?P<v0>[a-zA-Z]+)?( +)?line +(?P<v1>[a-zA-Z]+) +is +a +(?P<v2>[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)*) +line'    # noqa
            ),
        ]
    )
    def test_get_pattern_btw_two_lines(self, line_a, line_b, expected_pattern):
        node = DiffLinePattern('a', 'b')
        node.reset()
        pattern = node.get_pattern_btw_two_lines(line_a, line_b)
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "lines,expected_pattern",
        [
            (
                (
                    'this is a pen',
                    'this is the yellow pen',
                 ),
                'this +is +(?P<v0>[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)*) +pen'
            ),
            (
                (
                    'this is a pen',
                    'this is the yellow pen',
                    'this is the good yellow pen',
                ),
                'this +is +(?P<v0>[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)*) +pen'
            ),
            (
                (
                    'this is a pen',
                    'this is the yellow pen',
                    'this is the good yellow pen',
                    'that is a pencil'
                ),
                '(?P<v0>[a-zA-Z]+) +is +(?P<v1>[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)+)'
            ),
            (
                (
                    'this is a pen',
                    '  this is the yellow pen',
                    'this is the good yellow pen',
                    'that is a pencil'
                ),
                ' *(?P<v0>[a-zA-Z]+) +is +(?P<v1>[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)+)'
            ),
            (
                (
                    'this is a pen',
                    'this is the yellow pen',
                    'this is the good yellow pen  ',
                    ' that is a pencil'
                ),
                ' *(?P<v0>[a-zA-Z]+) +is +(?P<v1>[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)+) *'
            ),
            (
                (
                    '  this is a pen',
                    '    this is the yellow pen',
                    '  this is the good yellow pen ',
                    '    that is a pencil'
                ),
                ' +(?P<v0>[a-zA-Z]+) +is +(?P<v1>[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)+) *'
            ),
            (
                (
                    '  this is a pen               ',
                    '    this is the yellow pen    ',
                    '  this is the good yellow pen ',
                    '    that is a pencil          '
                ),
                ' +(?P<v0>[a-zA-Z]+) +is +(?P<v1>[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)+) +'
            ),
        ]
    )
    def test_generated_pattern(self, lines, expected_pattern):
        node = DiffLinePattern(*lines)
        pattern = node.pattern
        assert pattern == expected_pattern


class TestCategoryLinePattern:
    """Test class for CategoryLinePattern"""
    @pytest.mark.parametrize(
        "line,count,expected_pattern,expected_result",
        [
            (
                'fruits: orange, peach',
                1,
                'fruits: *(?P<fruits>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)+)',  # noqa
                {'fruits': 'orange, peach'}
            ),
            (
                'total   fruits: orange, peach',
                1,
                'total +fruits: *(?P<total_fruits>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)+)',     # noqa
                {'total_fruits': 'orange, peach'}
            ),
            (
                'total fruit(s): orange, peach',
                1,
                'total fruit\\(s\\): *(?P<total_fruit_s>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)+)',   # noqa
                {'total_fruit_s': 'orange, peach'}
            ),
            (
                'fruits: orange   meat: pork  drinks: water',
                3,
                r'fruits: *(?P<fruits>[a-zA-Z]+) +meat: *(?P<meat>[a-zA-Z]+) +drinks: *(?P<drinks>[a-zA-Z]+)',
                {'fruits': 'orange', 'meat': 'pork', 'drinks': 'water'}
            ),
            (
                'fruits:   meat: ',
                2,
                r'fruits: *(?P<fruits>.*|) +meat: *(?P<meat>.*|)',
                {'fruits': '', 'meat': ''}
            ),
            (
                'fruits:   meat:  drinks: ',
                3,
                r'fruits: *(?P<fruits>.*|) +meat: *(?P<meat>.*|) +drinks: *(?P<drinks>.*|)',
                {'fruits': '', 'meat': '', 'drinks': ''}
            ),
            (
                'fruits:   meat: pork  drinks: ',
                3,
                r'fruits: *(?P<fruits>.*|) +meat: *(?P<meat>[a-zA-Z]+) +drinks: *(?P<drinks>.*|)',
                {'fruits': '', 'meat': 'pork', 'drinks': ''}
            ),
            (
                'fruits:   meat: pork  drinks: water',
                3,
                r'fruits: *(?P<fruits>.*|) +meat: *(?P<meat>[a-zA-Z]+) +drinks: *(?P<drinks>[a-zA-Z]+)',
                {'fruits': '', 'meat': 'pork', 'drinks': 'water'}
            ),
            (
                'fruits: orange, peach  meat:   drinks: water',
                3,
                'fruits: *(?P<fruits>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)+) +meat: *(?P<meat>.*|) +drinks: *(?P<drinks>[a-zA-Z]+)',    # noqa
                {'fruits': 'orange, peach', 'meat': '', 'drinks': 'water'}
            ),
            (
                'time: 08:30:00 P.M.',
                1,
                'time: *(?P<time>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)+)',
                {'time': '08:30:00 P.M.'}
            ),
            (
                'time: 08:30:00 P.M.  mac_addr: 11:22:33:44:55:66',
                2,
                'time: *(?P<time>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)+) +mac_addr: *(?P<mac_addr>[+\\(\\[\\$-]?(\\d+([,:/-]\\d+)*)?[.]?\\d+[\\]\\)%a-zA-Z]*)',     # noqa
                {'time': '08:30:00 P.M.', 'mac_addr': '11:22:33:44:55:66'}
            ),
            (
                'time: 08:30:00 P.M.   ipv6: ::1234, 2000::ab, 2000::   mac_addr: 11:22:33:44:55:66',
                3,
                'time: *(?P<time>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)+) +ipv6: *(?P<ipv6>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)+) +mac_addr: *(?P<mac_addr>[+\\(\\[\\$-]?(\\d+([,:/-]\\d+)*)?[.]?\\d+[\\]\\)%a-zA-Z]*)',   # noqa
                {'time': '08:30:00 P.M.', 'ipv6': '::1234, 2000::ab, 2000::', 'mac_addr': '11:22:33:44:55:66'}
            ),
        ]
    )
    def test_to_regex(self, line, count, expected_pattern, expected_result, ):
        node = CategoryLinePattern(line, count=count)
        pattern = node.to_regex()
        assert pattern == expected_pattern
        match = re.match(pattern, line)
        if match:
            result = match.groupdict()
            assert result == expected_result
        else:
            assert False, 'No Match - Pattern is %r' % pattern

    @pytest.mark.parametrize(
        "line,count,expected_template_snippet,expected_template,expected_result",
        [
            (
                'fruits:  orange, peach',
                1,
                r'fruits:  mixed_phrase(var_fruits)',
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits ([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)+)

                    Start
                      ^fruits: +${fruits}
                """).strip(),
                [{'fruits': 'orange, peach'}]
            ),
            (
                'total fruit(s): orange, peach',
                1,
                r'total fruit(s): mixed_phrase(var_total_fruit_s)',
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value total_fruit_s ([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)+)

                    Start
                      ^total fruit\(s\): ${total_fruit_s}
                """).strip(),
                [{'total_fruit_s': 'orange, peach'}]
            ),
            (
                '  fruit(s): orange   meat: pork  drinks: water',
                3,
                r'  fruit(s): letters(var_fruit_s)  meat: letters(var_meat)  drinks: letters(var_drinks)',
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruit_s ([a-zA-Z]+)
                    Value meat ([a-zA-Z]+)
                    Value drinks ([a-zA-Z]+)

                    Start
                      ^ +fruit\(s\): ${fruit_s} +meat: ${meat} +drinks: ${drinks}
                """).strip(),
                [{'fruit_s': 'orange', 'meat': 'pork', 'drinks': 'water'}]
            ),
            (
                'fruits:   meat: ',
                2,
                r'fruits:zospaces()something(var_fruits, or_empty)  meat:zospaces()something(var_meat, or_empty)',
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits ((.*|))
                    Value meat ((.*|))

                    Start
                      ^fruits: *${fruits} +meat: *${meat}
                """).strip(),
                [{'fruits': '', 'meat': ''}]
            ),
            (
                'fruits: orange   meat:  drinks: water',
                3,
                r'fruits: letters(var_fruits)  meat:zospaces()something(var_meat, or_empty)  drinks: letters(var_drinks)',
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits ([a-zA-Z]+)
                    Value meat ((.*|))
                    Value drinks ([a-zA-Z]+)

                    Start
                      ^fruits: ${fruits} +meat: *${meat} +drinks: ${drinks}
                """).strip(),
                [{'fruits': 'orange', 'meat': '', 'drinks': 'water'}]
            ),
            (
                'fruits:   meat:  drinks: water',
                3,
                r'fruits:zospaces()something(var_fruits, or_empty)  meat:zospaces()something(var_meat, or_empty)  drinks: letters(var_drinks)',
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value fruits ((.*|))
                    Value meat ((.*|))
                    Value drinks ([a-zA-Z]+)

                    Start
                      ^fruits: *${fruits} +meat: *${meat} +drinks: ${drinks}
                """).strip(),
                [{'fruits': '', 'meat': '', 'drinks': 'water'}]
            ),
            (
                'time: 08:30:00 P.M.',
                1,
                r'time: mixed_phrase(var_time)',
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value time ([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)+)

                    Start
                      ^time: ${time}
                """).strip(),
                [{'time': '08:30:00 P.M.'}]
            ),
            (
                'time: 08:30:00 P.M.   mac_addr: 11:22:33:44:55:66',
                2,
                r'time: mixed_phrase(var_time)  mac_addr: mixed_number(var_mac_addr)',
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value time ([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)+)
                    Value mac_addr ([+\(\[\$-]?(\d+([,:/-]\d+)*)?[.]?\d+[\]\)%a-zA-Z]*)

                    Start
                      ^time: ${time} +mac_addr: ${mac_addr}
                """).strip(),
                [{'time': '08:30:00 P.M.', 'mac_addr': '11:22:33:44:55:66'}]
            ),
            (
                'time: 08:30:00 P.M.   ipv6: ::1234, 2000::ab, 2000::   mac_addr: 11:22:33:44:55:66',
                3,
                r'time: mixed_phrase(var_time)  ipv6: mixed_phrase(var_ipv6)  mac_addr: mixed_number(var_mac_addr)',
                dedent(r"""
                    ################################################################################
                    # Template is generated by template Pro Edition
                    # Created date: YYYY-mm-dd
                    ################################################################################
                    Value time ([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)+)
                    Value ipv6 ([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)+)
                    Value mac_addr ([+\(\[\$-]?(\d+([,:/-]\d+)*)?[.]?\d+[\]\)%a-zA-Z]*)
                    
                    Start
                      ^time: ${time} +ipv6: ${ipv6} +mac_addr: ${mac_addr}
                """).strip(),
                [{'time': '08:30:00 P.M.', 'ipv6': '::1234, 2000::ab, 2000::', 'mac_addr': '11:22:33:44:55:66'}]
            ),
        ]
    )
    def test_to_template_snippet(self, line, count, expected_template_snippet,
                                 expected_template, expected_result, ):
        node = CategoryLinePattern(line, count=count)
        tmpl_snippet = node.to_template_snippet()
        assert tmpl_snippet == expected_template_snippet

        template = get_textfsm_template(tmpl_snippet)
        template = re.sub(r'\d{4}-\d\d-\d\d', 'YYYY-mm-dd', template)
        assert template == expected_template

        test_data = line
        is_verified = verify(tmpl_snippet, test_data,
                             expected_result=expected_result)
        assert is_verified

