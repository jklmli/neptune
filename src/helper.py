import urllib2

def getSourceCode(url):
    # spoof user-agent
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24')

    source = urllib2.urlopen(request)
    ret = source.read()
    return ret

def unescape(filePath):
    forbiddenChars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in forbiddenChars:
        filePath = filePath.replace(char, '_')
    return filePath