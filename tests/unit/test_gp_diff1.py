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

    @pytest.mark.parametrize(
        "lines,expected_snippet",
        [
            (
                (
                    'ipv6_addr: a::b % 16',
                    'ipv6_addr: a::c % 32',
                 ),
                'start() ipv6_addr: mixed_word(var_v0) % digits(var_v1) end()'
            ),
            (
                (
                    'ipv6_addr: 1::2 % 32',
                    'ipv6_addr: 1::3 / 33',
                ),
                'start() ipv6_addr: non_whitespaces_phrase(var_v0) end()'
            ),
        ]
    )
    def test_generated_snippet1(self, lines, expected_snippet):
        node = DiffLinePattern(*lines)
        snippet = node.snippet
        assert snippet == expected_snippet

    @pytest.mark.parametrize(
        "lines,expected_snippet",
        [
            (
                (
                    'this is yellow half \t pencil',
                    'this is red half pencil',
                    'this is green half pencil',
                    'this is half pencil',
                 ),
                'start() this is letters(var_v0, or_empty) half\t pencil end()'
            ),
        ]
    )
    def test_generated_snippet2(self, lines, expected_snippet):
        node = DiffLinePattern(*lines)
        snippet = node.snippet
        assert snippet == expected_snippet
