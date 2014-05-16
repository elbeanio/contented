from __future__ import print_function
from __future__ import absolute_import

import argparse
import os
import sys

from contented.app import Application
from settings import settings


def app_serve():
    """
    Start the built-in web server and wait for a request.
    """
    from werkzeug.serving import run_simple
    from werkzeug.wsgi import SharedDataMiddleware

    app = Application(settings)
    app_settings = app.settings

    if app_settings.debug:
        app = SharedDataMiddleware(app, {
            "/static": os.path.join(app_settings.theme_root, "static")
        })

    run_simple(app_settings.serve_on[0],
               app_settings.serve_on[1],
               app,
               use_debugger=app_settings.debug,
               use_reloader=True)


def app_test():
    """
    Run all the unit tests
    """
    import unittest
    tests = unittest.TestLoader().discover('.', pattern="*.py")
    test_runner = unittest.runner.TextTestRunner()
    test_runner.run(tests)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the contented app")
    parser.add_argument("action", help="The action to perform", nargs="?")

    commands = [cmd[4:] for cmd in dir() if cmd.startswith("app_")]
    args = parser.parse_args()

    if args.action and args.action in commands:
        this_mod = sys.modules[__name__]
        command = getattr(this_mod, "app_" + args.action)
        command()
    else:
        print("No command or command not found, please use one of the following:")
        print("\n".join(commands))
        print("e.g. python run.py serve")
