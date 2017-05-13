# -*- coding: utf-8 -*-

from gi.repository import Gtk
from openmedia.player.player import Player
from openmedia.observable.observable import Observer
from .playlistbox import PlaylistBox
from .progressbar import ProgressBar
from .controlbox import ControlBox
from . import WINDOW_WIDTH, WINDOW_HEIGHT


class InvalidWidgetStateException(Exception):
    pass


class MainWindow(Gtk.Window, Observer):

    def __init__(self):
        Gtk.Window.__init__(self, title="open-media")
        Observer.__init__(self)
        self.connect("delete-event", self.halt)
        Player.instance().add_observer(self)

        self.progress_bar = ProgressBar(Player.instance().get_song_duration())
        self.control_box = ControlBox()
        self.playlist_box = PlaylistBox()

        # it contains the control buttons (play, stop etc), the playlist and
        # the progress bar
        self.upper_box = Gtk.VBox()
        self.upper_box.pack_start(self.control_box, False, False, 0)
        self.upper_box.pack_start(self.progress_bar, False, False, 0)

        # contains the control box and the status widget
        self.control_status_box = Gtk.VBox()
        self.control_status_box.set_border_width(10)
        self.control_status_box.set_spacing(5)
        self.control_status_box.pack_start(self.upper_box, False, True, 0)
        self._create_status_bar()
        self.control_status_box.pack_end(self.status_bar, False, False, 0)
        self.control_status_box.pack_end(Gtk.HSeparator(), False, False, 0)

        # contains the control box, status widget and playlist box
        self.main_paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        self.main_paned.set_border_width(10)
        self.main_paned.set_wide_handle(True)
        self.main_paned.pack1(self.control_status_box, True, False)

        self.add(self.main_paned)
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.show()

    def show(self):
        self.show_all()
        self.control_box.show()

    def _create_status_bar(self):
        self.status_bar = Gtk.Statusbar()
        self.last_context_id = None
        self._update_status("Stopped.")

    def show_playlist(self):
        if self.playlist_box in self.main_paned.get_children():
            self.main_paned.remove(self.playlist_box)
        else:
            self.main_paned.pack2(self.playlist_box, False, False)
            self.show_all()

    def update(self, event, event_type):
        from ..player import player as event
        player = Player.instance()
        if event_type == event.PLAY_EVENT or event_type == event.NEXT_EVENT:
            self.progress_bar.set_range(0, player.get_song_duration())
            self._update_status("Playing '" + str(player.current_track.name) +
                                "'.")
        elif event_type == event.PAUSE_EVENT or event_type == event.STOP_EVENT:
            if event_type == event.PAUSE_EVENT:
                self._update_status("Paused.")
            else:
                self._update_status("Stopped.")
        elif event_type == event.SLIDER_EVENT and \
                not self.progress_bar.skipping:
            self.progress_bar.set_value(player.get_current_second())
            if player.is_playing():
                self._update_status("Playing '" +
                                    str(player.current_track.name) + "'.")
        return False

    def _update_status(self, text="Nothing to show."):
        if self.last_context_id:
            self.status_bar.pop(self.last_context_id)
        context_id = self.status_bar.get_context_id(text)
        self.last_context_id = self.status_bar.push(context_id, text)

    def halt(self, window, event):
        Player.instance().stop()
        Gtk.main_quit()
