from gi.repository import Gst
from .track import Track
from .playerthread import PlayerThread
from openmedia.observable.observable import Observable

PLAY_EVENT, PAUSE_EVENT, STOP_EVENT,\
            NEXT_EVENT, SLIDER_EVENT = [index for index in range(5)]


class Player(Observable):
    """
    This is a singleton class that provides ways of manipulating the playback of multiple
    media files.

    This provides a way to play, pause, stop the playback of multiple media files and also
    increase/decrease the speed of the playback.

    This will contain a list of media files and new files can be added during the
    playback of any media.
    """
    _instance = None

    def __init__(self, song_list=[]):
        """
        Create a player which will contain a list of media that will be playable.

        :note: Use the instance method instead of instantiating a player directly.

        :param song_list: the file paths to be added to the playlist
        :type song_list: list
        """
        Observable.__init__(self)
        if Player._instance is None:
            Player._instance = self

        self._shuffle = False
        self.track_list = [Track(song) for song in song_list]
        self.curr_track_index = -1
        self.speed = 1.0
        if len(self.track_list):
            self.current_track = self._get_next_media()
        self.player_thread = PlayerThread()

        self.pipeline = Gst.Pipeline.new('main-pipeline')
        self.filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
        self.decoder = Gst.ElementFactory.make("decodebin", "decoder")
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

    @property
    def shuffle(self):
        """
        Whether or not the playlist is shuffled.

        :getter: Returns True if the playlist is shuffled, False otherwise.
        :setter: Sets whether or not the playlist is shuffled.
        :type: bool
        """
        return self._shuffle

    @shuffle.setter
    def shuffle(self, value):
        self._shuffle = value

    @classmethod
    def instance(cls):
        """
        Return the unique instance of the Player class.

        :returns: Player -- the unique instance of Player
        """
        return Player._instance

    def _on_dyanmic_pad(self, dbin, pad):
        pad.link(self.converter.get_static_pad("sink"))

    def play(self, path=None):
        """
        Set the player state to 'playing'.

        Play the current selected song, the first song if none are selected or
        the song with the file path that is specified by the given parameter.
        If the current selected media is paused, the playback will continue
        from the second at which the media was last paused.

        :note: The path parameter must specify a file name that is part of the\
        playlist of the player.

        :param path: the file path of the song to be played
        :type path: str
        """
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
            if not self.player_thread.isAlive():
                self.player_thread.start()

    def stop(self):
        """
        Stop the player, if it is playing.
        """
        self.pipeline.set_state(Gst.State.READY)
        self.notify_observers(STOP_EVENT)

    def pause(self):
        """
        Pause the player, if it is playing.
        """
        self.pipeline.set_state(Gst.State.PAUSED)
        self.notify_observers(PAUSE_EVENT)

    def is_playing(self):
        """
        Return True if the player is playing, False otherwise.
        :returns: bool
        """
        return self.pipeline.get_state(Gst.CLOCK_TIME_NONE)[1] \
            == Gst.State.PLAYING

    def is_paused(self):
        """
        Return True if the player is paused, False otherwise.
        :returns: bool
        """
        return self.pipeline.get_state(Gst.CLOCK_TIME_NONE)[1] \
            == Gst.State.PAUSED

    def is_stopped(self):
        """
        Return True if the player is stopped, False otherwise.
        :returns: bool
        """
        return self.pipeline.get_state(Gst.CLOCK_TIME_NONE)[1] \
            == Gst.State.READY

    def get_song_index(self, path):
        """
        Return the index in the playlist of the specified media.

        :param path: the path of the media whose index to return
        :type path: str
        """
        for idx, track in enumerate(self.track_list):
            if path == track.file_path:
                return idx
        return None

    def play_next(self):
        """
        Play the next media in the playlist.
        """
        if len(self.track_list):
            self.notify_observers(NEXT_EVENT)
            self.stop()
            self.offset = 0
            self.current_track = self._get_next_media()
            self.play()

    def play_previous(self):
        """
        Play the previous media in the playlist.
        """
        if len(self.track_list):
            self.notify_observers(NEXT_EVENT)
            self.stop()
            self.offset = 0
            self.current_track = self._get_prev_media()
            self.play()

    def skip(self, amount):
        """
        Skip the specified number of nanoseconds into the media currently
        playing. Play the next track if the amount to be skipped exceeds
        the media duration.

        :param amount: the number of nanoseconds to skip
        :type amount: int
        :note: this should only be called while the player is playing
        """
        duration = self.get_song_duration()
        if amount >= duration:
            self.play_next()
        else:
            offset = amount * Gst.SECOND
            self.play()
            while not self.is_playing():
                # wait for the pipeline to start playing
                pass
            self.pipeline.seek_simple(Gst.Format.TIME,
                                      Gst.SeekFlags.FLUSH,
                                      offset)
            self.notify_observers(PLAY_EVENT)

    def get_song_duration(self):
        """
        Return the duration of the song currently being played.

        :returns: int
        :note: this returns 0 if there is no media playing when this is called.
        """
        if self.current_track:
            return self.current_track.duration
        else:
            return 0

    def _get_next_media(self):
        if len(self.track_list):
            track_count = len(self.track_list)
            if self._shuffle:
                import random
                self.curr_track_index = random.randint(0, track_count - 1)
            else:
                self.curr_track_index = (self.curr_track_index + 1) % track_count
            song = self.track_list[self.curr_track_index]
            return song
        else:
            return None

    def _get_prev_media(self):
        if len(self.track_list):
            track_count = len(self.track_list)
            if self._shuffle:
                import random
                self.curr_track_index = random.randint(0, track_count - 1)
            else:
                self.curr_track_index = (track_count + self.curr_track_index - 1) % track_count
            song = self.track_list[self.curr_track_index]
            return song
        else:
            return None

    def set_volume(self, volume):
        """
        Set the playback volume.

        :param volume: the new playback volume
        :type volume: float
        :note: the volume needs to be a value between 0.0 and 1.0
        """
        if volume >= 0.0 and volume <= 1.0:
            self.volume.set_property("volume", volume)

    def add(self, track_path):
        """
        Create a Track object with the given path and add it to the
        track list.

        :param track_path: the path to the track that will be added to the\
        list of tracks
        :type track_path: str
        """
        if track_path not in [track.file_path for track in self.track_list]:
            self.track_list.append(Track(track_path))
            return True
        return False

    def get_current_second(self):
        """
        Return the number of seconds the current track has been playing for.

        :returns: int -- the number of seconds
        """
        return self.pipeline.query_position(Gst.Format.TIME)[1] / Gst.SECOND

    def notify_observers(self, event_type):
        Observable.notify_observers(self, event_type)

    def increase_playback_speed(self):
        """
        Increase the playback speed of the current playing track by 0.10 (10 percent).

        :note: This will not increase the speed of the track if the current playback\
        speed is greater or equal to 2.5 (250 percent).
        """
        if self.speed <= 2.5:
            self.speed += 0.10
            self._set_speed()

    def decrease_playback_speed(self):
        """
        Decrease the playback speed of the current playing track by 0.10 (10 percent).

        :note: This will not decrease the speed of the track if the current playback\
        speed is less or equal to 0.20 (20 percent).
        """
        if self.speed >= 0.20:
            self.speed -= 0.10
            self._set_speed()

    def _set_speed(self):
        self.pipeline.set_state(Gst.State.PAUSED)
        event = Gst.Event.new_seek(self.speed,
                                   Gst.Format.TIME,
                                   (Gst.SeekFlags.FLUSH |
                                    Gst.SeekFlags.ACCURATE),
                                   Gst.SeekType.SET,
                                   self.get_current_second() * Gst.SECOND,
                                   Gst.SeekType.SET,
                                   -1)
        self.sink.send_event(event)
        self.pipeline.set_state(Gst.State.PLAYING)
