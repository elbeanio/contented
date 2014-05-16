import unittest
from contented.settings import get_settings


class SettingsTests(unittest.TestCase):
    def test_global_settings(self):
        s = get_settings({})
        self.assertEqual(s.debug, False)

    def test_override_global(self):
        s = get_settings({"debug": True})
        self.assertEqual(s.debug, True)