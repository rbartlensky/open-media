from pygame import mixer
from track import Track

class Mixer(object):

    def __init__(self, song_list):
        self.song_list = [Track(song) for song in song_list]
        mixer.init()
        self.current_song = song_list[0]
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
