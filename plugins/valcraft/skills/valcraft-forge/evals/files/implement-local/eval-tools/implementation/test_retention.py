import unittest

from retention import parse_window


class ParseWindowTest(unittest.TestCase):
    def test_accepts_hours_and_days(self):
        """FR-001, AC-001: `12h` and `30d` convert to seconds."""
        self.assertEqual(parse_window("12h"), 43_200)
        self.assertEqual(parse_window("30d"), 2_592_000)

    def test_rejects_invalid_forms(self):
        """FR-001, AC-002: every form outside the window grammar raises ValueError."""
        for value in ("", "0h", "-1d", "1w", "1.5h", "12", " 12h", "12h ", "１２h", "١d", "²d"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_window(value)


if __name__ == "__main__":
    unittest.main()
