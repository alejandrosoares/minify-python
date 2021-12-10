"""
.. module:: minify
    :synopsis: All classes used in the project are here.
"""

from distutils.dir_util import copy_tree
from pathlib import Path
import sys
import os
import ntpath
import glob
import requests
from PIL import Image

from utils import (
    get_url, 
    get_size,
    get_extension
)
from settings import (
    DST_FOLDER,
    VALID_EXTENSIONS_FILE,
    VALID_EXTENSIONS_IMG,
    EXT_TO_COMPRESS,
    QUALITY_COMPRESSION
)

def create_instance(file):
    e = get_extension(file)
    pathname = Path(file)

    if e in VALID_EXTENSIONS_FILE:
        instance = CodeFile(pathname, e)
    elif e in VALID_EXTENSIONS_IMG:
        instance = ImageFile(pathname, e)
    else:
        instance = None

    return instance

class File:
    """
    Base class for (all)File classes
    """
    def __init__(self, pathname, extension):
        self.extension = extension
        self.pathname = pathname

class CodeFile(File):
    """
    Class for html, css and js files
    :self.process: minifies these files
    """
    def __init__(self, pathname, extension):
        self.raw_content = None
        self.minified_content = None
        self.minified = False
        super(__class__, self).__init__(pathname, extension)

    def __get_raw_content(self):
        with open(self.pathname, 'r') as c:
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
            with open(self.pathname, 'w') as m:
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
    """
    Class for image files
    :process(): compresses these files
    """
    def __init__(self, file, extension):
        self.compressed = False
        super(__class__, self).__init__(file, extension)

    def __get_path_name(self):
        """
        Take self.pathname and return 
        the path and name separately
        :@return: tuple(str, str)
        """
        return ntpath.split(self.pathname)
    
    def __generate_compressed_pathname(self):
        """
        :@return: PosixPath
        """
        path, name = self.__get_path_name()
        return Path(f"{path}/compressed_{name}")

    def process(self):
        """
        Compress the instance if you extension is .jpg or .jpeg
        Saved compressed img with prefix compressed
        """
        if self.extension in EXT_TO_COMPRESS:
            c_pathname = self.__generate_compressed_pathname()

            o = Image.open(self.pathname)
            o_size = get_size(self.pathname)
            
            # compress
            o.save(
                c_pathname, 
                optimized=True, 
                quality=QUALITY_COMPRESSION
                )
            c_size = get_size(c_pathname)

            if c_size > o_size:
                os.remove(c_pathname)
            else:
                os.remove(self.pathname)
                os.rename(c_pathname, self.pathname)
            
            self.compressed = True

class Process:
    """
    Class that trigger processing of each file instance
    :files: list that contains instances of CodeFile and ImageFile
    """
    dst_folder = DST_FOLDER

    def __init__(self):
        self.src = self.__set_src()
        self.dst = self.__set_dst()
        self.folder_project = self.__set_folder()
        self.re_search = self.__set_regex()
        self.files = []

    def __set_src(self):
        """
        Set source path
        :@return: src(PosixPath)
        """
        try:
            src = Path(f"../{sys.argv[1]}")
            self.folder_project = src.name
        except IndexError:
            print("Error: source path not found")
            print("Please run 'minify.py source_path destination_path'")
            sys.exit()

        return src
    
    def __set_dst(self):
        """
        Set destination path
        :@return: dst(PosixPath)
        """
        try:
            dst = Path(f"../{sys.argv[2]}/{self.dst_folder}")  
        except IndexError:
            dst = Path(f"../{self.dst_folder}")

        return dst 

    def __set_folder(self):
        """
        Set the folder name of project
        passed in the source path 
        :@return: folder(str)
        """
        folder = self.src.name

        if folder:
            self.folder_project = folder
            self.dst = self.dst / folder

        return folder

    def __set_regex(self):
        """
        Set the regex used for find the files
        :@return: regex(str)
        """
        regex = self.dst / "**/*.*"
        regex = regex.as_posix()
        return regex

    def __copy_files(self):
        copy_tree(
            self.src.as_posix(), 
            self.dst.as_posix()
            )
    
    def __load_files(self):
        for file in glob.iglob(self.re_search, recursive=True):
            instance = create_instance(file)
            if instance:
                self.files.append(instance)

    def __process_files(self):
        for f in self.files:
            f.process()

    def run(self):
        self.__copy_files()
        self.__load_files()
        self.__process_files()

if __name__ == "__main__":

    p = Process()
    p.run()