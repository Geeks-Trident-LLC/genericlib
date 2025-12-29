import pytest   # noqa

from genericlib import Text
from genericlib import DotObject

from genericlib.text import BaseMatchedObject
from genericlib.text import dedent_and_strip

from genericlib.text import decorate_list_of_line


class FooException(Exception):
    """Foo Exception"""


class TestText:
    """Test class for Text."""

    def test_text_initialization1(self):
        node = Text()
        assert node == ''

        node = Text('abc')
        assert node == 'abc'

    def test_text_initialization(self):
        exc = FooException('exception from foo instance')
        node = Text(exc)
        assert node == 'FooException: exception from foo instance'

    def test_format_case1(self):
        node = Text.format('%s %s', 'Jack', 'Brown')    # noqa
        assert node == 'Jack Brown'

        node = Text.format('{} {}', 'Jack', 'Brown')    # noqa
        assert node == 'Jack Brown'

    def test_format_case2(self):
        fmt = '%(first_name)s %(last_name)s'
        data = dict(first_name='Jack', last_name='Brown')
        node = Text.format(fmt, data)   # noqa
        assert node == 'Jack Brown'

        fmt = '{first_name} {last_name}'
        node = Text.format(fmt, first_name='Jack', last_name='Brown')   # noqa
        assert node == 'Jack Brown'

    def test_format_case3(self):

        data = DotObject(
            person1=dict(first_name='Jack', last_name='Brown'),
            person2=dict(first_name='Linda', last_name='Wilson')
        )

        fmt1 = '{0.person1.first_name} {0.person1.last_name}, {0.person2.first_name} {0.person2.last_name}'
        node = Text.format(fmt1, data)      # noqa
        assert node == 'Jack Brown, Linda Wilson'

        fmt2 = '{p1.first_name} {p1.last_name}, {p2.first_name} {p2.last_name}'
        node = Text.format(fmt2, p1=data.person1, p2=data.person2)  # noqa
        assert node == 'Jack Brown, Linda Wilson'

        fmt3 = '{p2[first_name]} {p2[last_name]}, {p1[first_name]} {p1[last_name]}'
        node = Text.format(fmt3, p1=data.person1, p2=data.person2)  # noqa
        assert node == 'Linda Wilson, Jack Brown'

    @pytest.mark.parametrize(
        "tag,data,attributes,expected_result",
        [
            ('div', '', [], '<div/>'),
            ('div', 'Hello GenericLib', [], '<div>Hello GenericLib</div>'),
            ('div', 'Hello GenericLib', ['class="container"'],
             '<div class="container">Hello GenericLib</div>'),
            ('div', 'Hello GenericLib',
             ['class="container"', 'width="100%"'],
             '<div class="container" width="100%">Hello GenericLib</div>'),
            ('div', 'Hello GenericLib',
             ['class="container"', ' ', 'width="100%"'],
             '<div class="container" width="100%">Hello GenericLib</div>'),

        ]
    )
    def test_wrap_html(self, tag, data, attributes, expected_result):
        result = Text.wrap_html(tag, data, *attributes)
        assert result == expected_result


class TestBaseMatchedObject:
    @pytest.mark.parametrize(
        'data,expected_result',
        [
            (' ', ' '),
            ('  ', ' +'),
            (' \t ', r'\s+'),
            ('abc xyz', 'abc xyz'),
            ('+++', r'\+{2,}'),
            ('+------------+', r'\+-{2,}\+'),
            ('+-----_-_-_-_-_-+', r'\+-{2,}(_-){2,}\+'),
            ('. . . . . . . . ', r'(\. ){2,}'),
        ]
    )
    def test_wrap_html(self, data, expected_result):
        node = BaseMatchedObject(data)
        result = node.to_pattern()
        assert result == expected_result


class TestDedentAndStripFunction:
    """
    Unit tests for the `dedent_and_strip` utility function.

    This test suite verifies that text normalization works correctly by
    converting input to string, removing common leading indentation, and
    stripping leading/trailing whitespace. It ensures consistent behavior
    across single-line, multi-line, and mixed-indentation inputs.
    """
    def test_dedent_and_strip_removes_indentation_and_whitespace(self):
        txt = "    line1\n    line2\n"
        result = dedent_and_strip(txt)
        assert result == "line1\nline2"

    def test_dedent_and_strip_trims_leading_and_trailing_spaces(self):
        txt = "   hello world   "
        result = dedent_and_strip(txt)
        assert result == "hello world"

    def test_dedent_and_strip_handles_multiline_with_mixed_indent(self):
        txt = """
            line1
              line2
            line3
        """
        result = dedent_and_strip(txt)
        # dedent removes common leading whitespace, strip removes outer blank lines
        assert result == "line1\n  line2\nline3"


class TestDecorateListOfLineFunction:
    """
    Unit tests for the `decorate_list_of_line` function.

    This test suite validates that framed text messages are generated
    correctly from lists of strings. It ensures proper alignment,
    border construction, and whitespace handling across a variety
    of input scenarios.
    """
    def test_single_line(self):
        expected = dedent_and_strip("""
            +--------------+
            | Hello Python |
            +--------------+
        """)
        lst_of_line = ["Hello Python"]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected

    def test_multiple_lines(self):
        expected = dedent_and_strip("""
            +------------------+
            | Short            |
            | Much longer line |
            | Mid              |
            +------------------+
        """)
        lst_of_line = ["Short", "Much longer line", "Mid"]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected

    def test_empty_string_line(self):
        expected = dedent_and_strip("""
            +-----+
            |     |
            | abc |
            +-----+
        """)
        lst_of_line = ["", "abc"]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected

    def test_all_empty_lines(self):
        expected = dedent_and_strip("""
            +--+
            |  |
            |  |
            +--+
        """)
        lst_of_line = ["", ""]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected

    def test_preserves_whitespace(self):
        expected = dedent_and_strip("""
            +----+
            | a  |
            | b  |
            +----+
        """)
        lst_of_line = ["a ", "b"]
        result = decorate_list_of_line(lst_of_line)
        assert result == expected
