import urllib

import mutagen
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from compatid3 import CompatID3

def picture_get(id3, key):
	pics = [frame.data for frame in id3.getall('APIC')]
	if pics:
		return pics
	else:
		raise EasyID3KeyError(key)

def picture_set(id3, key, value):
	(file, hdr) = urllib.urlretrieve(value[0])
	mimetype = hdr['Content-Type']
	rawData = open(file, 'rb').read()
	id3.add(mutagen.id3.APIC(encoding=3, mime=mimetype, type=3, desc='Cover (front)', data = rawData))

def picture_delete(id3, key):
	id3.delall('APIC')

def picture_list():
	return

def lyrics_get(id3, key):
	lyrics = [frame.text for frame in id3.getall('USLT')]
	if lyrics:
		return lyrics
	else:
		raise EasyID3KeyError(key)

def lyrics_set(id3, key, value):
	try:
		language = id3['language']
	except KeyError:
		language = 'eng'
	id3.add(mutagen.id3.USLT(encoding=3, lang=language, desc='desc', text=value[0]))

def lyrics_delete(id3, key):
	id3.delall('USLT')

def lyrics_list():
	return

EasyID3.RegisterKey('picture', getter=picture_get, setter=picture_set, deleter=picture_delete, lister = picture_list)
#EasyID3.RegisterKey('comments', getter=comments_get, setter=comments_set, deleter=comments_delete, lister = comments_list)
EasyID3.RegisterKey('lyrics', getter=lyrics_get, setter=lyrics_set, deleter=lyrics_delete, lister = lyrics_list)
EasyID3.RegisterTextKey('language', 'TLAN')

class IrreplaceableKeyError(Exception):
		def __init__(self, msg):
			self.msg = msg
		def __str__(self):
			return repr(self.msg)

class Song:
	#wiping TXXX wipes replaygain calc.
	def __init__(self, location,
					tagsToReplace=['album', 'artist', 'title', 'tracknumber', 'picture'],
					# future tags: comments/COMM, url/WXXX
					tagsToWipe=[]):
		try:
			self.tags = EasyID3(location)
			self.tagsToReplace = tagsToReplace
			self.location = location
			self.newTags = EasyID3()
		except mutagen.id3.ID3NoHeaderError:
			# this isn't an audio file!
			raise
		for frame in tagsToWipe:
			self.tags.delall(frame)
			self.save()

	def __setitem__(self, key, value):
		if key in self.tagsToReplace:
			self.tags.delall(key)
			self.tags[key] = value
		else:
			raise IrreplaceableKeyError(key)

	def save(self):
		self.tags.save(filename=self.location)
		self.tags = CompatID3(self.location)
		self.tags.update_to_v23()
		self.tags.save(filename=self.location, v2=3)