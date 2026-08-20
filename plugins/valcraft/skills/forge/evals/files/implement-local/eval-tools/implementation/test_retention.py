import unittest

from retention import parse_window


class ParseWindowTest(unittest.TestCase):
    def test_accepts_hours_and_days(self):
        self.assertEqual(parse_window("12h"), 43_200)
        self.assertEqual(parse_window("30d"), 2_592_000)

    def test_rejects_invalid_forms(self):
        for value in ("", "0h", "-1d", "1w", "1.5h", "12", " 12h", "12h "):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_window(value)


if __name__ == "__main__":
    unittest.main()
