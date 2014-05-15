from jinja2 import Environment, FileSystemLoader
from werkzeug.wrappers import Response
import markdown


class JinjaProcessorBase(object):
    """
    Not bothered making a real base processor because I'm not planning to use another templating engine, but if
    someone wants to it's not a difficult class signature to replicate.

    Sets up a jinja env on init and should render whatever file it's passed and return a response.
    """

    def __init__(self, settings, content_map):
        self.settings = settings
        self.content_map = content_map
        self.jinja_env = Environment(loader=FileSystemLoader(self.settings.theme_root + "/templates"),
                                     autoescape=True)

    def render_theme(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return t.render(context)

    def error(self, status, message, template="error.html"):
        context = {"path": "",
                   "content_map": self.content_map,
                   "content_file": None,
                   "content": message,
                   "debug": self.settings.debug}
        content = self.render_theme(template, **context)
        return Response(content, status=status, mimetype="text/html")

    def process(self, request, content_file):
        """
         Called by the
        """
        try:
            return self.process_request(request, content_file)
        except:
            # Too broad, I know - but until we start processing things properly I don't know what needs to be trapped.
            if self.settings.debug:
                raise
            else:
                return self.error(500, "There has a been problem processing that request")

    def process_request(self, request, content_file):
        raise NotImplementedError("Process must be overridden on base class")


class MarkdownProcessor(JinjaProcessorBase):
    type = "markdown"

    def process_request(self, request, content_file):
        content_path = content_file.file_path

        with open(content_path) as txt:
            text = txt.read()
            md = markdown.Markdown(extensions=["meta", ])
            content_html = md.convert(unicode(text, "utf-8"))

        context = {"path": request.path,
                   "content_map": self.content_map,
                   "content_file": content_file,
                   "content": content_html,
                   "debug": self.settings.debug}

        content_html = self.render_theme("index.html", **context)
        return Response(content_html, mimetype="text/html")
