from distutils.dir_util import copy_tree
from pathlib import Path
import sys
import os
import glob
import requests
from PIL import Image

from utils import get_url, get_size
from settings import (
    DST_FOLDER,
    VALID_EXTENSIONS_FILE,
    VALID_EXTENSIONS_IMG,
    EXT_TO_COMPRESS,
    QUALITY_COMPRESSION
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

    def __get_raw_content(self):
        with open(f"{self.path}/{self.name}", 'r') as c:
            self.raw_content = c.read()

    def __make_request(self):
        url =  get_url(self.extension)
        if url:
            payload = {'input': self.raw_content}
            r = requests.post(url, payload)

            if r.status_code == 200:
                self.minified_content = r.text
        
    def __set_minified_content(self):
        if self.minified_content:
            with open(f"{self.path}/{self.name}", 'w') as m:
                m.write(self.minified_content)
                self.minified = True

    def process(self):
        """
        Minify the instance
        """
        self.__get_raw_content()
        self.__make_request()
        self.__set_minified_content()
        
class ImageFile(File):
    def __init__(self, path, name, extension):
        self.compressed = False
        super(__class__, self).__init__(path, name, extension)

    def process(self):
        """
        Compress the instance if you extension is .jpg or .jpeg
        Saved compressed img with prefix compressed_
        """
        if self.extension in EXT_TO_COMPRESS:
            original_file = f"{self.path}/{self.name}"
            compressed_file = f"{self.path}/compressed_{self.name}"

            o = Image.open(original_file)
            o_size = get_size(original_file)
            
            # compress
            o.save(
                compressed_file, 
                optimized=True, 
                quality=QUALITY_COMPRESSION
                )
            c_size = get_size(compressed_file)

            if c_size > o_size:
                os.remove(compressed_file)
            else:
                os.remove(original_file)
                os.rename(compressed_file, original_file)

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
        self.src = self.set_src()
        self.dst = self.set_dst()
        self.folder_project = self.set_folder_project()
        self.re_search = self.set_regex_search()
        self.files = []

    def set_src(self):
        """
        Set source path
        @return: PosixPath
        """
        try:
            src = Path(f"../{sys.argv[1]}")
            self.folder_project = src.name
        except IndexError:
            print("Error: source path not found")
            print("Please run 'minify.py source_path destination_path'")
            sys.exit()

        return src
    
    def set_dst(self):
        """
        Set destination path
        @return: PosixPath
        """
        try:
            dst = Path(f"../{sys.argv[2]}/{self.dst_folder}")  
        except IndexError:
            dst = Path(f"../{self.dst_folder}")

        return dst 

    def set_folder_project(self):
        """
        Set the folder name of project
        passed in the source path 
        @return: str
        """
        folder = self.src.name

        if folder:
            self.folder_project = folder
            self.dst = self.dst / folder

        return folder

    def set_regex_search(self):
        """
        Set the regex used for find the files
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