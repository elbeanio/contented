import unittest
from settings import get_settings
from app import Application


class SettingsTests(unittest.TestCase):
    def test_global_settings(self):
        s = get_settings({})
        self.assertEqual(s.DEBUG, False)

    def test_override_global(self):
        s = get_settings({"DEBUG": True})
        self.assertEqual(s.DEBUG, True)


class AppTests(unittest.TestCase):
    def test_load_app(self):
        app = Application({})
        self.assertTrue(hasattr(app, "settings"))
        self.assertTrue(hasattr(app, "jinja_env"))

if __name__ == "__main__":
    unittest.main()
