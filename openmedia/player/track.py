from audiotools import open, UnsupportedFile
import mutagen
import os

class Track(object):

    def __init__(self, file_path):
        self.file_path = os.path.expanduser(file_path)
        try:
            self.track_file = open(self.file_path)
            self.duration = float(self.track_file.seconds_length())
            self.metadata = self.track_file.get_metadata()
        except UnsupportedFile:
            if file_path.endswith(".mp3"):
                from mutagen.mp3 import MP3, MPEGInfo
                from mutagen import File
                self.track_file = File(self.file_path)
                self.metadata = Metadata(self.track_file)
                self.duration = self.track_file.info.length
            else:
                self.duration = 0
                self.metadata = None

class Metadata(object):

    def __init__(self, mutFile):
        self.artist_name = mutFile["TPE1"]
        self.album_name = mutFile["TALB"]
        self.track_name = mutFile["TIT2"]
