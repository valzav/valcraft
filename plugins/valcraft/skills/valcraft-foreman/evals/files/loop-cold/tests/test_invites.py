import re
import unittest
from datetime import datetime, timedelta

import invites

NOW = datetime(2026, 8, 16, 9, 0, 0)
URL_SAFE = re.compile(r"^[A-Za-z0-9_-]+$")


class CreateLinkTest(unittest.TestCase):
    def test_expiry_and_token(self):
        """TS-001: AC-001."""
        for _ in range(100):
            link = invites.create_link("w1", NOW)
            self.assertEqual(link.expires_at, NOW + timedelta(days=7))
            self.assertRegex(link.token, URL_SAFE)


if __name__ == "__main__":
    unittest.main()
