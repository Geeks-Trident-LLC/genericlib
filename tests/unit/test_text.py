import pytest   # noqa

from genericlib import Text
from genericlib import DotObject

from genericlib.text import BaseMatchedObject


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
        node = Text.format('%s %s', 'Jack', 'Brown')
        assert node == 'Jack Brown'

        node = Text.format('{} {}', 'Jack', 'Brown')
        assert node == 'Jack Brown'

    def test_format_case2(self):
        fmt = '%(first_name)s %(last_name)s'
        data = dict(first_name='Jack', last_name='Brown')
        node = Text.format(fmt, data)
        assert node == 'Jack Brown'

        fmt = '{first_name} {last_name}'
        node = Text.format(fmt, first_name='Jack', last_name='Brown')
        assert node == 'Jack Brown'

    def test_format_case3(self):

        data = DotObject(
            person1=dict(first_name='Jack', last_name='Brown'),
            person2=dict(first_name='Linda', last_name='Wilson')
        )

        fmt1 = '{0.person1.first_name} {0.person1.last_name}, {0.person2.first_name} {0.person2.last_name}'
        node = Text.format(fmt1, data)
        assert node == 'Jack Brown, Linda Wilson'

        fmt2 = '{p1.first_name} {p1.last_name}, {p2.first_name} {p2.last_name}'
        node = Text.format(fmt2, p1=data.person1, p2=data.person2)
        assert node == 'Jack Brown, Linda Wilson'

        fmt3 = '{p2[first_name]} {p2[last_name]}, {p1[first_name]} {p1[last_name]}'
        node = Text.format(fmt3, p1=data.person1, p2=data.person2)
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
