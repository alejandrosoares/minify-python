import sys
import requests
import glob

URL_CSS = 'https://www.toptal.com/developers/cssminifier/raw'
URL_JS = 'https://www.toptal.com/developers/javascript-minifier/raw'

VALID_EXTENSIONS = [
    ".css",
    ".js"
]
LIST_FILES = []

def get_extension(file_name):

    dotIndex = file_name.rfind(".", 1)
    extension = file_name[dotIndex:]

    return extension


def get_url(file_name):
    """
    Get the url according to the file extension 
    """

    extension = get_extension(file_name)
    
    print("extension ", extension)
    
    if extension == ".js":
        url = URL_JS
    elif extension == ".css":
        url = URL_CSS
    else:
        raise ValueError("Invalid extension")

    return url


def get_file():
    try:
        raw_file = sys.argv[1]
        print(sys.argv)
    except:
        print("Missing input file")
        sys.exit()

    return raw_file


def open_content_of_file(raw_file):
    with open(raw_file, 'r') as c:
        content = c.read()

    return content


def make_request(content, file_name):
    payload = {'input': content}
    url =  get_url(file_name)
    r = requests.post(url, payload)

    if r.status_code == 200:
        return r.text

    return None


def write_minified_file(minified_content, raw_file, extension):
    minified_name = f"{raw_file.rstrip(extension)}.min{extension}"
    with open(minified_name, 'w') as m:
        m.write(minified_content)


def get_files():
    
    for extension in VALID_EXTENSIONS:
        LIST_FILES.extend(glob.glob(f'*{extension}'))

    print(LIST_FILES)


def Main():

    raw_file = get_file()
    content = open_content_of_file(raw_file)
    minified_content = make_request(content, raw_file)
    write_minified_file(minified_content, raw_file, get_extension(raw_file))
    get_files()
    

if __name__ == "__main__":
    Main()
    

