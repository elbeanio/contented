import unittest
from datetime import datetime
from contented.content_map import ContentFile, ContentMap


class ContentFileTests(unittest.TestCase):
    def test_new_file(self):
        #storing the file date to avoid complications with asserting it
        file_date = datetime.now()
        f = ContentFile("markdown",
                        "/path/to/content/file",
                        "/content/file",
                        "A test file",
                        file_date,
                        something="extra")

        self.assertEqual(f.file_type, "markdown")
        self.assertEqual(f.file_path, "/path/to/content/file")
        self.assertEqual(f.request_path, "/content/file")
        self.assertEqual(f.title, "A test file")
        self.assertEqual(f.date, file_date)
        self.assertEqual(f.something, "extra")

    def test_dummy_file(self):
        f = ContentFile.dummy()
        self.assertEqual(f.file_type, "")
        self.assertEqual(f.file_path, "")
        self.assertEqual(f.request_path, "")
        self.assertEqual(f.title, "")


class ContentMapTests(unittest.TestCase):
    def get_fake_file(self, name, date=datetime.now()):
        return ContentFile("markdown",
                           "/path/to/name" + name,
                           "/" + name,
                           name,
                           date)

    def setUp(self):
        """
        Create a basic, fake content tree
        """
        self.cm = ContentMap()
        self.files = [self.get_fake_file("file1.md"),
                      self.get_fake_file("file2.md"),
                      self.get_fake_file("file3.md"),
                      self.get_fake_file("file4.md"),
                      self.get_fake_file("files/file1.md"),
                      self.get_fake_file("files/file2.md")]
        self.cm.update(self.files)

    def test_get_content_tree(self):
        pass

    def test_update(self):
        self.assertEqual(len(self.cm.files), 6)
        self.cm.update([self.get_fake_file("updates/fxile1.md"),
                        self.get_fake_file("updates/fxile2.md")])
        self.assertEqual(len(self.cm.files), 8)

    def test_from_file_path_found(self):
        pass

    def test_from_file_path_not_found(self):
        pass

    def test_from_request_path_found(self):
        pass

    def test_from_request_path_not_found(self):
        pass