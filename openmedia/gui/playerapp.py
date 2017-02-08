from gi.repository import Gtk
from .mainwindow import MainWindow


class PlayerApp(object):
    def __init__(self):
        self.w_main = MainWindow()
        self.w_main.show()
        Gtk.main()
