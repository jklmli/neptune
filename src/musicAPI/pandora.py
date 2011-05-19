import ast
import re
import urllib

import helper

# since we're going to end up for-looping, much more efficient to compile regexes
trackUidRegex = re.compile('trackUid: "([^"]*)"')
lyricIdCheckSumRegex = re.compile('return fetchFullLyrics\((\d*), (\d*), false\)')

def getLyrics(track, artist):
    """
    Returns a dictionary with possible keys:
    lyrics
    If no match found, returns empty dictionary
    """
    track = track.encode('utf-8')
    artist = artist.encode('utf-8')
    url = 'http://www.pandora.com/music/song/%s/%s' % (urllib.quote_plus(artist.lower()), urllib.quote_plus(track.lower()))
    ret = helper.getSourceCode(url)

    try:
        trackUid = trackUidRegex.search(ret).group(1)
        intermMatch = lyricIdCheckSumRegex.search(ret)

        lyricId = intermMatch.group(1)
        checkSum = intermMatch.group(2)
        nonExplicit = 'false'
        authToken = 'null'
    except AttributeError:
        return {}
    else:
        return getEncryptedLyrics(trackUid, lyricId, checkSum, nonExplicit, authToken)

def getEncryptedLyrics(trackUid, lyricId, checkSum, nonExplicit, authToken):
    url = "http://www.pandora.com/services/ajax/?method=lyrics.getLyrics&trackUid=%s&lyricId=%s&check=%s&nonExplicit=%s&at=%s" % (trackUid, lyricId, checkSum, nonExplicit, authToken)
    ret = helper.getSourceCode(url)

    decryptionKey = re.search('var k="([^"]*)"', ret).group(1)

    # functions in javascript can contain ", which makes python dictionary parsing throw errors
    # workaround by replacing them out
    ret = re.sub('(function[^,]*)', '0', ret).replace('\\u00',r'\x')

    # use ast.literal_eval vs. eval because it's safer
    encrypted = ast.literal_eval(ret)

    encryptedLyrics= encrypted['lyrics']
    return decryptLyrics(encryptedLyrics, decryptionKey)

def decryptLyrics(encryptedLyrics, decryptionKey):
    # TODO: use string.join instead of + concatenation (might not be possible, since relies on mod func)
    decryptedLyrics = ""
    for i in range(0, len(encryptedLyrics)):
        decryptedLyrics += unichr(ord(encryptedLyrics[i]) ^ ord(decryptionKey[i % len(decryptionKey)]) )
    return {'lyrics': decryptedLyrics}