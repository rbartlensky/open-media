class Observable(object):

    def __init__(self):
        self._observers = []

    def has_observer(self, observer):
        for obs in self._observers:
            if obs == observer:
                return False
        return True

    def add_observer(self, observer):
        if not self.has_observer(observer):
            self._observers.append(observer)

    def notify_observers(self, info):
        for obs in self._observers:
            obs.update(info)

class Observer(object):

    def __init__(self, observable):
        self.observable = observable

    def update(self, info):
        pass
