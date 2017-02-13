# -*- coding: utf-8 -*-

from gi.repository import Gtk
from .playlistbox import PlaylistBox
from openmedia.observable.observable import Observer
from openmedia.player.player import Player
from .tools.iconhelp import get_button_image
from .tools.iconhelp import get_name
from ..player import player


class ControlBox(Gtk.VBox, Observer):

    def __init__(self):
        Gtk.VBox.__init__(self, False)
        Observer.__init__(self)
        Player.instance().add_observer(self)
        self.button_box = Gtk.HBox()
        self.button_box.set_spacing(5)
        self.playlist_box = PlaylistBox()
        self._create_buttons()
        self.set_spacing(5)
        self.button_box.pack_start(self.play_button, False, False, 0)
        self.button_box.pack_start(self.stop_button, False, False, 0)
        self.button_box.pack_start(self.play_prev_button, False, False, 0)
        self.button_box.pack_start(self.play_next_button, False, False, 0)
        self.volume_box = Gtk.HBox()
        self.volume_box.pack_end(self.volume_button, False, True, 0)
        self.button_box.pack_start(self.playlist_button, False, False, 0)
        self.button_box.pack_end(self.volume_box, True, True, 0)
        self.pack_start(self.playlist_box, False, False, 0)
        self.pack_start(self.button_box, False, False, 0)

    def _create_buttons(self):
        self.play_button = Gtk.Button.new_from_icon_name(get_name("play"),
                                                         Gtk.IconSize.BUTTON)
        self.play_button.connect("clicked", self._play_pause)
        self.stop_button = Gtk.Button.new_from_icon_name(get_name("stop"),
                                                         Gtk.IconSize.BUTTON)
        self.stop_button.connect("clicked", self._stop)
        self.play_next_button = Gtk.Button.new_from_icon_name(get_name("skip"),
                                                              Gtk.IconSize.BUTTON)
        self.play_next_button.connect("clicked", self._play_next)
        self.play_prev_button = Gtk.Button.new_from_icon_name(get_name("prev"),
                                                              Gtk.IconSize.BUTTON)
        self.play_prev_button.connect("clicked", self._play_previous)
        self.volume_button = Gtk.VolumeButton()
        self.volume_button.set_value(0.5)
        self.volume_button.connect("value-changed", self._volume)
        self.volume_button.x_align = 1.0
        self.playlist_button = Gtk.ToggleButton()
        self.playlist_button.set_image(get_button_image(get_name("menu")))
        self.playlist_button.connect("clicked", self._toggle_playlist)

    def update(self, event, event_type):
        if event_type == player.PLAY_EVENT or event_type == player.NEXT_EVENT:
            image = get_button_image(get_name("pause"))
            self.play_button.set_image(image)
        elif event_type == player.PAUSE_EVENT or\
                event_type == player.STOP_EVENT:
            image = get_button_image(get_name("play"))
            self.play_button.set_image(image)
        return False

    def show(self):
        self.show_all()
        self.playlist_box.hide()

    def _play_pause(self, widget):
        player = Player.instance()
        if player.is_playing():
            player.pause()
        else:
            player.play()

    def _play_next(self, widget):
        Player.instance().play_next()
        if self.playlist_box.is_visible():
            self.playlist_box.show_all()

    def _play_previous(self, widget):
        Player.instance().play_previous()
        if self.playlist_box.is_visible():
            self.playlist_box.show_all()

    def _stop(self, widget):
        Player.instance().stop()

    def _volume(self, widget, value):
        Player.instance().set_volume(value)

    def _toggle_playlist(self, widget):
        if self.playlist_box.is_visible():
            self.playlist_box.set_visible(False)
        else:
            self.playlist_box.set_visible(True)
