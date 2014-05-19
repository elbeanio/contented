from __future__ import absolute_import

import fnmatch
import os
from datetime import datetime

import markdown

from .content_map import ContentFile


def files_for_extension(content_root, ext):
    """
    Returns a list of files in content_root with the given extension.
    """
    matches = []
    pattern = '*.{0}'.format(ext)
    for root, dirnames, filenames in os.walk(content_root):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(content_root, root, filename))
    return matches


def markdown_mapper(content_root):
    """
    Collects metadata from all the markdown files in content_root
    """
    files = files_for_extension(content_root, "md")
    content_files = []
    
    for path in files:
        web_path = path.replace(content_root, "")

        with open(path) as txt:
            text = txt.read()
            md = markdown.Markdown(extensions=["meta", ])
            md.convert(text)

        title = md.Meta.get("title", [path.split("/")[-1]])[0]
        date = md.Meta.get("date", None)
        if date:
            date = datetime.strptime(date[0], "%Y-%m-%d")
        else:
            t = os.path.getctime(path)
            date = datetime.fromtimestamp(t)

        content_files.append(ContentFile("markdown",
                                         path,
                                         web_path,
                                         title,
                                         date))
    return content_files


def org_mapper(content_root):
    """
    Collects metadata from all the org-mode files in content_root
    """
    files = files_for_extension(content_root, "org")
    content_files = []

    for path in files:
        web_path = path.replace(content_root, "")
        #TODO parse and get proper meta out
        title = "Title"
        date = "2014-05-13"
        content_files.append(ContentFile("markdown",
                                         path,
                                         web_path,
                                         title,
                                         date))
        return content_files