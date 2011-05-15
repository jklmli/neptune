import os
import urllib

import helper
import musicAPI.lastFM
import musicAPI.pandora
from song import Song

import mutagen
from mutagen.id3 import TIT2, TPE1, TALB, USLT, APIC

def tagSong(root, location):
    try:
        song = Song(location)
    except mutagen.id3.ID3NoHeaderError:
        return

    if album is not None:
        testAndRemoveTag(tags, 'TALB', framesToReplace)
        tags.add(TALB(encoding=3, text=album.encode('utf-8')))
    if artist is not None:
        testAndRemoveTag(tags, 'TPE1', framesToReplace)
        tags.add(TPE1(encoding=3, text=artist.encode('utf-8')))
    if track is not None:
        testAndRemoveTag(tags, 'TIT2', framesToReplace)
        tags.add(TIT2(encoding=3, text=track.encode('utf-8')))
    if coverArtURL is not None:
        testAndRemoveTag(tags, 'APIC', framesToReplace)
        (file, hdr) = urllib.urlretrieve(coverArtURL)
        mimetype = hdr['Content-Type']
        rawData = open(file, 'rb').read()
        tags.add(APIC(encoding=3, mime=mimetype, type=3, desc='Cover'.encode('utf-8'), data = rawData))
    # want to check after we start removing the empty directories - no point in dl'ing the same image over+over again
    """
        tags.add(
                APIC(
                encoding=3, # 3 is for utf-8
                mime='image/png', # image/jpeg or image/png
                type=3, # 3 is for the cover image
                desc=u'Cover',
                data=open('example.png').read()
            )
        )
    """
    lyrics = pandora.getLyrics(taggedArtist, taggedTrack)
    if lyrics is not None:
        testAndRemoveTag(tags, 'USLT', framesToReplace)
        if 'TLAN' in tags:
            # TODO: Not that this assumes tags['TLAN] is valid
            language = tags['TLAN']
        else:
            language = 'eng'.encode('utf-8')
        tags.add(USLT(encoding=3, lang=language, desc='desc'.encode('utf-8'), text=lyrics))

    tags.save()

    artist = helper.cleanPath(artist)
    album = helper.cleanPath(album)
    track = helper.cleanPath(track)

    extension = os.path.splitext(location)[1]
    newLocation = os.path.join(root, artist, album, track, extension)
    print(location.encode('utf-8'))
    print(location.encode('utf-8') + 'x')
    print(newLocation.encode('utf-8'))
    if os.path.exists(newLocation) is False or os.path.abspath(location) == os.path.abspath(newLocation) is False or location != newLocation:
        # workaround for inability to rename to already existing file (i.e. case-sensitiviy)
        os.renames(location, location + 'x')
        os.renames(location + 'x', newLocation)

def tagDirectory(root):
    i = 0
    for dir, subdirs, files in os.walk(root, topdown=False):
        for name in files:
            tagSong(root, os.path.join(dir, name))
            i += 1
            print(i)
    # appears to be unneeded since os.renames does all this auto.
    """
        for name in subdirs:
            currDir = os.path.join(dir, name)
            if os.listdir(currDir) == []:
                try:
                    os.rmdir(currDir)
                except OSError:
                    # need error message here in case of permission error
                    pass
    """

