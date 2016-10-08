import frames
import gi

from gi.repository import Gtk

class PlayerApp(object):
    def __init__(self):
        self.f_main = frames.PlayerFrame()
        self.f_main.show_all()
        Gtk.main()
