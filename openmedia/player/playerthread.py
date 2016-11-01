from threading import Thread

import mixer
import time

class PlayerThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self._keep_running = True

    def run(self):
        while self.keep_running:
            pos = mixer.get_pos()
            if mixer.is_playing() and pos == -1:
                mixer.play_next()
            else:
                time.sleep(0.1)
                mixer.notify_observers(mixer.SLIDER_EVENT)

    @property
    def keep_running(self):
        return self._keep_running

    @keep_running.setter
    def keep_running(self, value):
        self._keep_running = value

