from gi.repository import Gst
from .track import Track
from .playerthread import PlayerThread
from openmedia.observable.observable import Observable

PLAY_EVENT, PAUSE_EVENT, STOP_EVENT,\
            NEXT_EVENT, SLIDER_EVENT = [index for index in range(5)]


class Player(Observable):
    _instance = None

    def __init__(self, song_list=[]):
        Observable.__init__(self)
        if Player._instance is None:
            Player._instance = self

        self.track_list = [Track(song) for song in song_list]
        self.curr_track_index = -1
        self.offset = 0
        if len(self.track_list):
            self.current_track = self._get_next_song()
        self.player_thread = PlayerThread()

        self.pipeline = Gst.Pipeline.new('main-pipeline')
        self.filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
        self.decoder = Gst.ElementFactory.make("decodebin", "oggdecoder")
        self.converter = Gst.ElementFactory.make("audioconvert", "convert")
        self.sink = Gst.ElementFactory.make("alsasink", "sink")
        self.volume = Gst.ElementFactory.make("volume", "volume")
        self.volume.set_property("volume", 0.5)

        self.pipeline.add(self.filesrc)
        self.pipeline.add(self.decoder)
        self.pipeline.add(self.converter)
        self.pipeline.add(self.volume)
        self.pipeline.add(self.sink)
        self.decoder.connect("pad-added", self._on_dyanmic_pad)

        self.filesrc.link(self.decoder)
        self.decoder.link(self.converter)
        self.converter.link(self.volume)
        self.volume.link(self.sink)

    @classmethod
    def instance(cls):
        return Player._instance

    def _on_dyanmic_pad(self, dbin, pad):
        pad.link(self.converter.get_static_pad("sink"))

    def play(self, path=None):
        if len(self.track_list):
            self.notify_observers(PLAY_EVENT)
            if path:
                self.pipeline.set_state(Gst.State.READY)
                self.curr_track_index = self.get_song_index(path)
                self.current_track = self.track_list[self.curr_track_index]
                self.filesrc.set_property("location",
                                          self.current_track.file_path)
                self.pipeline.set_state(Gst.State.PLAYING)
            if self.is_paused() and path is None:
                self.pipeline.set_state(Gst.State.PLAYING)
            else:
                self.pipeline.set_state(Gst.State.READY)
                self.offset = 0
                self.filesrc.set_property("location",
                                          self.current_track.file_path)
                self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(Gst.State.READY)
        self.notify_observers(STOP_EVENT)

    def pause(self):
        self.pipeline.set_state(Gst.State.PAUSED)
        self.notify_observers(PAUSE_EVENT)

    def is_playing(self):
        return self.pipeline.get_state(Gst.CLOCK_TIME_NONE)[1] == Gst.State.PLAYING

    def is_paused(self):
        return self.pipeline.get_state(Gst.CLOCK_TIME_NONE)[1] == Gst.State.PAUSED

    def get_song_index(self, path):
        for idx, track in enumerate(self.track_list):
            if path == track.file_path:
                return idx
        return None

    def play_next(self):
        if len(self.track_list):
            self.notify_observers(NEXT_EVENT)
            self.stop()
            self.offset = 0
            self.current_track = self._get_next_song()
            self.play()

    def get_song_duration(self):
        if self.current_track:
            return self.current_track.duration
        else:
            return 0

    def _get_next_song(self):
        if len(self.track_list):
            track_count = len(self.track_list)
            self.curr_track_index = (self.curr_track_index + 1) % track_count
            song = self.track_list[self.curr_track_index]
            return song
        else:
            return None

    def set_volume(self, volume):
        if volume >= 0.0 and volume <= 1.0:
            self.volume.set_property("volume", volume)

    def add(self, track_path):
        if track_path not in [track.file_path for track in self.track_list]:
            self.track_list.append(Track(track_path))

    def notify_observers(self, event_type):
        Observable.notify_observers(self, event_type)
