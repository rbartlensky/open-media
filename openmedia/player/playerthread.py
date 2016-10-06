from threading import Thread
import mixer

import time

class PlayerThread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            pos = mixer.get_pos()
            if mixer.is_playing() and pos == -1:
                mixer.play_next()
            elif mixer.is_paused and pos != -1:
                pass
            elif mixer.is_stopped:
                break
