# import re

import pytest
from genericlib.gp import CommonPhrase


class TestCommonPhrase:
    """Test class for CommonPhrase."""

    @pytest.mark.parametrize(
        "data,is_generic,is_flex_space,expected_result",
        [
            ('', False, False, ''),
            (' ', False, False, ' '),
            ('   ', False, False, '   '),
            ('   ', False, True, ' +'),
            ('abc xyz', False, False, 'abc xyz'),
            ('abc   xyz', False, False, 'abc   xyz'),
            ('abc   xyz', False, True, 'abc +xyz'),
            ('  abc   xyz', False, True, ' +abc +xyz'),
            ('  abc   xyz  ', False, True, ' +abc +xyz +'),
            ('  (abc)   xyz  ', False, True, ' +\\(abc\\) +xyz +'),
            ('  (abc+)   xyz  ', False, True, ' +\\(abc\\+\\) +xyz +'),
            ('  (abc++)   x.yz  ', False, True, ' +\\(abc\\+\\+\\) +x\\.yz +'),
        ]
    )
    def test_common_phrase(self, data, is_generic, is_flex_space, expected_result):
        node = CommonPhrase(data, is_generic=is_generic, is_flex_space=is_flex_space)
        pattern = node.pattern
        assert pattern == expected_result
