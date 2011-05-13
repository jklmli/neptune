import urllib.request
import ast
import re

# since we're going to end up for-looping, much more efficient to compile regexes
trackUidRegex = re.compile('trackUid: "([^"]*)"')
lyricIdCheckSumRegex = re.compile('return fetchFullLyrics\((\d*), (\d*), false\)')

class Download:
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.url = 'http://www.pandora.com/music/song/%s/%s' % (artist.lower().replace(' ', '+'), title.lower().replace(' ', '+'))

def decryptLyrics(encryptedLyrics, decryptionKey):
    # TODO: use string.join instead of + concatenation
    decryptedLyrics = ""
    for i in range(0, len(encryptedLyrics)):
        decryptedLyrics += chr( ord(encryptedLyrics[i]) ^ ord(decryptionKey[i % len(decryptionKey)]) )
    return decryptedLyrics

def getSourceCode(url):
    # spoof user-agent
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24')

    source = urllib.request.urlopen(request)
    ret = source.read().decode('utf-8')
    return ret

def getLyrics(url):
        sourceCode = getSourceCode(url)

        trackUid = trackUidRegex.search(sourceCode).group(1)
        intermMatch = lyricIdCheckSumRegex.search(sourceCode)
        lyricId = intermMatch.group(1)
        checkSum = intermMatch.group(2)
        nonExplicit = 'false'
        authToken = 'null'

        getEncryptedLyrics(trackUid, lyricId, checkSum, nonExplicit, authToken)

def getEncryptedLyrics(trackUid, lyricId, checkSum, nonExplicit, authToken):
    url = "http://www.pandora.com/services/ajax/?method=lyrics.getLyrics&trackUid=%s&lyricId=%s&check=%s&nonExplicit=%s&at=%s" % (trackUid, lyricId, checkSum, nonExplicit, authToken)

    ret = getSourceCode(url)

    decryptionKey = re.search('var k="([^"]*)"', ret).group(1)

    # functions in javascript can contain ", which makes python dictionary parsing throw errors
    ret = re.sub('(function[^,]*)', '0', ret)

    # use ast.literal_eval vs. eval because it's safer
    encrypted = ast.literal_eval(ret)

    encryptedLyrics= encrypted['lyrics']
    print(decryptLyrics(encryptedLyrics, decryptionKey))

def getAlbumArt():
    return 0
