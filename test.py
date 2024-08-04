import logging
import math
import unittest
from io import StringIO
from unit_converter import UnitConverter


class TestUnitConverter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Redirect logging to a string buffer for testing
        cls.log_capture = StringIO()
        cls.log_handler = logging.StreamHandler(cls.log_capture)
        logging.getLogger().addHandler(cls.log_handler)
        logging.getLogger().setLevel(logging.DEBUG)

    @classmethod
    def tearDownClass(cls):
        # Remove the log handler and close the string buffer
        logging.getLogger().removeHandler(cls.log_handler)
        cls.log_capture.close()

    def setUp(self):
        self.log_capture.seek(0)
        self.log_capture.truncate()

    def assertAlmostEqualRelative(self, a, b, rel_tol=1e-9, abs_tol=1e-12):
        return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

    def test_to_miles_per_hour(self):
        test_cases = [
            (1, "mph", 1),
            (1, "km/h", 0.621371),
            (1, "m/h", 0.00062137),
            (1, "yd/h", 0.00056818),
            (1, "ft/h", 0.00018939388),
            (1, "mpm", 60),
            (1, "km/min", 37.28227),
            (1, "m/min", 0.03728236),
            (1, "yd/min", 0.03409091),
            (1, "ft/min", 0.01136363333),
            (1, "mps", 3600),
            (1, "km/s", 2236.93629),
            (1, "m/s", 2.23694),
            (1, "yd/s", 2.04545),
            (1, "ft/s", 0.681818),
        ]

        for value, unit, expected in test_cases:
            with self.subTest(f"{value} {unit} to mph"):
                result = UnitConverter.to_miles_per_hour(value, unit)
                self.assertTrue(
                    self.assertAlmostEqualRelative(
                        result, expected, rel_tol=1e-5, abs_tol=1e-8
                    ),
                    f"Expected {expected}, but got {result}",
                )

    def test_to_miles_per_hour_invalid_unit(self):
        with self.assertRaises(ValueError):
            UnitConverter.to_miles_per_hour(1, "invalid_unit")

    def test_to_miles(self):
        test_cases = [
            (1, "miles", 1),
            (1, "kilometers", 0.621371),
            (1, "meters", 0.000621371),
            (1, "yards", 0.000568182),
            (1, "feet", 0.000189394),
        ]

        for value, unit, expected in test_cases:
            with self.subTest(f"{value} {unit} to miles"):
                result = UnitConverter.to_miles(value, unit)
                self.assertTrue(
                    self.assertAlmostEqualRelative(
                        result, expected, rel_tol=1e-5, abs_tol=1e-8
                    ),
                    f"Expected {expected}, but got {result}",
                )

    def test_to_miles_invalid_unit(self):
        with self.assertRaises(ValueError):
            UnitConverter.to_miles(1, "invalid_unit")

    def test_from_miles_to_unit(self):
        test_cases = [
            (1, "miles", 1),
            (1, "kilometers", 1.60934),
            (1, "meters", 1609.34),
            (1, "yards", 1760),
            (1, "feet", 5280),
        ]

        for value, unit, expected in test_cases:
            with self.subTest(f"{value} miles to {unit}"):
                result = UnitConverter.from_miles_to_unit(value, unit)
                self.assertTrue(
                    self.assertAlmostEqualRelative(
                        result, expected, rel_tol=1e-5, abs_tol=1e-8
                    ),
                    f"Expected {expected}, but got {result}",
                )

    def test_from_miles_to_unit_invalid_unit(self):
        with self.assertRaises(ValueError):
            UnitConverter.from_miles_to_unit(1, "invalid_unit")

    def test_logging(self):
        UnitConverter.to_miles_per_hour(1, "km/h")
        log_output = self.log_capture.getvalue()
        self.assertIn("to_miles_per_hour called with value=1, unit=km/h", log_output)
