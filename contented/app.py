from werkzeug.wrappers import Request
from werkzeug.exceptions import NotFound

from settings import get_settings
from content_map import ContentMap


class Application(object):
    """
    The main WSGI application, __init__ runs on app start so we do everything here that doesn't have to be done every
    request.

    Settings - Gets the settings namedtuple which is a combination of the global settings dict and the one passed
               into this app

    Map content - runs all the content mappers, each CM will run over content_root and parse files relevant to it
                  for metadata

    Set up request processors - Each request processor is then constructed with the content map and the settings

    Everything else is handled per-request in dispatch_request()
    """

    def __init__(self, settings):
        self.settings = get_settings(settings)
        self.content_map = ContentMap()
        self.request_processors = {}

        for mapper in self.settings.content_mappers:
            files = mapper(self.settings.content_root)
            self.content_map.update(files)

        for processor in self.settings.request_processors:
            self.request_processors[processor.type] = processor(self.settings, self.content_map)

    def dispatch_request(self, request):
        """
        Loads an appropriate content file if found, runs the request processor for that file and returns the response
        """
        try:
            content_file = self.content_map.from_request_path(request.path)
        except NotFound as ex:
            request_processor = self.request_processors.values()[0]
            return request_processor.error(404, "Error, path not found: {0}".format(ex.description))

        request_processor = self.request_processors[content_file.file_type]
        response = request_processor.process(request, content_file)
        return response

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """
        Called on every request.
        """
        return self.wsgi_app(environ, start_response)