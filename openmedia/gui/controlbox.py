# -*- coding: utf-8 -*-

from gi.repository import Gtk
from playlistbox import PlaylistBox
from openmedia.observable.observable import Observer
from openmedia.player import mixer


class ControlBox(Gtk.VBox, Observer):

    def __init__(self):
        Gtk.VBox.__init__(self, False)
        Observer.__init__(self)
        mixer.add_observer(self)
        self.button_box = Gtk.HBox()
        self.button_box.set_spacing(5)
        self.playlist_box = PlaylistBox()
        self._create_buttons()
        self.set_spacing(5)
        self.button_box.pack_start(self.play_button, False, False, 0)
        self.button_box.pack_start(self.stop_button, False, False, 0)
        self.button_box.pack_start(self.play_next_button, False, False, 0)
        self.volume_box = Gtk.HBox()
        self.volume_box.pack_end(self.volume_button, False, True, 0)
        self.button_box.pack_start(self.playlist_button, False, False, 0)
        self.button_box.pack_end(self.volume_box, True, True, 0)
        self.pack_start(self.playlist_box, False, False, 0)
        self.pack_start(self.button_box, False, False, 0)

    def _create_buttons(self):
        self.play_button = Gtk.Button(label=u'▶')
        self.play_button.connect("clicked", self._play_pause)
        self.stop_button = Gtk.Button(label=u'■')
        self.stop_button.connect("clicked", self._stop)
        self.play_next_button = Gtk.Button(label=">>")
        self.play_next_button.connect("clicked", self._play_next)
        self.volume_button = Gtk.VolumeButton()
        self.volume_button.set_value(0.5)
        self.volume_button.connect("value-changed", self._volume)
        self.volume_button.x_align = 1.0
        self.playlist_button = Gtk.ToggleButton(label="=")
        self.playlist_button.connect("clicked", self._toggle_playlist)

    def update(self, event, event_type):
        if event_type == mixer.PLAY_EVENT or event_type == mixer.NEXT_EVENT:
            self.play_button.get_children()[0].set_text(u'▌▌')
        elif event_type == mixer.PAUSE_EVENT or event_type == mixer.STOP_EVENT:
            self.play_button.get_children()[0].set_text('▶')
        return False

    def show(self):
        self.show_all()
        self.playlist_box.hide()

    def _play_pause(self, widget):
        if mixer.is_playing():
            mixer.pause()
        else:
            mixer.play()

    def _play_next(self, widget):
        mixer.play_next()
        if self.playlist_box.is_visible():
            self.playlist_box.show_all()

    def _stop(self, widget):
        mixer.stop()

    def _volume(self, widget, value):
        mixer.set_volume(value)

    def _toggle_playlist(self, widget):
        if self.playlist_box.is_visible():
            self.playlist_box.set_visible(False)
        else:
            self.playlist_box.set_visible(True)
