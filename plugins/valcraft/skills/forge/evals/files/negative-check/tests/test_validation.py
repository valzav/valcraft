import unittest

from validation import require_non_empty


class RequireNonEmptyTest(unittest.TestCase):
    def test_returns_value_unchanged(self):
        self.assertEqual(require_non_empty("name", "field"), "name")

    def test_rejects_empty_value(self):
        with self.assertRaises(ValueError):
            require_non_empty("", "field")


if __name__ == "__main__":
    unittest.main()
