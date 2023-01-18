from os import listdir
from os.path import isfile, join
import shutil
import pathlib

from config import Config

class FileApi(object):
    
    config: Config = None

    def __init__(self, config: Config):
        self.config = config
    
    def getSubDirectories(self, directory):
        if not directory:
            return
        path = pathlib.Path(directory)
        if not path.exists() or not path.is_dir():
            return
        
        subdir = {}

        for f in listdir(directory):
            file_path = join(directory, f)
            if isfile(file_path):
                continue
            else:
                subdir[f] = file_path
        
        return subdir

    def moveDirectoryArchive(self, source_dir, target_objdir, target_subdir):
        target_dir = self.config.archive_dir + '/' + target_objdir + '/' + target_subdir 
        self.moveDirectory(source_dir, target_dir)
    
    def moveDirectory(self, source_dir, target_dir):
        shutil.move(source_dir, target_dir)