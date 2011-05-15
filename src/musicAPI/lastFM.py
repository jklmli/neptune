import xml.etree.ElementTree
import urllib
import urllib2

from helper import getSourceCode
from musicAPI import lastFM_api_key

def getTrackInfo(track, artist):
    try:
        url = "http://ws.audioscrobbler.com/2.0/?method=track.getinfo&"
        url += urllib.urlencode(dict(api_key=lastFM_api_key, artist=artist, track=track, autocorrect=1))
        ret = getSourceCode(url)
    except urllib2.HTTPError:
        return None
    else:
        info = {}
        tree = xml.etree.ElementTree.XML(ret)
        if tree is not None:
            tree = tree.find('track')
            info['track'] = tree.find('name').text
            info['artist'] = tree.find('artist').find('name').text
            try:
                tree = tree.find('album')
                info['album'] = tree.find('title').text
                info['trackNumber'] = tree.attrib['position']
                info['coverArtURL'] = tree.findall('image')[-1].text
            except AttributeError:
                pass
        return info

def getAlbumInfo(album, artist):
    try:
        print(album)
        print(artist)
        url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&"
        url += urllib.urlencode(dict(api_key=lastFM_api_key, album=album, artist=artist, autocorrect=1))
        ret = getSourceCode(url)
    except urllib2.HTTPError:
        return None
    else:
        info = {}
        tree = xml.etree.ElementTree.XML(ret)
        if tree is not None:
            tree = tree.find('album')
            info['album'] = tree.find('name').text
            info['artist'] = tree.find('artist').text
            try:
                info['coverArtURL'] = tree.findall('image')[-1].text
            except AttributeError:
                pass
            tree = tree.find('tracks')
            info['totalTracks'] = str(len(tree))
        return info
