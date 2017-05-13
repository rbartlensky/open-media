import os.path
from gi.repository import Gst, GstPbutils


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
        self._file_path = os.path.abspath(file_path)
        self._metadata = {}
        discoverer_info = self._get_discoverer_info(self._file_path)
        tags = discoverer_info.get_tags()
        if tags.get_string(Gst.TAG_TITLE)[0]:
            self._metadata['title'] = tags.get_string(Gst.TAG_TITLE)[1]
        else:
            self._metadata['title'] = 'untitled'
        if tags.get_sample(Gst.TAG_IMAGE)[0]:
            self._metadata['image'] = tags.get_sample(Gst.TAG_IMAGE)[1]
        else:
            self._metadata['image'] = os.path.abspath('./openmedia/gui/res/img/no_image.png')
        self._duration = discoverer_info.get_duration() / Gst.SECOND


    def _get_discoverer_info(self, file_path):
        Gst.init()
        discoverer = GstPbutils.Discoverer()
        return discoverer.discover_uri("file://" + file_path)

    @property
    def name(self):
        """
        The name of this track.

        :getter: Return this track's name.
        :type: str
        """
        return self._metadata['title']

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

        The metadata is a dictionary mapping tags to values.

        :getter: Return this track's metadata.
        :type: dict
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
