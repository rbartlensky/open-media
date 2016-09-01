# -*- coding: utf-8 -*-

import Tkinter as Tk
import os, widgets, tkFileDialog
from openmedia.player import mixer

class InvalidWidgetStateException(Exception):
    pass

class PlayerFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.f_control = _ControlFrame(self)
        self.f_progress = _ProgressFrame(self)
        self.f_playlist = _PlaylistFrame(self)
        self.f_control.grid(row=0, column=0)
        self.f_progress.grid(row=1, column=0)
        self.f_playlist.grid(row=0, column=1, rowspan=10)
        self._bind_all()
        mixer.play()

    def _bind_all(self):
        for button in self.f_control.buttons:
            button.bind(button.sequence, getattr(self, '_' + button.name + '_handler'))
        for button in self.f_playlist.buttons:
            button.bind(button.sequence, getattr(self, '_' + button.name + '_handler'))
        self.f_control.s_volume.bind('<B1-Motion>', self._set_volume)
        self.f_playlist.l_playlist.bind('<Double-Button-1>', self._play)

    def _play_pause_handler(self, event):
        if not mixer.is_paused and not mixer.is_stopped:
            self.f_control.buttons[_ControlFrame.PLAY].config(text=u'▶')
            mixer.pause()
        else:
            self.f_control.buttons[_ControlFrame.PLAY].config(text=u'▌▌')
            mixer.play()

    def _stop_handler(self, event):
        self._play_pause_handler(event)
        mixer.stop()

    def _play_next_handler(self, event):
        if mixer.is_paused:
            self._play_pause_handler(event)
        list_box = self.f_playlist.l_playlist
        list_box.highlight_next(mixer.song_index)
        mixer.play_next()

    def _show_hide_handler(self, event):
        if event.widget.checked is None:
            raise InvalidWidgetStateException('Expected boolean value for ' +
                                              str(event.widget))
        if event.widget.checked:
            self.f_playlist.l_playlist.grid_remove()
            self.f_playlist.buttons[_PlaylistFrame.ADD].grid_remove()
            event.widget.checked = False
        else:
            self.f_playlist.l_playlist.grid(row=0, column=0)
            self.f_playlist.buttons[_PlaylistFrame.ADD].grid(row=1, column=1)
            event.widget.checked = True

    def _play(self, event):
        mixer.stop()
        mixer.play(self.f_playlist.l_playlist.get(Tk.ACTIVE))

    def _add_handler(self, event):
        self.filename = os.path.basename(tkFileDialog.askopenfilename())
        self.f_playlist.l_playlist.insert(Tk.END, self.filename)
        mixer.add(self.filename)

    def _set_volume(self, event):
        mixer.set_volume(float(event.widget.get())/100)

class _PlaylistFrame(Tk.Frame):
    _button_data = [('show_hide', u'≡', False, True),
                   ('add', u'+', None, False)]
    _button_names = 'SHOW_HIDE ADD'

    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.buttons = [widgets.PlayerButton(self, text=text,\
                        name=name, checked=checked, visible=visible) \
                        for name, text, checked, visible in self._button_data]
        for index, button in enumerate(self.buttons):
            if button.visible:
                button.grid(row=1, column=index)
        self._create_playlist()

    def _create_playlist(self):
        self.l_playlist = widgets.PlayList(self)
        for track in mixer.track_list:
            self.l_playlist.insert(Tk.END, os.path.basename(track.get_path()))
        self.l_playlist.highlight_index(0)

for index, field in enumerate(_PlaylistFrame._button_names.split(' ')):
    setattr(_PlaylistFrame, field, index)

class _ControlFrame(Tk.Frame):
    _button_data = [('play_pause', u'▌▌', True),
                   ('stop', u'■', True),
                   ('play_next', u'↦', True)]
    _button_names = 'PLAY STOP NEXT'

    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.buttons = [widgets.PlayerButton(self, text=text,\
                        name=name, visible=visible) \
                        for name, text, visible in self._button_data]
        self.s_volume = widgets.VolumeSlider(self)
        for index, button in enumerate(self.buttons):
            if button.visible:
                button.grid(row=0, column=index)
        self.s_volume= widgets.VolumeSlider(self)
        self.s_volume.grid(row=0, column=6)

for index, field in enumerate(_ControlFrame._button_names.split(' ')):
    setattr(_ControlFrame, field, index)

class _StatusFrame(Tk.Frame):
    def __init__(self, root):
        pass

class _ProgressFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.s_progress = widgets.PlayerSlider(self, to=100)
        self.s_progress.grid()
