import unittest
from contented.app import Application


class AppTests(unittest.TestCase):
    def test_load_app(self):
        app = Application({})
        self.assertTrue(hasattr(app, "settings"))
        self.assertTrue(hasattr(app, "content_map"))
        self.assertTrue(hasattr(app, "request_processors"))