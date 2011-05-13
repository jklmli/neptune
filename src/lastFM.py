import xml.etree.ElementTree
import urllib
import urllib2

from helper import getSourceCode

def getTrackInfo(artist, track):
    try:
        url = "http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key=b25b959554ed76058ac220b7b2e0a026&artist=%s&track=%s&autocorrect=1" % (urllib.quote(artist), urllib.quote(track))
        ret = getSourceCode(url)
    except urllib2.HTTPError:
        return None
    else:
        return xml.etree.ElementTree.XML(ret)

def getAlbumInfo(album, artist):
    try:
        print(album)
        print(artist)
        url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=b25b959554ed76058ac220b7b2e0a026&album=%s&artist=%s&autocorrect=1" % (urllib.quote(album), urllib.quote(artist))
        ret = getSourceCode(url)
    except urllib2.HTTPError:
        return None
    else:
        return xml.etree.ElementTree.XML(ret)
