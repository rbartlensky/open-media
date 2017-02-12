from threading import Thread
import time


class PlayerThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self._keep_running = True

    def run(self):
        from .player import Player
        from . import player as event
        while self.keep_running:
            player = Player.instance()
            pos = player.get_current_second()
            # XXX this condition should be improved
            if player.is_playing() and abs(player.get_song_duration() - pos) <= 1:
                player.play_next()
            else:
                time.sleep(0.1)
                player.notify_observers(event.SLIDER_EVENT)

    @property
    def keep_running(self):
        return self._keep_running

    @keep_running.setter
    def keep_running(self, value):
        self._keep_running = value
