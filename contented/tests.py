import unittest
from settings import get_settings
from app import Application


class SettingsTests(unittest.TestCase):
    def test_global_settings(self):
        s = get_settings({})
        self.assertEqual(s.debug, False)

    def test_override_global(self):
        s = get_settings({"debug": True})
        self.assertEqual(s.debug, True)


class AppTests(unittest.TestCase):
    def test_load_app(self):
        app = Application({})
        self.assertTrue(hasattr(app, "settings"))
        self.assertTrue(hasattr(app, "content_map"))
        self.assertTrue(hasattr(app, "request_processors"))

if __name__ == "__main__":
    unittest.main()
