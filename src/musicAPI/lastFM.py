import xml.etree.ElementTree
import urllib
import urllib2

from helper import getSourceCode
from musicAPI import lastFM_api_key

albumCache = {}
pictureCache = {}

def getPicture(url):
    if url in pictureCache:
        return pictureCache[url]
    (file, hdr) = urllib.urlretrieve(url)
    mimetype = hdr['Content-Type']
    data = open(file, 'rb').read()
    info = {    'mimetype':mimetype,
                'data':data         }
    pictureCache[url] = info
    return info

def getTrackInfo(track, artist):
    """
    Returns a dictionary with possible keys:
    'title', 'artist', 'album', 'trackPosition', 'picture'
    If no match found, returns empty dictionary
    """
    track = track.encode('utf-8')
    artist = artist.encode('utf-8')
    try:
        url = "http://ws.audioscrobbler.com/2.0/?method=track.getinfo&"
        url += urllib.urlencode(    {'api_key':lastFM_api_key,
                                     'artist':artist,
                                     'track':track,
                                     'autocorrect':1    }   )

        ret = getSourceCode(url)
    #except urllib2.HTTPError:
    except AttributeError:
        return {}
    else:
        info = {}
        #tree = xml.etree.ElementTree.XML(ret, parser=xml.etree.ElementTree.XMLParser(encoding='mbcs'))
        tree = xml.etree.ElementTree.XML(ret)
        if tree is not None:
            tree = tree.find('track')
            info['title'] = tree.find('name').text
            info['artist'] = tree.find('artist').find('name').text
            try:
                tree = tree.find('album')
                info['album'] = tree.find('title').text
                info['trackPosition'] = tree.attrib['position']
                info['picture'] = getPicture(tree.findall('image')[-1].text)
            except AttributeError:
                pass
        return info

def getAlbumInfo(album, artist):
    """
    Returns a dictionary with possible keys:
    'album', 'artist', 'picture', 'totalTracks'
    If no match found, returns empty dictionary
    """
    if (album, artist) in albumCache:
        return albumCache[(album,artist)]

    album = album.encode('utf-8')
    artist = artist.encode('utf-8')
    try:
        url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&"
        url += urllib.urlencode(    {'api_key':lastFM_api_key,
                                     'album':album,
                                     'artist':artist,
                                     'autocorrect':1}   )
        ret = getSourceCode(url)
    except urllib2.HTTPError:
        return {}
    else:
        info = {}
        tree = xml.etree.ElementTree.XML(ret)
        if tree is not None:
            tree = tree.find('album')
            info['album'] = tree.find('name').text
            info['artist'] = tree.find('artist').text
            try:
                info['picture'] = getPicture(tree.findall('image')[-1].text)
            except AttributeError:
                pass
            tree = tree.find('tracks')
            info['totalTracks'] = str(len(list(tree)))
            albumCache[(album,artist)] = info
        return info
