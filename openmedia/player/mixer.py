from gi.repository import Gst
from .track import Track
from .playerthread import PlayerThread
from openmedia.observable.observable import Observable


class InvalidVolumeError(Exception):
    pass

PLAY_EVENT, PAUSE_EVENT, STOP_EVENT,\
            NEXT_EVENT, SLIDER_EVENT = [index for index in range(5)]

pipeline = Gst.Pipeline.new('main-pipeline')
filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
decoder = Gst.ElementFactory.make("decodebin", "mp3decoder")


track_list = []
curr_track_index, track_count, offset = -1, 0, 0
current_track = None
is_paused, is_stopped = False, True
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
    global track_list, track_count, current_track, pipeline, filesrc,\
            decoder
    pipeline.add(filesrc)
    pipeline.add(decoder)
    filesrc.link(decoder)
    convert = Gst.ElementFactory.make("audioconvert", "convert")
    pipeline.add(convert)
    sink = Gst.ElementFactory.make("alsasink", "sink")
    pipeline.add(sink)
    convert.link(sink)
    decoder.link(convert)
    track_list = [Track(song) for song in song_list]
    #if len(track_list) > 0:
    #    filesrc.set_property("location", track_list[0].file_path)

def play(path=None):
    global track_count, is_paused, is_stopped, curr_track_index,\
           current_track, offset, player_thread, _observable, pipeline, filesrc
    if len(track_list) > 0:
        print("playing?")
        filesrc.set_property("location", track_list[0].file_path)
        pipeline.set_state(Gst.State.PLAYING)

def get_song_index(path):
    for idx, track in enumerate(track_list):
        if path == track.file_path:
            return idx
    return None


def pause():
    global is_paused
    if not is_paused:
        is_paused = True
        notify_observers(PAUSE_EVENT)


def stop():
    global is_paused, is_stopped
    is_paused = False
    is_stopped = True
    notify_observers(STOP_EVENT)
    #mixer.music.stop()


def set_volume(volume):
    if volume >= 0.0 and volume <= 1.0:
        pass
    else:
        raise InvalidVolumeError(volume)


def play_next():
    global current_track, offset
    if track_count:
        notify_observers(NEXT_EVENT)
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
    global offset, is_paused, is_stopped
    duration = get_song_duration()
    if amount >= duration:
        play_next()
    else:
        offset = amount * 1000
        if is_paused or is_stopped:
            is_paused = False
            if is_stopped:
                if not player_thread.isAlive():
                    player_thread.start()
                is_stopped = False
        notify_observers(PLAY_EVENT)


def get_pos():
    global offset, is_stopped
    pos = 1
    if is_stopped:
        return 0.0
    elif pos == -1:
        return -1.0
    else:
        return float(pos + offset)


def is_playing():
    global is_paused, is_stopped, pipeline
    return not is_paused and not is_stopped
    #return pipeline.get_state() == Gst.State.PLAYING

def add_observer(widget):
    global _observable
    _observable.add_observer(widget)


def notify_observers(event_type):
    global _observable
    _observable.notify_observers(event_type)
