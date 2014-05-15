from werkzeug.exceptions import NotFound


class DuplicateURLException(Exception):
    """
    Raised when a file is added to ContentMap when its request_path already exists in the collection
    """
    pass


class ContentFile(object):
    """
    Represents a content file on the filesystem, contains its own path and the request path it should render from.
    It also contains some general metadata as well as an extra dict for anything specific to the file type.
    """
    def __init__(self, file_type, file_path, request_path, title, date, **kwargs):
        self.file_type = file_type
        self.file_path = file_path
        self.request_path = request_path
        self.title = title
        self.date = date
        self.extra = kwargs


class ContentMap(object):
    """
    Map of all the content we have to serve. It could potentially have many different types of content: markdown, org,
    html, pdf, whatever.

    Provides methods to get file objects from either their filesystem path, or their request path. The request path is
    for general web serving, the file path is to help with url resolution.
    """
    def __init__(self):
        self.files = []

    def get_content_tree(self):
        """
        Returns a nested view of the content bt
        """
        pass

    def update(self, file_list):
        """
        Add a list of files to the content map.
        """
        for new_file in file_list:
            if new_file.request_path in [f.request_path for f in self.files]:
                raise DuplicateURLException(
                    "You are trying to add request path {0} ({1}) but it already exists in the collection".format(
                        new_file.request_path, new_file.file_path))

        self.files.extend(file_list)

    def from_file_path(self, file_path):
        """
        Return the ContentFile for a given file path
        """
        for item in self.files:
            if item.file_path == file_path:
                return item

        raise NotFound(description=file_path)

    def from_request_path(self, request_path):
        """
        Return the ContentFile for a given request path
        """
        for item in self.files:
            if item.request_path == request_path:
                return item

        raise NotFound(description=request_path)