import pytest   # noqa

from genericlib import NUMBER


class TestNumber:

    @pytest.mark.parametrize(
        "constant_number,expected_result",
        [
            (NUMBER.ZERO, 0),
            (NUMBER.ONE, 1),
            (NUMBER.TWO, 2),
            (NUMBER.THREE, 3),
            (NUMBER.FOUR, 4),
            (NUMBER.FIVE, 5),
            (NUMBER.SIX, 6),
            (NUMBER.SEVEN, 7),
            (NUMBER.EIGHT, 8),
            (NUMBER.NINE, 9),
            (NUMBER.TEN, 10),
            (NUMBER.ELEVEN, 11),
            (NUMBER.TWELVE, 12),
            (NUMBER.THIRTEEN, 13),
            (NUMBER.FOURTEEN, 14),
            (NUMBER.FIFTEEN, 15),
            (NUMBER.SIXTEEN, 16),
            (NUMBER.SEVENTEEN, 17),
            (NUMBER.EIGHTEEN, 18),
            (NUMBER.NINETEEN, 19),
            (NUMBER.TWENTY, 20),
            (NUMBER.THIRTY, 30),
            (NUMBER.FORTY, 40),
            (NUMBER.FIFTY, 50),
            (NUMBER.SIXTY, 60),
            (NUMBER.SEVENTY, 70),
            (NUMBER.EIGHTY, 80),
            (NUMBER.NINETY, 90),
            (NUMBER.HUNDRED, 100),
            (NUMBER.THOUSAND, 1000),


        ]
    )
    def test_constant_number(self, constant_number, expected_result):
        assert constant_number == expected_result
