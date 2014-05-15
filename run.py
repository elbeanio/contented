import os

from contented.app import Application
from settings import settings

if __name__ == '__main__':
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