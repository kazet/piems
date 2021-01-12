from decimal import Decimal
from unittest.case import TestCase

from .evaluate import evaluate
from .hourminutetime import HourMinuteTimeInterval


class SICTestCase(TestCase):
    def test_calculating_time_interval_without_midnight(self):
        self.assertEqual(evaluate("19:12 to 19:34"), HourMinuteTimeInterval(minutes=Decimal(22)))

    def test_calculating_time_interval_with_midnight(self):
        self.assertEqual(evaluate("19:12 to 19:11"), HourMinuteTimeInterval(hours=Decimal(23), minutes=Decimal(59)))

    def test_addition(self):
        self.assertEqual(evaluate("1h 2m + 2h 3m"), HourMinuteTimeInterval(hours=Decimal(3), minutes=Decimal(5)))

    def test_subtraction(self):
        self.assertEqual(evaluate("1h 2m - 2h 3m"), HourMinuteTimeInterval(hours=Decimal(-1), minutes=Decimal(-1)))

    def test_addition_and_subtraction_ordering(self):
        self.assertEqual(evaluate("1h + 2h - 1h"), HourMinuteTimeInterval(hours=Decimal(2)))
        self.assertEqual(evaluate("1h - 1h + 2h"), HourMinuteTimeInterval(hours=Decimal(2)))

    def test_const_multiplication(self):
        self.assertEqual(evaluate("3 * 1h 2m"), HourMinuteTimeInterval(hours=Decimal(3), minutes=Decimal(6)))
        self.assertEqual(evaluate("1h 2m * 3"), HourMinuteTimeInterval(hours=Decimal(3), minutes=Decimal(6)))

    def test_ordering(self):
        self.assertEqual(evaluate("3 * 1h 2m + 1h 1m"), HourMinuteTimeInterval(hours=Decimal(4), minutes=Decimal(7)))
