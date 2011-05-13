from helper import getSourceCode
import xml.etree.ElementTree
import urllib.parse

def getTrackInfo(artist, track):
    try:
        url = "http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key=b25b959554ed76058ac220b7b2e0a026&artist=%s&track=%s&autocorrect=1" % (urllib.parse.quote(artist), urllib.parse.quote(track))
        ret = getSourceCode(url)
    except urllib.error.HTTPError:
        return None
    else:
        return xml.etree.ElementTree.XML(ret)

def getAlbumInfo(album, artist):
    try:
        url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=b25b959554ed76058ac220b7b2e0a026&album=%s&artist=%s&autocorrect=1" % (urllib.parse.quote(album), urllib.parse.quote(artist))
        ret = getSourceCode(url)
    except urllib.error.HTTPError:
        return None
    else:
        return xml.etree.ElementTree.XML(ret)
