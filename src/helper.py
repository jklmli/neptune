import urllib.request

def getSourceCode(url):
    # spoof user-agent
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24')

    source = urllib.request.urlopen(request)
    ret = source.read().decode('utf-8')
    return ret