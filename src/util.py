import os
import shutil

def __unescape(filePath):
    """
    Fix Windows pathname forbidden characters, by replacing them with an underscore
    """
    forbiddenChars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in forbiddenChars:
        filePath = filePath.replace(char, '_')
    return filePath

def cleanPath(path):
    """
    Rename path components to valid ones.
    """
    path = __unescape(path)
    if (len(path.strip()) == 0):
        return 'Untitled'
    else:
        return path.strip().rstrip('.')

def removeEmptyDirectories(root):
    for dir, subdirs, files in os.walk(root):
        if len(subdirs) == 0 and len(files == 0):
            shutil.rmtree(dir)