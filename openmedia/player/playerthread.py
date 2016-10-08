from threading import Thread

import mixer
import time

class PlayerThread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while not mixer.is_stopped:
            pos = mixer.get_pos()
            mixer.notify_observers(mixer.SLIDER_EVENT)
            if mixer.is_playing() and pos == -1:
                mixer.play_next()
