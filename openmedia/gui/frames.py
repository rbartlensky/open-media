# -*- coding: utf-8 -*-

import gi
from gi.repository import Gtk
from openmedia.player import mixer
from openmedia.observable.observable import Observer

class InvalidWidgetStateException(Exception):
    pass

class PlayerFrame(Gtk.Window, Observer):
    def __init__(self):
        Gtk.Window.__init__(self, title="open-media")
        Observer.__init__(self)
        self.connect("delete-event", self.halt)
        self.set_border_width(10)
        mixer.add_observer(self)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)

        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        hbox.set_spacing(5)
        hbox.set_hexpand(True)
        hbox.set_vexpand(True)

        self.play = Gtk.Button(label=u'▶')
        self.play.connect("clicked", self._play_pause)
        self.stop = Gtk.Button(label="stop")
        self.stop.connect("clicked", self._stop)
        self.next_track = Gtk.Button(label="next")

        hbox.pack_start(self.play, True, True, 0)
        hbox.pack_start(self.stop, True, True, 0)
        hbox.pack_start(self.next_track, True, True, 0)
        grid.add(hbox)

        self.add(grid)

    def update(self, event_type):
        if event_type == mixer.PLAY_EVENT or event_type == mixer.NEXT_EVENT:
            self.play.get_children()[0].set_text(u'▌▌')
        elif event_type == mixer.PAUSE_EVENT or event_type == mixer.STOP_EVENT:
            self.play.get_children()[0].set_text('▶')

    def _play_pause(self, widget):
        if mixer.is_playing():
            mixer.pause()
        else:
            mixer.play()

    def _stop(self, widget):
        mixer.stop()

    def halt(self, window, event):
        mixer.stop()
        Gtk.main_quit()
