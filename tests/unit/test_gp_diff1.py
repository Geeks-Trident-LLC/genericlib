import pytest           # noqa

from genericlib.gpdiff import DiffLinePattern


class TestDiffLinePattern:
    """Test class for DiffLinePattern"""
    @pytest.mark.parametrize(
        "lines,expected_pattern",
        [
            (
                (
                    'this \t is a pen',
                    'this is the yellow pen',
                 ),
                'this\\s+is (?P<v0>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*) pen'
            ),
        ]
    )
    def test_generated_pattern(self, lines, expected_pattern):
        node = DiffLinePattern(*lines)
        pattern = node.pattern
        assert pattern == expected_pattern

    @pytest.mark.parametrize(
        "lines,expected_snippet",
        [
            (
                (
                    'this \t is a pen',
                    'this is the yellow pen',
                 ),
                'start() this\t is words(var_v0) pen end()'
            ),
        ]
    )
    def test_generated_snippet(self, lines, expected_snippet):
        node = DiffLinePattern(*lines)
        snippet = node.snippet
        assert snippet == expected_snippet
