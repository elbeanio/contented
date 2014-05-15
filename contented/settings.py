from __future__ import absolute_import

import os
from collections import namedtuple
from copy import deepcopy

from .mappers import markdown_mapper, org_mapper
from .request_processors import MarkdownProcessor


default_settings = {"debug": False,
                    "content_root": os.path.join(os.getcwd(), "content"),
                    "theme_root": os.path.join(os.getcwd(), "theme"),
                    "static_root": os.path.join(os.getcwd(), "static"),
                    "serve_on": ("127.0.0.1", 5001),
                    "content_mappers": [markdown_mapper, org_mapper],
                    "request_processors": [MarkdownProcessor, ]}

settings = namedtuple("settings", " ".join(default_settings.keys()))


def get_settings(local_settings):
    new_settings = deepcopy(default_settings)
    new_settings.update(local_settings)
    return settings(**new_settings)