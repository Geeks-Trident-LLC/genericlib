"""
Unit tests for the `genericlib.conststruct` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_conststruct.py
    or
    $ python -m pytest tests/unit/test_conststruct.py
"""

import pytest
from genericlib import SLICE
from genericlib import STRUCT


class TestConstantStruct:

    @pytest.mark.parametrize(
        "data,slice_obj,expected_result",
        [
            ([0, 1, 3, 5], SLICE.FIRST_ITEM, [0]),
            ([0, 1, 3, 5], SLICE.LAST_ITEM, [5]),
            ([0, 1, 3, 5], SLICE.GET_FIRST, [0]),
            ([0, 1, 3, 5], SLICE.GET_LAST, [5]),
            ([0, 1, 3, 5], SLICE.EVERYTHING, [0, 1, 3, 5]),
            ([0, 1, 3, 5], SLICE.FIRST_TO_LAST, [1, 3]),
            ([0, 1, 3, 5], SLICE.SKIP_FROM_FIRST, [1, 3, 5]),
            ([0, 1, 3, 5], SLICE.SKIP_FROM_SECOND, [3, 5]),
            ([0, 1, 3, 5], SLICE.SKIP_FROM_THIRD, [5]),
            ([0, 1, 3, 5], SLICE.TAKE_TO_LAST, [0, 1, 3]),
            ([0, 1, 3, 5], SLICE.TAKE_TO_SECOND_LAST, [0, 1]),
            ([0, 1, 3, 5], SLICE.TAKE_TO_THIRD_LAST, [0]),
            ('01234567', SLICE.FIRST_TO_LAST, '123456'),
            ('01234567', SLICE.SECOND_TO_SECOND_LAST, '2345'),
            ('01234567', SLICE.THIRD_TO_THIRD_LAST, '34'),
        ]
    )
    def test_slice(self, data, slice_obj, expected_result):
        assert data[slice_obj] == expected_result

    def test_struct(self):
        assert STRUCT.EMPTY_LIST == []
        assert STRUCT.EMPTY_DICT == dict()
