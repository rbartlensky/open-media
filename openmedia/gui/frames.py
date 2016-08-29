import Tkinter as Tk
import widgets

class PlayerFrame(Tk.Frame):
    def __init__(self, root, mixer):
        Tk.Frame.__init__(self, root)
        self.f_control = _ControlFrame(self, mixer)
        self.f_progress = _ProgressFrame(self)
        self.f_control.grid(row=0, column=0)
        self.f_progress.grid(row=1, column=0)

class _ControlFrame(Tk.Frame):
    def __init__(self, root, mixer):
        Tk.Frame.__init__(self, root)
        self.b_play = widgets.PlayButton(self, mixer)
        self.s_volume = widgets.VolumeSlider(self)
        self.b_play.grid(row=0, column=0)
        self.s_volume.grid(row=0, column=6, columnspan=3)

class _StatusFrame(Tk.Frame):
    def __init__(self, root):
        pass

class _ProgressFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.s_progress = widgets.PlayerSlider(self, to=100)
        self.s_progress.grid()
