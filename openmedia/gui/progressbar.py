# -*- coding: utf-8 -*-

from gi.repository import Gtk
from openmedia.player.player import Player
from openmedia.tools.timeformatter import hms_format


class ProgressBar(Gtk.Scale):

    def __init__(self, song_duration):
        Gtk.Scale.__init__(self)
        self._skipping = False
        self.set_range(0, song_duration)
        self.set_value(0)
        self.connect("button-press-event", self._start_skip)
        self.connect("button-release-event", self._end_skip)
        self.connect("format-value", _hms_format)

    @property
    def skipping(self):
        return self._skipping

    def _start_skip(self, widget, value):
        self._skipping = True

    def _end_skip(self, widget, value):
        self._skipping = False
        Player.instance().skip(widget.get_value())


def _hms_format(scale, value):
    return hms_format(value)
