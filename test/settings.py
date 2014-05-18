import unittest
from contented.settings import get_settings


class SettingsTests(unittest.TestCase):
    def test_global_settings(self):
        s = get_settings({})
        self.assertEqual(s.debug, False)
        self.assertEqual(len(s.content_mappers), 2)

    def test_override_global(self):
        s = get_settings({"debug": True,
                          "content_mappers": []})
        self.assertEqual(s.debug, True)
        self.assertEqual(len(s.content_mappers), 0)