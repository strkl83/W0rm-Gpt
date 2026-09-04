import contextlib
import io
import os
import unittest
from argparse import Namespace
from unittest.mock import patch

from main import DEFAULT_BASE_URL, DEFAULT_MODEL, Settings, ask, print_health


class MainTests(unittest.TestCase):
    def test_defaults_are_safe_and_explicit(self):
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings.from_environment(Namespace(base_url=None, model=None))
        self.assertIsNone(settings.api_key)
        self.assertEqual(settings.base_url, DEFAULT_BASE_URL)
        self.assertEqual(settings.model, DEFAULT_MODEL)

    def test_base_url_is_normalized(self):
        settings = Settings.from_environment(
            Namespace(base_url="https://example.test/v1/", model="demo")
        )
        self.assertEqual(settings.base_url, "https://example.test/v1")
        self.assertEqual(settings.model, "demo")

    def test_health_never_requires_a_key(self):
        output = io.StringIO()
        settings = Settings(None, DEFAULT_BASE_URL, DEFAULT_MODEL, "test")
        with contextlib.redirect_stdout(output):
            result = print_health(settings)
        self.assertEqual(result, 0)
        self.assertIn("not configured", output.getvalue())

    def test_missing_key_does_not_make_a_request(self):
        output = io.StringIO()
        settings = Settings(None, DEFAULT_BASE_URL, DEFAULT_MODEL, "test")
        with contextlib.redirect_stdout(output):
            result = ask(settings, "hello")
        self.assertEqual(result, 2)
        self.assertIn("No API key is configured", output.getvalue())


if __name__ == "__main__":
    unittest.main()