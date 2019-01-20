from unittest import TestCase
from datetime import date
from . import speaker

import ddt


@ddt.ddt
class SmmValidator(TestCase):
    @ddt.data(
        (1, speaker.LANG['EN'], 0, 'year'),
        (2, speaker.LANG['EN'], 0, 'years'),
    )
    @ddt.unpack
    def test_EN(self, value, lang, index, expected):
        self.assertEqual(speaker.smm(value, lang, index), expected)


@ddt.ddt
class CogwheelValidator(TestCase):
    @ddt.data(
        (True, 365, speaker.LANG['EN'], 0, 366, '1 year', 1),
        (True, 365, speaker.LANG['EN'], 0, 366, '1 year', 1),
    )
    @ddt.unpack
    def test_EN(self, boolean, divider, language, index, delta, expected1, expected2):
        self.assertEqual(speaker.cogwheel(boolean, divider, language, index, delta), (expected1, expected2))


@ddt.ddt
class DeltaDatePrinterValidator(TestCase):
    @ddt.data(
        (date(day=16, month=11, year=1988), date(day=21, month=11, year=1988), '5 days'),
    )
    @ddt.unpack
    def test_EN_with_two_arg(self, date_st, date_end, expected):
        self.assertEqual(speaker.delta_date_printer(date_st, date_end), expected)









