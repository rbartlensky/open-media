from audiotools import open, UnsupportedFile
import os


class Track(object):

    def __init__(self, file_path):
        self._file_path = os.path.expanduser(file_path)
        try:
            track_file = open(self.file_path)
            self._duration = float(track_file.seconds_length())
            self._metadata = track_file.get_metadata()
        except UnsupportedFile:
            if file_path.endswith(".mp3"):
                from mutagen import File
                track_file = File(self.file_path)
                self._metadata = Metadata(track_file)
                self._duration = track_file.info.length
            else:
                self._duration = 0
                self._metadata = None

    @property
    def name(self):
        return self._metadata.track_name

    @property
    def file_path(self):
        return self._file_path

    @property
    def metadata(self):
        return self._metadata

    @property
    def duration(self):
        return self._duration


class Metadata(object):

    def __init__(self, mutFile):
        self._artist_name = mutFile["TPE1"]
        self._album_name = mutFile["TALB"]
        self._track_name = mutFile["TIT2"]

    @property
    def artist_name(self):
        return self._artist_name

    @property
    def album_name(self):
        return self._album_name

    @property
    def track_name(self):
        return self._track_name
