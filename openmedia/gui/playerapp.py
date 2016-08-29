import Tkinter as Tk
import widgets, frames

class PlayerApp(object):
    def __init__(self, mixer):
        self.root = Tk.Tk()
        self.m_main = widgets.PlayerMenu()
        self.f_main = frames.PlayerFrame(self.root, mixer)
        self.f_main.grid()
        self.root.config(menu=self.m_main)
        self.root.mainloop()
