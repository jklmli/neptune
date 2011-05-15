import mutagen
from mutagen.easyid3 import EasyID3

class Song:
	#wiping TXXX wipes replaygain calc.
	def __init__(self, location,
					tagsToReplace=['album', 'artist', 'track', 'picture'],
					tagsToWipe=['comments', 'URL']):
		try:
			self.tags = EasyID3(location)
			self.tagsToReplace = tagsToReplace
			self.tagsToWipe = tagsToWipe
			self.location = location
		except mutagen.id3.ID3NoHeaderError:
			# this isn't an audio file!
			raise
		for frame in tagsToWipe:
			self.tags.delall(frame)
			self.save()
		self.album = self.tags['album']
		artist = self.tags['TPE1'.encode('utf-8')].text
		track = self.tags['TIT2'.encode('utf-8')].text

	def __getter__(self, key):
		return self.tags[map[key]]

	def __setter__(self, key, value):
		if key in self.tagsToReplace:
			tags.delall(frameName)
			tags[map[key]] = value

	def removeAll(self, frameName, framesToDelete):
		if frameName in framesToDelete:
			id3File.delall(frameName)

		def save(self):
			self.tags.save(self.location)

