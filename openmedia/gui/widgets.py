#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as Tk
import tkFileDialog

class NoMixerException(Exception):
    pass

class PlayButton(Tk.Button):
    def __init__(self, root, mixer):
        Tk.Button.__init__(self, root, text=u'▌▌', command=self._play_pause)
        self.is_paused = False
        self.mixer = mixer
        self.mixer.play()

    def _play_pause(self):
        if not self.mixer:
            raise NoMixerException()
        elif not self.is_paused:
            self.config(text=u'▶')
            self.is_paused = True
            self.mixer.pause()
        else:
            self.config(text=u'▌▌')
            self.is_paused = False
            self.mixer.play()

class PlayerMenu(Tk.Menu):
    def __init__(self):
        Tk.Menu.__init__(self)
        self._create_sub_menu("File", [{"label" : "Open", "command" : self._open_file},\
                                       {"label" : "Quit", "command" : Tk.Frame().quit}])

    def _open_file(self):
        self.filename = tkFileDialog.askopenfilename()
        self.openfile = tkFileDialog.askopenfile()

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
        Tk.Scale.__init__(self, root, from_=0, to=100, orient=Tk.HORIZONTAL)
