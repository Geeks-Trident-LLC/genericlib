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
                'file_{abc,xyz}.txt',
                '^file_(abc|xyz)\\.txt$',
                ['file_abc.txt', 'file_xyz.txt'],
                ['file_abd.txt', 'file_123.txt']
            ),
            (
                'file_{abc,}.txt',
                '^file_(abc)?\\.txt$',
                ['file_abc.txt', 'file_.txt'],
                ['file_abd.txt', 'file__.txt']
            ),
            (
                'file_{abc,,xyz}.txt',
                '^file_(abc|xyz)?\\.txt$',
                ['file_abc.txt', 'file_.txt', 'file_xyz.txt'],
                ['file_abd.txt', 'file__.txt']
            ),
            (
                'file_{abc,,xyz,}.txt',
                '^file_(abc|xyz)?\\.txt$',
                ['file_abc.txt', 'file_.txt', 'file_xyz.txt'],
                ['file_abd.txt', 'file__.txt']
            ),
            (
                'file_{,}.txt',
                '^file_\\.txt$',
                ['file_.txt'],
                ['file_abd.txt', 'file__.txt']
            ),
            (
                'file_{,,,}.txt',
                '^file_\\.txt$',
                ['file_.txt', ],
                ['file_abd.txt', 'file__.txt']
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
                'file{5..10}',
                '^file([5-9]|(10))$',
                ['file5', 'file9', 'file10'],
                ['file4', 'file11']
            ),
            (
                'file{9..10}',
                '^file(9|(10))$',
                ['file9', 'file10'],
                ['file4', 'file8', 'file11']
            ),
            (
                'file{5..17}',
                '^file([5-9]|(1[0-7]))$',
                ['file5', 'file11', 'file17'],
                ['file4', 'file20', 'file18']
            ),
            (
                'file{9..17}',
                '^file(9|(1[0-7]))$',
                ['file9', 'file11', 'file17'],
                ['file4', 'file20', 'file18']
            ),
            (
                'file{5..27}',
                '^file([5-9]|(1[0-9])|(2[0-7]))$',
                ['file5', 'file12', 'file27'],
                ['file4', 'file99', 'file28']
            ),
            (
                'file{5..29}',
                '^file([5-9]|([1-2][0-9]))$',
                ['file5', 'file12', 'file29'],
                ['file4', 'file99', 'file30']
            ),
            (
                'file{9..29}',
                '^file(9|([1-2][0-9]))$',
                ['file9', 'file12', 'file29'],
                ['file8', 'file99', 'file30']
            ),
            (
                'file{5..40}',
                '^file([5-9]|([1-3][0-9])|(40))$',
                ['file5', 'file31', 'file40'],
                ['file4', 'file41', 'file99']
            ),
            (
                'file{9..40}',
                '^file(9|([1-3][0-9])|(40))$',
                ['file9', 'file31', 'file40'],
                ['file8', 'file41', 'file99']
            ),
            (
                'file{5..43}',
                '^file([5-9]|([1-3][0-9])|(4[0-3]))$',
                ['file5', 'file31', 'file42'],
                ['file4', 'file44', 'file99']
            ),
            (
                'file{5..49}',
                '^file([5-9]|([1-4][0-9]))$',
                ['file5', 'file31', 'file49'],
                ['file4', 'file50', 'file99']
            ),
            (
                'file{22..27}',
                '^file2[2-7]$',
                ['file22', 'file25', 'file27'],
                ['file21', 'file30', 'file28']
            ),
            (
                'file{22..30}',
                '^file((2[2-9])|(30))$',
                ['file22', 'file25', 'file30'],
                ['file21', 'file31', 'file99']
            ),
            (
                'file{22..37}',
                '^file((2[2-9])|(3[0-7]))$',
                ['file22', 'file31', 'file37'],
                ['file21', 'file38', 'file44']
            ),
            (
                'file{34..71}',
                '^file((3[4-9])|([4-6][0-9])|(7[0-1]))$',
                ['file34', 'file55', 'file71'],
                ['file33', 'file99', 'file72']
            ),
            (
                'file{34..79}',
                '^file((3[4-9])|([4-7][0-9]))$',
                ['file34', 'file55', 'file79'],
                ['file33', 'file99', 'file80']
            ),
            (
                'file{5..100}',
                '^file([5-9]|([1-9][0-9])|(100))$',
                ['file34', 'file55', 'file71', 'file100'],
                ['file3', 'file2', 'file101']
            ),
            (
                'file{25..100}',
                '^file((2[5-9])|([3-9][0-9])|(100))$',
                ['file34', 'file55', 'file99', 'file100'],
                ['file21', 'file22', 'file101']
            ),
            (
                'file{95..100}',
                '^file(9[5-9]|(100))$',
                ['file95', 'file96', 'file99', 'file100'],
                ['file94', 'file93', 'file101']
            ),
            (
                'file{99..100}',
                '^file((99)|(100))$',
                ['file99', 'file100'],
                ['file98', 'file93', 'file101']
            ),
            # two negative numbers
            (
                'file{-2..-5}',
                '^file(-[2-5])$',
                ['file-2', 'file-3', 'file-4'],
                ['file-6', 'file0', 'file2']
            ),
            (
                'file{-5..-2}',
                '^file(-[2-5])$',
                ['file-2', 'file-3', 'file-4'],
                ['file-6', 'file0', 'file2']
            ),
            (
                'file{-7..-10}',
                '^file(-([7-9]|(10)))$',
                ['file-7', 'file-9', 'file-10'],
                ['file-6', 'file-11', 'file-20']
            ),
            (
                'file{-9..-10}',
                '^file(-(9|(10)))$',
                ['file-9', 'file-10'],
                ['file-6', 'file-11', 'file-20']
            ),
            (
                'file{-9..-17}',
                '^file(-(9|(1[0-7])))$',
                ['file-9', 'file-10', 'file-17'],
                ['file-8', 'file-18', 'file-20']
            ),
            (
                'file{-5..-17}',
                '^file(-([5-9]|(1[0-7])))$',
                ['file-5', 'file-10', 'file-17'],
                ['file-4', 'file-18', 'file-20']
            ),
            (
                'file{-5..-20}',
                '^file(-([5-9]|(1[0-9])|(20)))$',
                ['file-5', 'file-10', 'file-20'],
                ['file-4', 'file-21', 'file-30']
            ),
            (
                'file{-5..-27}',
                '^file(-([5-9]|(1[0-9])|(2[0-7])))$',
                ['file-5', 'file-19', 'file-27'],
                ['file-4', 'file-28', 'file-30']
            ),
            (
                'file{-5..-29}',
                '^file(-([5-9]|([1-2][0-9])))$',
                ['file-5', 'file-19', 'file-29'],
                ['file-4', 'file-31', 'file-30']
            ),
            (
                'file{-25..-29}',
                '^file(-2[5-9])$',
                ['file-25', 'file-28', 'file-29'],
                ['file-24', 'file-31', 'file-30']
            ),
            (
                'file{-25..-30}',
                '^file(-((2[5-9])|(30)))$',
                ['file-25', 'file-28', 'file-29'],
                ['file-24', 'file-31', 'file-32']
            ),
            (
                'file{-25..-36}',
                '^file(-((2[5-9])|(3[0-6])))$',
                ['file-25', 'file-28', 'file-36'],
                ['file-24', 'file-37', 'file-44']
            ),
            (
                'file{-25..-47}',
                '^file(-((2[5-9])|(3[0-9])|(4[0-7])))$',
                ['file-25', 'file-38', 'file-47'],
                ['file-24', 'file-48', 'file-55']
            ),
            (
                'file{-25..-57}',
                '^file(-((2[5-9])|([3-4][0-9])|(5[0-7])))$',
                ['file-25', 'file-38', 'file-57'],
                ['file-24', 'file-58', 'file-65']
            ),
            (
                'file{-25..-59}',
                '^file(-((2[5-9])|([3-5][0-9])))$',
                ['file-25', 'file-38', 'file-59'],
                ['file-24', 'file-60', 'file-65']
            ),
            (
                'file{-25..-60}',
                '^file(-((2[5-9])|([3-5][0-9])|(60)))$',
                ['file-25', 'file-60', 'file-59'],
                ['file-24', 'file-61', 'file-65']
            ),
            (
                'file{-25..-61}',
                '^file(-((2[5-9])|([3-5][0-9])|(6[0-1])))$',
                ['file-25', 'file-61', 'file-59'],
                ['file-24', 'file-62', 'file-65']
            ),
            (
                'file{-5..-100}',
                '^file(-([5-9]|([1-9][0-9])|(100)))$',
                ['file-5', 'file-61', 'file-99', 'file-100'],
                ['file-4', 'file-101', 'file-102']
            ),
            (
                'file{-9..-100}',
                '^file(-(9|([1-9][0-9])|(100)))$',
                ['file-9', 'file-61', 'file-99', 'file-100'],
                ['file-8', 'file-101', 'file-102']
            ),
            (
                'file{-25..-100}',
                '^file(-((2[5-9])|([3-9][0-9])|(100)))$',
                ['file-25', 'file-61', 'file-99', 'file-100'],
                ['file-24', 'file-101', 'file-102']
            ),
            (
                'file{-29..-100}',
                '^file(-((29)|([3-9][0-9])|(100)))$',
                ['file-29', 'file-61', 'file-99', 'file-100'],
                ['file-28', 'file-101', 'file-102']
            ),
            (
                'file{-95..-100}',
                '^file(-(9[5-9]|(100)))$',
                ['file-95', 'file-98', 'file-99', 'file-100'],
                ['file-94', 'file-101', 'file-102']
            ),
            (
                'file{-99..-100}',
                '^file(-((99)|(100)))$',
                ['file-99', 'file-100'],
                ['file-98', 'file-101', 'file-102']
            ),
            # positive and negative numbers
            (
                'file{-2..5}',
                '^file((-[0-2])|[0-5])$',
                ['file-2', 'file-1', 'file4'],
                ['file-3', 'file-4', 'file6']
            ),
            (
                'file{-2..10}',
                '^file((-[0-2])|([0-9]|(10)))$',
                ['file-2', 'file-1', 'file4', 'file10'],
                ['file-3', 'file-4', 'file11']
            ),
            (
                'file{-5..15}',
                '^file((-[0-5])|([0-9]|(1[0-5])))$',
                ['file-5', 'file-1', 'file4', 'file15'],
                ['file-6', 'file-24', 'file16']
            ),
            (
                'file{-15..5}',
                '^file((-([0-9]|(1[0-5])))|[0-5])$',
                ['file-15', 'file-1', 'file4', 'file5'],
                ['file-16', 'file-24', 'file6']
            ),
            (
                'file{-5..100}',
                '^file((-[0-5])|([0-9]|([1-9][0-9])|(100)))$',
                ['file-5', 'file-1', 'file99', 'file100'],
                ['file-6', 'file-24', 'file101']
            ),
            (
                'file{-100..5}',
                '^file((-([0-9]|([1-9][0-9])|(100)))|[0-5])$',
                ['file-100', 'file-99', 'file4', 'file5'],
                ['file-101', 'file24', 'file6']
            ),
            (
                'file{-100..100}',
                '^file((-([0-9]|([1-9][0-9])|(100)))|([0-9]|([1-9][0-9])|(100)))$',
                ['file-100', 'file-99', 'file99', 'file100'],
                ['file-101', 'file224', 'file101']
            ),
            (
                'file{-10..10}',
                '^file((-([0-9]|(10)))|([0-9]|(10)))$',
                ['file-10', 'file-1', 'file4', 'file10'],
                ['file-11', 'file-14', 'file11']
            ),
            (
                'file{-15..15}',
                '^file((-([0-9]|(1[0-5])))|([0-9]|(1[0-5])))$',
                ['file-15', 'file-1', 'file4', 'file15'],
                ['file-16', 'file-24', 'file16']
            ),
            (
                'file{-15..19}',
                '^file((-([0-9]|(1[0-5])))|([0-9]|(1[0-9])))$',
                ['file-15', 'file-1', 'file4', 'file19'],
                ['file-16', 'file-24', 'file20']
            ),
            (
                'file{-15..20}',
                '^file((-([0-9]|(1[0-5])))|([0-9]|(1[0-9])|(20)))$',
                ['file-15', 'file-1', 'file4', 'file20'],
                ['file-16', 'file-24', 'file21']
            ),
            (
                'file{-15..32}',
                '^file((-([0-9]|(1[0-5])))|([0-9]|([1-2][0-9])|(3[0-2])))$',
                ['file-15', 'file-1', 'file4', 'file32'],
                ['file-16', 'file-24', 'file33']
            ),
            (
                'file{-15..32}',
                '^file((-([0-9]|(1[0-5])))|([0-9]|([1-2][0-9])|(3[0-2])))$',
                ['file-15', 'file-1', 'file4', 'file32'],
                ['file-16', 'file-24', 'file33']
            ),
            (
                'file{-15..39}',
                '^file((-([0-9]|(1[0-5])))|([0-9]|([1-3][0-9])))$',
                ['file-15', 'file-1', 'file4', 'file39'],
                ['file-16', 'file-24', 'file40']
            ),
            (
                'file{-30..39}',
                '^file((-([0-9]|([1-2][0-9])|(30)))|([0-9]|([1-3][0-9])))$',
                ['file-30', 'file-1', 'file4', 'file39'],
                ['file-31', 'file-44', 'file40']
            ),
            (
                'file{-33..39}',
                '^file((-([0-9]|([1-2][0-9])|(3[0-3])))|([0-9]|([1-3][0-9])))$',
                ['file-33', 'file-1', 'file4', 'file39'],
                ['file-34', 'file-44', 'file40']
            ),
            (
                'file{-39..39}',
                '^file((-([0-9]|([1-3][0-9])))|([0-9]|([1-3][0-9])))$',
                ['file-39', 'file-1', 'file4', 'file39'],
                ['file-40', 'file-44', 'file40']
            ),
            # Limiting repetition
            (
                'file_a{2}.txt',
                '^file_a{2}\\.txt$',
                ['file_aa.txt'],
                ['file_a.txt', 'file_aaa.txt', 'file_.txt']
            ),
            (
                'file_a{1,2}.txt',
                '^file_a{1,2}\\.txt$',
                ['file_a.txt', 'file_aa.txt'],
                ['file_aaa.txt', 'file_.txt']
            ),
            (
                'file_a{,2}.txt',
                '^file_a{,2}\\.txt$',
                ['file_.txt', 'file_a.txt', 'file_aa.txt'],
                ['file_aaa.txt']
            ),
            (
                'file_a{2,}.txt',
                '^file_a{2,}\\.txt$',
                ['file_aa.txt', 'file_aaaa.txt', 'file_aaaaaaaaaa.txt'],
                ['file_.txt', 'file_a.txt']
            ),
            # Limiting repetition with back flash
            (
                'file_a\\{2\\}.txt',
                '^file_a{2}\\.txt$',
                ['file_aa.txt'],
                ['file_a.txt', 'file_aaa.txt', 'file_.txt']
            ),
            (
                'file_a\\{1,2\\}.txt',
                '^file_a{1,2}\\.txt$',
                ['file_a.txt', 'file_aa.txt'],
                ['file_aaa.txt', 'file_.txt']
            ),
            (
                'file_a\\{,2\\}.txt',
                '^file_a{,2}\\.txt$',
                ['file_.txt', 'file_a.txt', 'file_aa.txt'],
                ['file_aaa.txt']
            ),
            (
                'file_a\\{2,\\}.txt',
                '^file_a{2,}\\.txt$',
                ['file_aa.txt', 'file_aaaa.txt', 'file_aaaaaaaaaa.txt'],
                ['file_.txt', 'file_a.txt']
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

    @pytest.mark.parametrize(
        "data,expected_failure",
        [
            ('file_{5..101}', '^file_unsupported parsing integers (5, 101)$'),
            ('file_{5..199}', '^file_unsupported parsing integers (5, 199)$'),
            ('file_{235..545}', '^file_unsupported parsing integers (235, 545)$'),
            ('file_{235..9}', '^file_unsupported parsing integers (9, 235)$'),
            ('file_{-101..-9}', '^file_unsupported parsing integers (-101, -9)$'),
            ('file_{-9..-101}', '^file_unsupported parsing integers (-101, -9)$'),
            ('file_{-119..-101}', '^file_unsupported parsing integers (-119, -101)$'),
            ('file_{-101..5}', '^file_unsupported parsing integers (-101, 5)$'),
            ('file_{-101..222}', '^file_unsupported parsing integers (-101, 222)$'),
            ('file_{-25..222}', '^file_unsupported parsing integers (-25, 222)$'),
        ]
    )
    def test_wildcard_for_expansion_unsupported_case(self, data, expected_failure):
        node = Wildcard(data, is_prefix=False, is_postfix=False, ignore_case=False)
        pattern = node.pattern
        assert pattern == expected_failure

    @pytest.mark.parametrize(
        "data,expected_result",
        [
            ('file_{5 11}', r'^file_\{5 11\}$'),
            ('file_{5-11}', r'^file_\{5\-11\}$'),
            ('file_{5 - 11}', r'^file_\{5 \- 11\}$'),
            ('file_{5...11}', r'^file_\{5\.\.\.11\}$'),
            ('file_{5:11}', r'^file_\{5:11\}$'),
            ('file_{aa..z}', r'^file_\{aa\.\.z\}$'),
            ('file_{a..az}', r'^file_\{a\.\.az\}$'),
            ('file_{a az}', r'^file_\{a az\}$'),
            ('file_{abc}', r'^file_\{abc\}$'),
        ]
    )
    def test_wildcard_for_unrecognized_expansion_case(self, data, expected_result):
        node = Wildcard(data, is_prefix=False, is_postfix=False, ignore_case=False)
        pattern = node.pattern
        assert pattern == expected_result
