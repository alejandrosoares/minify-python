import os

from settings import (
    URL_HTML,
    URL_CSS,
    URL_JS
)

GET_SIZE = os.path.getsize

def get_size(path_file):
    return GET_SIZE(path_file)

def get_url(extension):
    """
    Get the url according to the file extension
    @param: str
    @return: str
    """
    
    if extension == ".js":
        url = URL_JS
    elif extension == ".css":
        url = URL_CSS
    elif extension == ".html":
        url = URL_HTML
    else:
        url = ""

    return url

