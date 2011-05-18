import os
import urllib2
import shutil

def getSourceCode(url):
    """
    With spoofed User-Agent.
    """
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24')

    source = urllib2.urlopen(request)
    ret = source.read()
    return ret

def unescape(filePath):
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
    path = unescape(path)
    if (len(path.strip()) == 0):
        return 'Untitled'
    else:
        return path.strip().rstrip('.')

def removeEmptyDirectories(root):
    for dir, subdirs, files in os.walk(root):
        if len(subdirs) == 0 and len(files == 0):
            shutil.rmtree(dir)