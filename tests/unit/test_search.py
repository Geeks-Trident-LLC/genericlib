import pytest
from genericlib import Wildcard


class FooException(Exception):
    """Foo Exception"""


class TestWildcard:
    """Test class for Wildcard."""

    @pytest.mark.parametrize(
        "data,is_prefix,is_postfix,ignore_case,expected_result",
        [
            ('', False, False, False, '^$'),
            ('', True, False, False, '^$'),
            ('', True, True, False, '^$'),
            ('', True, True, True, '(?i)^$'),
            (' ', False, False, False, '^ +$'),
            ('    ', False, False, False, '^ +$'),
            ('    ', True, False, False, '^ +$'),
            ('    ', True, True, False, '^ +$'),
            ('    ', True, True, True, '(?i)^ +$'),
            ('Johnson', False, False, False, '^Johnson$'),
            ('  Johnson', False, False, False, '^ *Johnson$'),
            ('Johnson', True, False, False, '^ *Johnson$'),
            ('  Johnson', True, False, False, '^ *Johnson$'),
            ('  Johnson  ', True, False, False, '^ *Johnson *$'),
            ('  Johnson', True, True, False, '^ *Johnson *$'),
            ('  Johnson  ', True, True, False, '^ *Johnson *$'),
            ('  Johnson  ', True, True, True, '(?i)^ *Johnson *$'),
            ('John*', True, True, True, '(?i)^ *John.* *$'),
            ('*ohn*', False, False, True, '(?i)^.*ohn.*$'),
            ('*ohn*\n*illi*\n*ynd*', False, False, True, r'(?i)^.*ohn.*[\r\n]+.*illi.*[\r\n]+.*ynd.*$'),
            ('[Jj]ohn*', False, False, True, '(?i)^[Jj]ohn.*$'),
            ('[Ww]ild[Cc]ar*', False, False, True, '(?i)^[Ww]ild[Cc]ar.*$'),
            ('*[Ww]ild[Cc]ar*', False, False, True, '(?i)^.*[Ww]ild[Cc]ar.*$'),

        ]
    )
    def test_wrap_html(self, data, is_prefix, is_postfix, ignore_case, expected_result):
        node = Wildcard(data, is_prefix=is_prefix, is_postfix=is_postfix,
                        ignore_case=ignore_case)
        pattern = node.pattern
        assert pattern == expected_result
