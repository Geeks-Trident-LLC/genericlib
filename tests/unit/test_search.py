import re

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
    def test_wildcard(self, data, is_prefix, is_postfix, ignore_case, expected_result):
        node = Wildcard(data, is_prefix=is_prefix, is_postfix=is_postfix,
                        ignore_case=ignore_case)
        pattern = node.pattern
        assert pattern == expected_result

    @pytest.mark.parametrize(
        "data,expected_result",
        [
            ('--regex', ''),
            ('--regex ', ''),
            ('--regex  ', ' *'),
            ('--regex Hello GenericLib', 'Hello GenericLib'),
            ('--regex  Hello GenericLib', ' *Hello GenericLib'),
            ('--regex Hello [Gg]eneric[Ll]ib', 'Hello [Gg]eneric[Ll]ib'),
            ('--regex (?i)Hello [Gg]eneric[Ll]ib', '(?i)Hello [Gg]eneric[Ll]ib'),
            ('(?i)--regex Hello [Gg]eneric[Ll]ib', '(?i)Hello [Gg]eneric[Ll]ib'),
            ('(?i)--regex  Hello [Gg]eneric[Ll]ib', '(?i) *Hello [Gg]eneric[Ll]ib'),
            ('(?i) --regex Hello [Gg]eneric[Ll]ib', '(?i) *Hello [Gg]eneric[Ll]ib'),
            ('(?i)Hello --regex [Gg]eneric[Ll]ib', '(?i)Hello *[Gg]eneric[Ll]ib'),
            ('(?i)Hello --regex  [Gg]eneric[Ll]ib', '(?i)Hello *[Gg]eneric[Ll]ib'),
            ('(?i)Hello [Gg]eneric[Ll]ib --regex', '(?i)Hello [Gg]eneric[Ll]ib'),
            ('(?i)Hello [Gg]eneric[Ll]ib  --regex', '(?i)Hello [Gg]eneric[Ll]ib *'),
            ('(?i)Hello [Gg]eneric[Ll]ib  --regex $', '(?i)Hello [Gg]eneric[Ll]ib *$'),
        ]
    )
    def test_wildcard_for_regex_flag_case(self, data, expected_result):
        node = Wildcard(data)
        pattern = node.pattern
        assert pattern == expected_result

    @pytest.mark.parametrize(
        "data,expected_pattern,matched_results",
        [
            (
                'file[[:digit:]]',
                '^file[0-9]$',
                [
                    'file0', 'file1', 'file3', 'file4', 'file5',
                    'file6', 'file7', 'file7', 'file8', 'file9'
                ]
            ),
            (
                'file[[:alpha:]]',
                '^file[a-zA-Z]$',
                ['filea', 'fileb', 'filec', 'fileE']
            ),
            (
                'file[[:alnum:]]',
                '^file[a-zA-Z0-9]$',
                [
                    'file0', 'file1', 'file3', 'file4', 'file5',
                    'file6', 'file7', 'file7', 'file8', 'file9',
                    'filea', 'fileb', 'filec', 'fileE'
                ]
            ),
            (
                'file[a-c[:digit:]]',
                '^file[a-c0-9]$',
                [
                    'file0', 'file1', 'file3', 'file4', 'file5',
                    'file6', 'file7', 'file7', 'file8', 'file9',
                    'filea', 'fileb', 'filec'
                ]
            ),
            (
                'file[2-5[:alpha:]]',
                '^file[2-5a-zA-Z]$',
                [
                    'file2', 'file3', 'file4', 'file5',
                    'filea', 'fileb', 'filec'
                ]
            ),
            (
                'file[^2-5[:alpha:]]',
                '^file[^2-5a-zA-Z]$',
                [
                    'file0', 'file1', 'file6', 'file7',
                    'file_', 'file+', 'file-'
                ]
            ),
            (
                'file[^a-c[:digit:]]',
                '^file[^a-c0-9]$',
                [
                    'filed', 'filee', 'filef', 'fileg',
                    'file_', 'file+', 'file-'
                ]
            ),
            (
                '*file[^a-c[:digit:]]*',
                '^.*file[^a-c0-9].*$',
                [
                    'filed', 'filee', 'filef', 'fileg',
                    'file_', 'file+', 'file-'
                ]
            ),
            (
                '*file[^a-c[:digit:]]*',
                '^.*file[^a-c0-9].*$',
                [
                    'abc_filed_xyz', '123_filee_+++',
                    'filed', 'filee', 'filef', 'fileg',
                    'file_', 'file+', 'file-'
                ]
            ),
        ]
    )
    def test_wildcard_for_posix_case(self, data, expected_pattern, matched_results):
        node = Wildcard(data, is_prefix=False, is_postfix=False, ignore_case=False)
        pattern = node.pattern
        assert pattern == expected_pattern
        for matched_result in matched_results:
            matched = re.match(pattern, matched_result)
            assert bool(matched)

    @pytest.mark.parametrize(
        "data,expected_pattern,matched_results,not_matched_results",
        [
            (
                'file.{txt,xml,yaml}',
                '^file\\.(txt|xml|yaml)$',
                ['file.txt', 'file.xml', 'file.yaml'],
                ['file.xml1', 'file.yml']
            ),
            (
                'file.{b..d}',
                '^file\\.[b-d]$',
                ['file.b', 'file.c', 'file.d'],
                ['file.a', 'file.e']
            ),
            (
                'file.{d..b}',
                '^file\\.[b-d]$',
                ['file.b', 'file.c', 'file.d'],
                ['file.a', 'file.e']
            ),
            (
                'file.{c..E}',
                '^file\\.[E-Za-c\\[\\\\\\]\\^_`]$',
                ['file.E', 'file.F', 'file.b', 'file._', 'file.^', 'file.`', 'file.['],
                ['file.D', 'file.d', 'file.+']
            ),
            (
                'file{2..5}',
                '^file[2-5]$',
                ['file2', 'file3', 'file4'],
                ['file1', 'file6']
            ),
            (
                'file{5..2}',
                '^file[2-5]$',
                ['file2', 'file3', 'file4'],
                ['file1', 'file6']
            ),
            (
                'file{-2..5}',
                '^file-?[0-5]$',
                ['file-2', 'file-1', 'file4'],
                ['file-9', 'file6']
            ),
        ]
    )
    def test_wildcard_for_expansion_case(self, data, expected_pattern,
                                         matched_results, not_matched_results):
        node = Wildcard(data, is_prefix=False, is_postfix=False, ignore_case=False)
        pattern = node.pattern
        assert pattern == expected_pattern
        for matched_result in matched_results:
            matched = re.match(pattern, matched_result)
            assert bool(matched)

        if not_matched_results:
            for not_matched_result in not_matched_results:
                matched = re.match(pattern, not_matched_result)
                assert not bool(matched)
