# -*- coding: utf-8 -*-

import Tkinter as Tk
import widgets
from openmedia.player import mixer

class PlayerFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.f_control = _ControlFrame(self)
        self.f_progress = _ProgressFrame(self)
        self.f_control.grid(row=0, column=0)
        self.f_progress.grid(row=1, column=0)

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
        mixer.play_next()

class _StatusFrame(Tk.Frame):
    def __init__(self, root):
        pass

class _ProgressFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.s_progress = widgets.PlayerSlider(self, to=100)
        self.s_progress.grid()
