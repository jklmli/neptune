import lastFM
import pandora

class Neptune:
    def __init__(self, artist, album, track, hasLyrics):
        self.album = album
        self.artist = artist
        self.track = track
        albumTree = lastFM.getAlbumInfo(self.album, self.artist)
        if albumTree != None:
            albumTree = albumTree.find('album')
            self.album = albumTree.find('name').text
            self.artist = albumTree.find('artist').text
            try:
                self.coverArtURL = albumTree.findall('image')[-1].text
            except AttributeError:
                pass
        trackTree = lastFM.getTrackInfo(self.artist, self.track)
        if trackTree != None:
            trackTree = trackTree.find('track')
            self.track = trackTree.find('name').text
            if self.artist == artist:
                self.artist = trackTree.find('artist').find('name').text
            if self.coverArtURL is None:
                try:
                    self.coverArtURL = trackTree.find('album').findall('image')[-1].text
                except AttributeError:
                    pass
        if hasLyrics is False:
            self.lyrics = pandora.getLyrics(self.artist, self.track)
        print(self.__dict__)