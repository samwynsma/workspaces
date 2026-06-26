import io
import sys
import os
import types
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

# Ensure workspace root is on sys.path so tests can import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from UserInterface import UserInterface


class TestUrlShortenDetailsAndLengthen(unittest.TestCase):

    def setUp(self):
        self.ui = UserInterface()

    def _install_fake_shortener(self):
        class FakeShortener:
            def __init__(self, domain):
                # keep domain without trailing slash to mimic real usage
                self.domain = domain.rstrip('/')

            def shorten(self, url):
                return f"{self.domain}/abc123"

            def access_url(self, candidate):
                if candidate.rstrip('/') == f"{self.domain}/abc123":
                    return "https://long.example.com/page"
                return None

            def get_record(self, candidate):
                if candidate.rstrip('/') == f"{self.domain}/abc123":
                    return {"url": "https://long.example.com/page", "visits": 42}
                return None

        mod = types.ModuleType("UrlShortener")
        mod.UrlShortener = FakeShortener
        sys.modules["UrlShortener"] = mod

    def testURLShortenLengthen(self):
        # Install fake UrlShortener module
        self._install_fake_shortener()

        try:
            # 1) Test shortening flow
            inputs = ["example.com", "q"]
            buf = io.StringIO()
            with patch("builtins.input", side_effect=inputs), patch.object(sys.stdin, 'isatty', return_value=True):
                with redirect_stdout(buf):
                    self.ui.cli_fallback()
            out = buf.getvalue()
            self.assertIn("Short URL:", out)
            self.assertIn("https://test/abc123", out)

            # 2) Test expanding short code
            inputs = ["abc123", "q"]
            buf = io.StringIO()
            with patch("builtins.input", side_effect=inputs), patch.object(sys.stdin, 'isatty', return_value=True):
                with redirect_stdout(buf):
                    self.ui.cli_fallback()
            out = buf.getvalue()
            self.assertIn("Long URL:", out)
            self.assertIn("https://long.example.com/page", out)

            # 3) Test expanding full short URL
            inputs = ["https://test/abc123", "q"]
            buf = io.StringIO()
            with patch("builtins.input", side_effect=inputs), patch.object(sys.stdin, 'isatty', return_value=True):
                with redirect_stdout(buf):
                    self.ui.cli_fallback()
            out = buf.getvalue()
            self.assertIn("Long URL:", out)
            self.assertIn("https://long.example.com/page", out)

            # 4) Test data command
            inputs = ["data", "abc123", "q"]
            buf = io.StringIO()
            with patch("builtins.input", side_effect=inputs), patch.object(sys.stdin, 'isatty', return_value=True):
                with redirect_stdout(buf):
                    self.ui.cli_fallback()
            out = buf.getvalue()
            self.assertIn("Record metadata:", out)
            self.assertIn("url: https://long.example.com/page", out)
            self.assertIn("visits: 42", out)

        finally:
            # Clean up module injection
            sys.modules.pop("UrlShortener", None)


if __name__ == "__main__":
    unittest.main()

