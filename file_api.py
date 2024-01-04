from os import listdir
from os.path import isfile, join, splitext
import shutil
import pathlib
import re


def normalizeFilename(source_name, postfix: str) -> str:
    # Replace white space with underscores:
    filename_new = re.sub('\s+', '_', source_name)
        
    # Erase non-alphanumeric-period-underscore characters:
    filename_new = re.sub('[^a-zA-Z0-9._-]', '',  filename_new)
        
    # eleminate dots
    fprefix, fext = splitext(filename_new)
    fprefix = fprefix.replace(".", "_")
    
    # Merge consecutive underscores for aesthetics
    fprefix = re.sub('_+', '_', fprefix)
    
    # add postfix
    if len(postfix) > 0:
        fprefix = fprefix + "_" + postfix
        
    filename_new = fprefix + fext
        
    return filename_new

def moveDirectory(source_dir, target_dir):
    shutil.move(source_dir, target_dir)

def getSubDirectories(directory):
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

def moveDirectoryArchive(source_dir, target_objdir, target_subdir, archive_dir):
    target_dir = archive_dir + '/' + target_objdir + '/' + target_subdir 
    moveDirectory(source_dir, target_dir)
