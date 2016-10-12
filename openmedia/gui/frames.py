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

        self.play_next_button = Gtk.Button(label=">>")
        self.play_next_button.connect("clicked", self._play_next)
        self.play_next_button.set_vexpand(False)

        self.volume_button = Gtk.VolumeButton()
        self.volume_button.set_value(0.5)
        self.volume_button.connect("value-changed", self._volume)
        self.volume_button.x_align = 1.0
        self.volume_button.set_vexpand(False)

        self.playlist_button = Gtk.ToggleButton(label="=")
        self.playlist_button.connect("clicked", self._toggle_playlist)
        self.playlist_button.set_vexpand(False)

        self.buttonsBox = Gtk.HBox(False)
        self.buttonsBox.set_spacing(5)
        self.buttonsBox.pack_start(self.play_button, False, False, 0)
        self.buttonsBox.pack_start(self.stop_button, False, False, 0)
        self.buttonsBox.pack_start(self.play_next_button, False, False, 0)
        self.volumeBox = Gtk.HBox()
        self.volumeBox.pack_end(self.volume_button, False, True, 0)
        self.buttonsBox.pack_start(self.playlist_button, False, False, 0)
        self.buttonsBox.pack_end(self.volumeBox, True, True, 0)
        self.buttonsBox.set_vexpand(False)

    def _create_playlist(self):
        self.model = Gio.ListStore.new(ModelItem)
        self.playlist = Gtk.ListBox()
        self.playlist.bind_model(self.model, self._create_list_item, None)
        self.playlist.connect("row_activated", self._play_item)
        for track in mixer.track_list:
            item = ModelItem(track.name, track.duration)
            self.model.append(item)
        self.playlist.select_row(self.playlist.get_row_at_index(0))
        self.add_track = Gtk.Button(label="+")
        self.add_track.connect("clicked", self._add_track)

        self.playlistBox = Gtk.VBox()
        self.playlistBox.set_spacing(5)
        self.playlistBox.pack_start(self.playlist, False, False, 0)
        self.playlistBox.pack_start(self.add_track, False, False, 0)
        self.playlistBox.set_vexpand(False)

    def _create_list_item(self, item, data):
        hbox = Gtk.HBox(5)
        title_label = Gtk.Label(item.title)
        duration_label = Gtk.Label(hms_format(item.duration))
        title_label.show()
        duration_label.show()
        hbox.pack_start(title_label, False, False, 0)
        hbox.pack_start(duration_label, False, False, 0)
        return hbox

    def _play_item(self, list_box, row):
        mixer.play(mixer.track_list[row.get_index()].file_path)

    def _add_track(self, widget):
        dialog = Gtk.FileChooserDialog(Gtk.FileChooserAction.OPEN)
        dialog.set_transient_for(self)
        dialog.set_title("Add tracks to your playlist")
        dialog.add_button("_Open", Gtk.ResponseType.OK)
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.set_default_response(Gtk.ResponseType.OK)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            mixer.add(dialog.get_filename())
            self.model.append(ModelItem(mixer.track_list[-1].metadata.track_name,\
                              mixer.track_list[-1].duration))
            self.show_all()
        dialog.destroy()

    def _start_skip(self, widget, value):
        self.skipping = True

    def _end_skip(self, widget, value):
        mixer.skip(widget.get_value())
        self.skipping = False

    def show(self):
        self.show_all()
        self.playlistBox.hide()

    def update(self, event, event_type):
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
