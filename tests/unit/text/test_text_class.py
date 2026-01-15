"""
Unit tests for the `genericlib.text.Text` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/text/test_text_class.py
    or
    $ python -m pytest tests/unit/text/test_text_class.py
"""

import pytest

from genericlib import Text
from genericlib import DotObject

from tests.unit import FooException


class TestText:
    """
    Unit tests for the Text class.
    """

    def test_initialize_empty_and_string(self):
        """
        Verify that Text initializes correctly with no arguments or a simple string.
        """
        node = Text()
        assert node == ''

        node = Text('abc')
        assert node == 'abc'

    def test_initialize_with_exception(self):
        """
        Verify that initializing Text with an exception produces a formatted string.
        """
        exc = FooException("Sample error raised from FooException")
        node = Text(exc)
        assert node == "FooException: Sample error raised from FooException"

    def test_format_with_positional_placeholders(self):
        """
        Verify that Text.format handles positional formatting.

        - Supports old-style `%s` formatting.
        - Supports new-style `{}` formatting.
        """
        node = Text.format('%s %s', 'Jack', 'Brown')
        assert node == 'Jack Brown'

        node = Text.format('{} {}', 'Jack', 'Brown')
        assert node == 'Jack Brown'

    def test_format_with_named_placeholders(self):
        """
        Verify that Text.format handles named placeholders.

        - Supports old-style `%(name)s` formatting with dictionaries.
        - Supports new-style `{name}` formatting with keyword arguments.
        """
        fmt = '%(first_name)s %(last_name)s'
        data = dict(first_name='Jack', last_name='Brown')
        node = Text.format(fmt, data)   # noqa
        assert node == 'Jack Brown'

        fmt = '{first_name} {last_name}'
        node = Text.format(fmt, first_name='Jack', last_name='Brown')
        assert node == 'Jack Brown'

    def test_format_with_nested_objects_and_dicts(self):
        """
        Verify that Text.format supports nested object and dictionary access.

        - Supports attribute access via dot notation.
        - Supports keyword argument mapping to objects.
        - Supports dictionary-style key access within placeholders.
        """
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
            (
                'div', 'Hello GenericLib',
                ['class="container"'],
                '<div class="container">Hello GenericLib</div>'
            ),
            (
                'div', 'Hello GenericLib',
                ['class="container"', 'width="100%"'],
                '<div class="container" width="100%">Hello GenericLib</div>'
            ),
            (
                'div', 'Hello GenericLib',
                ['class="container"', ' ', 'width="100%"'],
                '<div class="container" width="100%">Hello GenericLib</div>'
            ),
        ]
    )
    def test_wrap_html_generates_expected_output(self, tag, data, attributes, expected_result):
        """
        Verify that Text.wrap_html generates correct HTML tags.
        """
        result = Text.wrap_html(tag, data, *attributes)
        assert result == expected_result
