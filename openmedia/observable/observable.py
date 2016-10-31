import threading
import gi
from gi.repository import GLib

class Observable(object):

    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, info):
        for obs in self._observers:
            event = threading.Event()
            GLib.idle_add(obs.update, event, info)

class Observer(object):

    def __init__(self):
        pass

    def update(self, event, info):
        return False
