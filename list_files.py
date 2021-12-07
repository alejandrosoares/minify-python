import glob
import sys
VALID_EXTENSIONS = [
    ".css",
    ".js",
    ".py"
]

def get_root_path():

    print(sys.argv[1])

def search_files(path):
    for extension in VALID_EXTENSIONS:
        for file_name in glob.iglob(f'./**/*{extension}', recursive=True):
            print(file_name)
    
def Main():
    path = get_root_path()
    #search_files(path)


if __name__ == "__main__":
    Main()