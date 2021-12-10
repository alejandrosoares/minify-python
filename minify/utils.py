"""
.. module:: utils
    :synopsis: Contains helper functions used in the minify.py module.
"""
import os

from settings import (
    URL_HTML,
    URL_CSS,
    URL_JS
)

GET_SIZE = os.path.getsize

def get_extension(file):
    dot_index = file.rfind(".", 1)
    return file[dot_index:]

def get_size(pathname):
    """
    Return the size of file
    :@param: pathname(str)
    :@return: size(int)
    """
    size = GET_SIZE(pathname)
    return size

def get_url(extension):
    """
    Get the url according to the file extension
    :@param: extension(str)
    :@return: url(str)
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

