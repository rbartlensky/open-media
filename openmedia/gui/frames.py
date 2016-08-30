# -*- coding: utf-8 -*-

import Tkinter as Tk
import os, widgets, tkFileDialog
from openmedia.player import mixer

class PlayerFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.f_control = _ControlFrame(self)
        self.f_progress = _ProgressFrame(self)
        self.f_playlist = _PlaylistFrame(self)
        self.f_control.grid(row=0, column=0)
        self.f_progress.grid(row=1, column=0)
        self.f_playlist.grid(row=0, column=1, rowspan=10)

class _PlaylistFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.b_playlist = widgets.PlaylistButton(self, self._show_hide)
        self.b_add = widgets.AddButton(self, self._add_track)
        self.l_playlist = widgets.PlayList(self, self._play)
        self.b_playlist.grid(row=1, column=0)
        self.playlist_visible = False

    def _show_hide(self):
        if self.playlist_visible:
            self.l_playlist.grid_remove()
            self.b_add.grid_remove()
            self.playlist_visible = False
        else:
            self.l_playlist.grid(row=0, column=0)
            self.b_add.grid(row=1, column=1)
            self.playlist_visible = True

    def _play(self, event):
        mixer.stop()
        mixer.init([self.l_playlist.get(Tk.ACTIVE)])
        mixer.play()

    def _add_track(self):
        self.filename = tkFileDialog.askopenfilename()
        self.l_playlist.insert(Tk.END, os.path.basename(self.filename))

class _ControlFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.b_play = widgets.PlayButton(self, self._play_pause)
        self.b_stop = widgets.StopButton(self, self._stop)
        self.b_next = widgets.NextButton(self, self._play_next)
        self.s_volume = widgets.VolumeSlider(self)
        self.b_play.grid(row=0, column=0)
        self.b_stop.grid(row=0, column=1)
        self.b_next.grid(row=0, column=2)
        self.s_volume.grid(row=0, column=6, columnspan=3)

    def _play_pause(self):
        if not mixer.is_paused and not mixer.is_stopped:
            self.b_play.config(text=u'▶')
            mixer.pause()
        else:
            self.b_play.config(text=u'▌▌')
            mixer.play()

    def _stop(self):
        self._play_pause()
        mixer.stop()

    def _play_next(self):
        if mixer.is_paused:
            self._play_pause()
        mixer.play_next()

class _StatusFrame(Tk.Frame):
    def __init__(self, root):
        pass

class _ProgressFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.s_progress = widgets.PlayerSlider(self, to=100)
        self.s_progress.grid()
