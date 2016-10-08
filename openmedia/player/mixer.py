from pygame import mixer
from track import Track
from playerthread import PlayerThread
from openmedia.observable.observable import Observable

import os

class InvalidVolumeError(Exception):
    pass

PLAY_EVENT, PAUSE_EVENT, STOP_EVENT,\
            NEXT_EVENT, SLIDER_EVENT = [index for index in xrange(5)]
track_list = []
curr_track_index, track_count, offset = -1, 0, 0
current_track = None
is_paused, is_stopped = False, False
player_thread = PlayerThread()
_observable = Observable()

def reset_values():
    global track_list, curr_track_index, track_count,\
           current_track, is_paused, is_stopped, offset,\
           player_thread, _observable
    track_list = []
    curr_track_index, track_count, offset = -1, 0, 0
    current_track = None
    is_paused, is_stopped = False, True
    _observable = Observable()
    player_thread = PlayerThread()

def init(song_list):
    global track_list, track_count, current_track
    reset_values()
    track_list = [Track(song) for song in song_list]
    mixer.init()
    set_volume(0.5)
    track_count = len(track_list)
    if track_count:
        current_track = _get_next_song()

def play(path=None):
    global track_count, is_paused, is_stopped, curr_track_index,\
           current_track, offset, player_thread, _observable
    if track_count:
        _observable.notify_observers(PLAY_EVENT)
        if path:
            curr_track_index = get_song_index(path)
            current_track = track_list[curr_track_index]
        if not is_paused or is_stopped:
            is_stopped = False
            offset = 0
            mixer.music.load(current_track.file_path)
            mixer.music.play()
            if not player_thread.isAlive():
                player_thread.start()
        else:
            is_paused = False
            is_stopped = False
            mixer.music.unpause()

def get_song_index(path):
    for idx, track in enumerate(track_list):
        if path == os.path.basename(track.file_path):
            return idx
    return None

def pause():
    global is_paused, _observable
    _observable.notify_observers(PAUSE_EVENT)
    if not is_paused:
        is_paused = True
        mixer.music.pause()

def stop():
    global is_paused, is_stopped, _observable
    _observable.notify_observers(STOP_EVENT)
    mixer.music.stop()
    is_paused = False
    is_stopped = True

def set_volume(volume):
    if volume >= 0.0 and volume <= 1.0:
        mixer.music.set_volume(volume)
    else:
        raise InvalidVolumeError(volume)

def play_next():
    global current_track, offset, _observable
    _observable.notify_observers(NEXT_EVENT)
    stop()
    offset = 0
    current_track = _get_next_song()
    play()

def _get_next_song():
    global track_list, curr_track_index, track_count
    if track_count:
        curr_track_index = (curr_track_index + 1) % track_count
        song = track_list[curr_track_index]
        return song
    else:
        return None

def get_song_duration():
    global current_track
    if current_track:
        return current_track.duration
    else:
        return 0

def add(track_path):
    global track_list, track_count
    track_count += 1
    track_list.append(Track(track_path))

def skip(amount):
    global offset
    duration = get_song_duration()
    if amount >= duration:
        play_next()
    else:
        offset = amount * 1000
        mixer.music.play(0, amount)

def get_pos():
    global offset, is_stopped
    pos = mixer.music.get_pos()
    if is_stopped:
        return 0
    elif pos == -1:
        return -1
    else:
        return pos + offset

def is_playing():
    global is_paused, is_stopped
    return not is_paused and not is_stopped

def add_observer(widget):
    global _observable
    _observable.add_observer(widget)

def notify_observers(event_type):
    global _observable
    _observable.notify_observers(event_type)
