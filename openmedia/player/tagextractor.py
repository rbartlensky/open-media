from gi.repository import Gst


class TagExtractor(object):

    def __init__(self, bus):
        bus.add_signal_watch()
        bus.connect("message::tag", self._extract)
        self.extracted = False
        self.title = self.artist = self.album = None

    def _extract(self, bus, message):
        if self.extracted is False:
            taglist = message.parse_tag()
            self.title = taglist.get_string(Gst.TAG_TITLE)
            self.artist = taglist.get_string(Gst.TAG_ARTIST)
            self.album = taglist.get_string(Gst.TAG_ALBUM)
            self.extracted = True

    def get_metadata(self):
        return (self.title, self.artist, self.album)
