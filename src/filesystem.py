import os
import shutil

from helper import unescape
from neptune import Neptune

import mutagen
from mutagen.id3 import ID3, TIT2, TPE1, TALB, USLT, APIC

def fixSong(root, location):
    # root should end in a path seperator
    try:
        tags = ID3(location)
    except mutagen.id3.ID3NoHeaderError:
        # this isn't an audio file!
        return
    album = tags['TALB'.encode('utf-8')].text[0]
    artist = tags['TPE1'.encode('utf-8')].text[0]
    track = tags['TIT2'.encode('utf-8')].text[0]

    newTags = Neptune(artist, album, track)

    if newTags.album is not None:
        tags['TALB'.encode('utf-8')] = TALB(encoding=3, text=(newTags.album).encode('utf-8'))
    if newTags.artist is not None:
        tags['TPE1'.encode('utf-8')] = TPE1(encoding=3, text=(newTags.artist).encode('utf-8'))
    if newTags.track is not None:
        tags['TIT2'.encode('utf-8')] = TIT2(encoding=3, text=(newTags.track).encode('utf-8'))
    if newTags.coverArtURL is not None:
        pass
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
    if newTags.lyrics is not None:
        tags["USLT::'eng'".encode('utf-8')] = USLT(encoding=3, lang='eng'.encode('utf-8'), desc='desc'.encode('utf-8'), text=newTags.lyrics)

    tags.save()


    extension = os.path.splitext(location)[1]
    newLocation = '%s/%s/%s/%s%s' % (root, unescape(newTags.artist), unescape(newTags.album), unescape(newTags.track), extension)
    print(location.encode('utf-8'))
    print(location.encode('utf-8') + 'x')
    print(newLocation.encode('utf-8'))
    if os.path.exists(newLocation) is False or os.path.abspath(location) == os.path.abspath(newLocation) is False or location != newLocation:
        # workaround for inability to rename to already existing file (i.e. case-sensitiviy)
        os.renames(location, location + 'x')
        os.renames(location + 'x', newLocation)

def removeEmptyDirectories(root):
    for dir, subdirs, files in os.walk(root):
        if len(subdirs) == 0 and len(files == 0):
            shutil.rmtree(dir)

def fixDirectory(root):
    i = 0
    for dir, subdirs, files in os.walk(root, topdown=False):
        for name in files:
            fixSong(root, os.path.join(dir, name))
            i += 1
            print(i)
        for name in subdirs:
            currDir = os.path.join(dir, name)
            if os.listdir(currDir) == []:
                try:
                    os.rmdir(currDir)
                except OSError:
                    # need error message here in case of permission error
                    pass


