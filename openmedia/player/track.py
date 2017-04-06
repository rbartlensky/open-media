from audiotools import open, UnsupportedFile
import os


class Track(object):
    """
    This holds data about media files.

    The information about the media file associated with this includes
    the name, file path, duration and metadata.
    """

    def __init__(self, file_path):
        """
        Create a track using data from the specified file.

        Parameters
        ----------
        :param file_path: the path of the file out of which to create a track
        :type file_path: str
        """
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
        """
        The name of this track.

        :getter: Return this track's name.
        :type: str
        """
        return self._metadata.track_name

    @property
    def file_path(self):
        """
        The path of the file corresponding to this track.

        :getter: Return this track's file path.
        :type: str
        """

        return self._file_path

    @property
    def metadata(self):
        """
        The metadata associated with this track.

        :getter: Return this track's metadata.
        :type: Metadata
        """
        return self._metadata

    @property
    def duration(self):
        """
        The duration of this track.

        :getter: Return this track's duration.
        :type: int
        """
        return self._duration


class Metadata(object):
    """
    This generates and holds the name of the artist, the name of the track
    and the name of the album of a given mutagen file.

    :note:This should only be used by Track.
    """

    def __init__(self, mutFile):
        """
        Create and extracts metadata out of a mutagen file type.

        Parameters
        ----------
        :param mutFile: the mutagen file that will be used to extract metadata
        :type mutFile: a mutagen file object
        """
        self._artist_name = mutFile["TPE1"]
        self._album_name = mutFile["TALB"]
        self._track_name = mutFile["TIT2"]

    @property
    def artist_name(self):
        """
        The name of the artist as specified in the file's metadata.

        :getter: Return the file's artist name.
        :type: str
        """
        return self._artist_name

    @property
    def album_name(self):
        """
        The name of the album as specified in the file's metadata.

        :getter: Return the file's album name.
        :type: str
        """
        return self._album_name

    @property
    def track_name(self):
        """
        The name of the track as specified in the file's metadata.

        :getter: Return the file's track name.
        :type: str
        """
        return self._track_name
