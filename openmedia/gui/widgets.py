# -*- coding: utf-8 -*-

import Tkinter as Tk
import tkFileDialog
from openmedia.player import mixer

class PlayerButton(Tk.Button):
    def __init__(self, root, text, name, visible=True, checked=None, cmd=None):
        Tk.Button.__init__(self, root, text=text, command=cmd)
        self.sequence = '<Button-1>'
        self.name = name
        self.visible = visible
        self.checked = checked

    def __str__(self):
        return 'PlayerButton: %s, visible = %s, checked = %s' % \
                (self.name, self.visible, self.checked)

class PlayList(Tk.Listbox):
    def __init__(self, root):
        Tk.Listbox.__init__(self, root, selectmode=Tk.SINGLE)

    def highlight_index(self, index):
        self.selection_clear(Tk.ACTIVE)
        self.activate(index)
        self.selection_set(index)

    def highlight_next(self, index):
        self.highlight_index((index + 1) % self.size())

    def add_track(self, name):
        self.insert(Tk.END, name)

    def clear(self):
        self.delete(0, Tk.END)

class PlayerMenu(Tk.Menu):
    def __init__(self, open_file):
        Tk.Menu.__init__(self)
        self._create_sub_menu("File", [{"label" : "Open", "command" : open_file},\
                                       {"label" : "Quit", "command" : Tk.Frame().quit}])

    def _create_sub_menu(self, label, commands):
        sub_menu = Tk.Menu()
        self.add_cascade(label=label, menu=sub_menu)
        for command in commands:
            sub_menu.add_command(label=command["label"], command=command["command"])

class PlayerSlider(Tk.Scale):
    def __init__(self, root, to):
        Tk.Scale.__init__(self, root, from_=0, to=to, orient=Tk.HORIZONTAL)

class VolumeSlider(Tk.Scale):
    def __init__(self, root):
        Tk.Scale.__init__(self, root, from_=0, to=100, orient=Tk.HORIZONTAL, command=None)

