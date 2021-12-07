from distutils.dir_util import copy_tree
from pathlib import Path
import sys
import os
import glob
import requests

URL_CSS = 'https://www.toptal.com/developers/cssminifier/raw'
URL_JS = 'https://www.toptal.com/developers/javascript-minifier/raw'
URL_HTML = 'https://www.toptal.com/developers/html-minifier/raw'

VALID_EXTENSIONS = [
    ".css",
    ".js",
    ".html"
]

FILES_LIST = []

FOLDER_NAME = "prod"

def get_extension(file):
    """
    Get the extension of a file
    @param: str
    @return: str
    """

    dotIndex = file.rfind(".", 1)

    return file[dotIndex:]

def validate_file(file):
    """
    Return True if the file is valid
    @param: str
    @return: bool
    """

    extension = get_extension(file)

    if extension in VALID_EXTENSIONS:
        return True

    return False

def get_url(file):
    """
    Get the url according to the file extension
    @param: str
    @return: str or None 
    """

    extension = get_extension(file)
    
    if extension == ".js":
        url = URL_JS
    elif extension == ".css":
        url = URL_CSS
    elif extension == ".html":
        url = URL_HTML
    else:
        url = None

    return url
   
def get_paths():
    """
    Get source and destination folder
    @return: str, str
    """

    try:
        s_path = Path(sys.argv[1])
        folder_project = s_path.name
    except IndexError:
        s_path = Path("./")
        folder_project = None

    try:
        d_path = Path(sys.argv[2])  
    except IndexError:
        d_path = Path("./")
    
    d_path = d_path / FOLDER_NAME
    if folder_project:
         d_path = d_path / folder_project

    if not os.path.exists(s_path):
        print(f"Source folder '{s_path}' not found")
        sys.exit()

    return s_path, d_path

def copy_files(s_path, d_path):
    """
    Make a copy of all directories and files of the 
    source path in the destination path
    @param: str: source path, str: destination path
    """

    copy_tree(s_path.as_posix(), d_path.as_posix())

def make_request(content, file_name):
    
    url =  get_url(file_name)

    if url:
        payload = {'input': content}
        r = requests.post(url, payload)

        if r.status_code == 200:
            return r.text

    return None

def search_files(path):
    """
    Search all files in the destination path
    and add the files to FILES_LIST
    @param: destination path
    """

    for file_name in glob.iglob(f'{path}/**/*.*', recursive=True):
        FILES_LIST.append(file_name)

def minify_files():
    """
    Minify files that have valid extension
    """

    for file in FILES_LIST:

        if validate_file(file):
            # Open file
            with open(file, 'r') as c:
                content = c.read()
            
            # Request 
            minified_content = make_request(content, file)

            # OverWrite File
            if minified_content:
                with open(file, 'w') as m:
                    m.write(minified_content)

def Main():
    s_path, d_path = get_paths()
    copy_files(s_path, d_path)
    search_files(d_path)
    minify_files()


if __name__ == "__main__":
    Main()