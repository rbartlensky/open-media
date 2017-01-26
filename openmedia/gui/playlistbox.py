# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GObject
from openmedia.player import mixer
from openmedia.observable.observable import Observer
from openmedia.tools.timeformatter import hms_format
from tools.iconhelp import get_name


class PlaylistBox(Gtk.VBox, Observer):

    def __init__(self):
        Gtk.VBox.__init__(self)
        Observer.__init__(self)
        mixer.add_observer(self)
        self.set_spacing(5)
        self._create_playlist()
        self.pack_start(self.playlist, False, False, 0)
        self.pack_start(self.add_track, False, False, 0)

    def _create_playlist(self):
        self.model = Gio.ListStore.new(ModelItem)
        self.playlist = Gtk.ListBox()
        self.playlist.bind_model(self.model, self._create_list_item, None)
        self.playlist.connect("row_activated", self._play_item)
        for track in mixer.track_list:
            item = ModelItem(track.metadata.track_name, track.duration)
            self.model.append(item)
        self.playlist.select_row(self.playlist.get_row_at_index(0))
        self.add_track = Gtk.Button.new_from_icon_name(get_name("add"),
                                                       Gtk.IconSize.BUTTON)
        self.add_track.connect("clicked", self._add_track)

    def _add_track(self, widget):
        dialog = Gtk.FileChooserDialog(Gtk.FileChooserAction.OPEN)
        # XXX dialog should be transient for the main window
        dialog.set_transient_for(Gtk.Window())
        dialog.set_title("Add tracks to your playlist")
        dialog.add_button("_Open", Gtk.ResponseType.OK)
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.set_default_response(Gtk.ResponseType.OK)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            mixer.add(dialog.get_filename())
            track_name = mixer.track_list[-1].metadata.track_name
            self.model.append(ModelItem(track_name,
                                        mixer.track_list[-1].duration))
            self.show_all()
        dialog.destroy()

    def _play_item(self, list_box, row):
        mixer.play(mixer.track_list[row.get_index()].file_path)

    def _create_list_item(self, item, data):
        hbox = Gtk.HBox(5)
        title_label = Gtk.Label(item.title)
        duration_label = Gtk.Label(hms_format(item.duration))
        title_label.show()
        duration_label.show()
        hbox.pack_start(title_label, False, False, 0)
        hbox.pack_start(duration_label, False, False, 0)
        return hbox

    def update(self, event, event_type):
        if event_type == mixer.PLAY_EVENT or event_type == mixer.NEXT_EVENT:
            row = self.playlist.get_row_at_index(mixer.curr_track_index)
            self.playlist.select_row(row)
        return False


class ModelItem(GObject.Object):

    def __init__(self, title, duration):
        GObject.Object.__init__(self)
        self.title = title
        self.duration = duration
