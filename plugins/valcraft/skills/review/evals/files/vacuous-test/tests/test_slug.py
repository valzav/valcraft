import unittest

from slug import slugify


class SlugifyTest(unittest.TestCase):
    def test_lowercases_and_hyphenates(self):
        self.assertEqual(slugify("Quarterly Report"), "quarterly-report")

    def test_collapses_whitespace(self):
        self.assertEqual(slugify("  Quarterly   Report "), "quarterly-report")


if __name__ == "__main__":
    unittest.main()
