from copy import deepcopy
from mock import MagicMock, patch, mock_open
import os
import unittest

from contented.mappers import files_for_extension, markdown_mapper


file_list = [("/data", ["markdown", "org", "nothing"], ["index.md"]),
             ("/data/markdown", [], ["index.md", "file1.md", "file2.md"]),
             ("/data/org", [], ["index.org", "file1.org", "file2.org"]),
             ("/data/nothing", [], ["index.txt", "file1.txt", "file2.txt"])]


class MappersTests(unittest.TestCase):
    @patch("os.walk", return_value=iter(file_list))
    def test_file_finder(self, os_walk):
        md_files = files_for_extension("/data", "md")
        self.assertEqual(md_files[0],
                         os.path.join("/", "data", "index.md"))

    @patch("os.walk", return_value=iter(file_list))
    def test_markdown_mapper(self, os_walk):
        pass

    def test_org_mapper(self):
        pass