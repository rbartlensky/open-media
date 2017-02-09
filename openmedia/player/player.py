from gi.repository import Gst
from .track import Track
from .playerthread import PlayerThread
from openmedia.observable.observable import Observable

PLAY_EVENT, PAUSE_EVENT, STOP_EVENT,\
            NEXT_EVENT, SLIDER_EVENT = [index for index in range(5)]


class Player(Observable):

    def __init__(self, song_list):

        Observable.__init__(self)

        self.track_list = [Track(song) for song in song_list]
        self.curr_track_index = -1
        self.track_count = len(self.track_list)
        self.offset = 0
        self.current_track = self.track_list[0]
        self.player_thread = PlayerThread()

        self.pipeline = Gst.Pipeline.new('main-pipeline')
        self.filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
        self.decoder = Gst.ElementFactory.make("decodebin", "oggdecoder")
        self.converter = Gst.ElementFactory.make("audioconvert", "convert")
        self.sink = Gst.ElementFactory.make("alsasink", "sink")

        self.pipeline.add(self.filesrc)
        self.pipeline.add(self.decoder)
        self.pipeline.add(self.converter)
        self.pipeline.add(self.sink)
        self.decoder.connect("pad-added", self._on_dyanmic_pad)

        self.filesrc.link(self.decoder)
        self.decoder.link(self.converter)
        self.converter.link(self.sink)

    def _on_dyanmic_pad(self, dbin, pad):
        pad.link(self.converter.get_static_pad("sink"))

    def play(self, path=None):
        if self.track_count:
            self.notify_observers(PLAY_EVENT)
            if path:
                self.curr_track_index = self.get_song_index(path)
            if False and self.pipeline.get_state(0)[1] == Gst.State.PAUSED and\
               path is None:
                pass
            else:
                self.offset = 0
                self.filesrc.set_property("location",
                                          self.current_track.file_path)
                if not self.player_thread.isAlive():
                    self.player_thread.start()
            self.pipeline.set_state(Gst.State.PLAYING)

    def get_song_index(self, path):
        for idx, track in enumerate(self.track_list):
            if path == track.file_path:
                return idx
        return None
