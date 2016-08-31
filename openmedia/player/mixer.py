from pygame import mixer
from track import Track
import os

class InvalidVolumeError(Exception):
    pass

track_list = []
song_index = 0
total_tracks = 0
current_song = None
is_paused = False
is_stopped = False

def init(song_list):
    global track_list, song_index, total_tracks, current_song, is_paused
    track_list = [Track(song) for song in song_list]
    mixer.init()
    song_index = 0
    total_tracks = len(track_list)
    current_song = _get_next_song()
    is_paused = False

def play(filename=None):
    global is_paused, is_stopped, current_song
    if filename:
        current_song = get_song(filename)
    if not is_paused or is_stopped:
        is_stopped = False
        mixer.music.load(current_song.get_path())
        mixer.music.play()
    else:
        is_paused = False
        is_stopped = False
        mixer.music.unpause()

def get_song(filename):
    for track in track_list:
        if filename == os.path.basename(track.get_path()):
            return track
    return None

def pause():
    global is_paused
    if not is_paused:
        is_paused = True
        mixer.music.pause()

def stop():
    global is_paused, is_stopped
    mixer.music.stop()
    is_paused = False
    is_stopped = True

def set_volume(volume):
    if volume >= 0.0 and volume <= 1.0:
        mixer.music.set_volume(volume)
    else:
        raise InvalidVolumeError(volume)

def play_next():
    global current_song
    stop()
    current_song = _get_next_song()
    play()

def _get_next_song():
    global track_list, song_index, total_tracks
    song = track_list[song_index]
    song_index = (song_index + 1) % total_tracks
    return song

def get_song_duration():
    global current_song
    return current_song.duration

def add(track_path):
    global track_list, total_tracks
    total_tracks += 1
    track_list.append(Track(track_path))
