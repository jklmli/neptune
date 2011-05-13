import lastFM
import pandora

class Neptune:
    def __init__(self, artist, album, track):
        self.artist = artist
        self.album = album
        self.track = track
        foundInfo = False
        albumTree = lastFM.getAlbumInfo(self.album, self.artist)
        if albumTree is not None:
            foundInfo = True
            albumTree = albumTree.find('album')
            self.album = albumTree.find('name').text
            self.artist = albumTree.find('artist').text
            try:
                self.coverArtURL = albumTree.findall('image')[-1].text
            except AttributeError:
                pass
        trackTree = lastFM.getTrackInfo(self.artist, self.track)
        if trackTree is not None:
            trackTree = trackTree.find('track')
            self.track = trackTree.find('name').text
            if foundInfo is False:
                # already found artist/coverArtURL
                self.artist = trackTree.find('artist').find('name').text
                try:
                    trackTree = trackTree.find('album')
                    self.album = trackTree.find('title').text
                    self.coverArtURL = trackTree.findall('image')[-1].text
                except AttributeError:
                    pass
        self.lyrics = pandora.getLyrics(self.artist, self.track)