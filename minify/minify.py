from distutils.dir_util import copy_tree
from pathlib import Path
import sys
import os
import glob
import requests
from PIL import Image

from utils import get_url
from settings import (
    DST_FOLDER,
    VALID_EXTENSIONS_FILE,
    VALID_EXTENSIONS_IMG
)

class File:
    def __init__(self, path, name, extension):
        self.path = path
        self.name = name
        self.extension = extension

class CodeFile(File):
    def __init__(self, path, name, extension):

        self.raw_content = None
        self.minified_content = None
        self.minified = False
        super(__class__, self).__init__(path, name, extension)

    def get_raw_content(self):
        with open(f"{self.path}/{self.name}", 'r') as c:
            self.raw_content = c.read()

    def make_request(self):
        url =  get_url(self.extension)
        if url:
            payload = {'input': self.raw_content}
            r = requests.post(url, payload)

            if r.status_code == 200:
                self.minified_content = r.text
        
    def write_minified_content(self):
        if self.minified_content:
            with open(f"{self.path}/{self.name}", 'w') as m:
                m.write(self.minified_content)
                self.minified = True

    def process(self):
        """
        Minify the instance
        """
        self.get_raw_content()
        self.make_request()
        self.write_minified_content()
        

class ImageFile(File):
    def __init__(self, path, name, extension):
        self.compressed = False
        super(__class__, self).__init__(path, name, extension)

    def process(self):
        """
        Compress the instance if you
        extension is .jpg or .jpeg
        """
        pass

class FileInstanceCreator:
    def get_extension(file):
        dot_index = file.rfind(".", 1)
        return file[dot_index:]

    def get_path_and_name(file):
        return os.path.split(file)
    
    @staticmethod
    def create(file):
        e = __class__.get_extension(file)
        p, n = __class__.get_path_and_name(file)

        if e in VALID_EXTENSIONS_FILE:
            instance = CodeFile(p, n, e)
        elif e in VALID_EXTENSIONS_IMG:
            instance = ImageFile(p, n, e)
        else:
            instance = None

        return instance

class Process:
    dst_folder = DST_FOLDER

    def __init__(self):
        self.src = self.get_src()
        self.dst = self.get_dst()
        self.folder_project = self.get_folder_project()
        self.re_search = self.get_regex_search()
        self.files = []

    def get_src(self):
        try:
            src = Path(f"../{sys.argv[1]}")
            self.folder_project = src.name
        except IndexError:
            print("Error: source path not found")
            print("Please run 'minify.py source_path destination_path'")
            sys.exit()

        return src
    
    def get_dst(self):
        try:
            dst = Path(f"../{sys.argv[2]}/{self.dst_folder}")  
        except IndexError:
            dst = Path(f"../{self.dst_folder}")

        return dst 

    def get_folder_project(self):
        """
        Write the folder name of project
        passed in the source path 
        """
        folder = self.src.name

        if folder:
            self.folder_project = folder
            self.dst = self.dst / folder

        return folder

    def get_regex_search(self):
        """
        Write the regex used for find the files
        @return: str
        """
        regex = self.dst / "**/*.*"
        regex = regex.as_posix()
        return regex

    def copy_files(self):
        copy_tree(
            self.src.as_posix(), 
            self.dst.as_posix()
            )
    
    def load_files(self):
        for file in glob.iglob(self.re_search, recursive=True):
            instance = FileInstanceCreator.create(file)
            if instance:
                self.files.append(instance)

    def process_files(self):
        for f in self.files:
            f.process()

    def run(self):
        self.copy_files()
        self.load_files()
        self.process_files()


if __name__ == "__main__":

    p = Process()
    p.run()