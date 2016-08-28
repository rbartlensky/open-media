from pygame import mixer
from track import Track

class InvalidVolumeError(Exception):
    pass

class Mixer(object):

    def __init__(self, song_list):
        self.song_list = [Track(song) for song in song_list]
        self.song_list.reverse()
        mixer.init()
        self.current_song = self._get_next_song()
        self.is_paused = False

    def play(self):
        if not self.is_paused:
            mixer.music.load(self.current_song.get_path())
            mixer.music.play()
        else:
            self.is_paused = False
            mixer.music.unpause()

    def pause(self):
        if not self.is_paused:
            self.is_paused = True
            mixer.music.pause()

    def stop(self):
        mixer.music.stop()

    def set_volume(volume):
        if volume >= 0.0 and volume <= 1.0:
            mixer.set_volume(volume)
        else:
            raise InvalidVolumeError(volume)

    def play_next():
        self.current_song = self._get_next_song()

    def _get_next_song():
        old = self.song_list.pop()
        self.song_list.push(old)
        return old
