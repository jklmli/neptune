# Copyright (C) 2011 598074 (http://github.com/598074)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import os
import sys

import mutagen

from music_apis import lastfm, pandora
from song import Song
import util

def tagSong(root, location):
    try:
        song = Song(location)
    except mutagen.id3.ID3NoHeaderError:
        return

    info = {}
    if song.tags['title'][0] and song.tags['artist'][0]:
        trackInfo = lastfm.getTrackInfo(song.tags['title'][0], song.tags['artist'][0])
    if trackInfo:
        if 'album' in trackInfo:
            song.tags['album'] = trackInfo['album']
            song.tags.save()
        info.update(trackInfo)

    if song.tags['album'][0] and song.tags['artist'][0]:
        albumInfo = lastfm.getAlbumInfo(song.tags['album'][0], song.tags['artist'][0])
    if albumInfo:
        info.update(albumInfo)

    try:
        info['tracknumber'] = '%s/%s' % (info['trackPosition'], info['totalTracks'])
    except KeyError:
        pass
    for tag in ['trackPosition', 'totalTracks']:
        if tag in info:
            del info[tag]

    print [(k,v) for (k,v) in info.items() if k != 'picture']

    for tag in info:
        if info[tag]:
            song.tags[tag] = info[tag]

    lyrics = pandora.getLyrics(song.tags['artist'][0], song.tags['title'][0])
    if lyrics:
        song.tags['lyrics'] = lyrics

    artist = util.cleanPath(song.tags['artist'][0])
    album = util.cleanPath(song.tags['album'][0])
    title = util.cleanPath(song.tags['title'][0])

    song.save()

    # fixes for Unicode encoding in system filenames into UTF-8
    # INFO: http://docs.python.org/library/sys.html
    location = location.decode(sys.getfilesystemencoding())
    root = root.decode(sys.getfilesystemencoding())

    extension = os.path.splitext(location)[1]
    newLocation = os.path.join(root, artist, album, title + extension)
#    print(location)
#    print(location + 'x')
#    print(newLocation)
    if os.path.exists(newLocation) is False or os.path.abspath(location) == os.path.abspath(newLocation) is False or location != newLocation:
        # workaround for inability to rename to already existing file (i.e. case-sensitiviy)
        os.renames(location, location + 'x')
        os.renames(location + 'x', newLocation)

def tagDirectory(root):
    i = 1
    for dir, subdirs, files in os.walk(root, topdown=False):
        for name in files:
            print(i)
            tagSong(root, os.path.join(dir, name))
            i += 1

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