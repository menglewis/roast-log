import unittest
from app.utils import convert_times_to_second_diff


class TimeDiffTestCase(unittest.TestCase):

    def test_minutes(self):
        self.assertEqual(convert_times_to_second_diff("7:30:00 AM", "7:35:00 AM"), 300)

    def test_seconds(self):
        self.assertEqual(convert_times_to_second_diff("7:30:00 AM", "7:30:05 AM"), 5)

    def test_hours(self):
        self.assertEqual(convert_times_to_second_diff("7:30:00 AM", "8:30:00 AM"), 3600)

    def test_PM(self):
        self.assertEqual(convert_times_to_second_diff("7:30:00 AM", "7:30:00 PM"), 43200)

    def test_large_diff(self):
        self.assertEqual(convert_times_to_second_diff("7:30:00 AM", "7:29:00 AM"), 86340)

    def test_invalid_time_string(self):
        with self.assertRaises(ValueError):
            convert_times_to_second_diff("badtime", "7:31:00 AM")


if __name__ == "__main__":
    unittest.main()
