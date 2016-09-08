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
        for i in xrange(0, 2):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)
        self._bind_all()
        mixer.play()

    def _bind_all(self):
        for button in self.f_control.buttons:
            button.bind(button.sequence, getattr(self, '_' + button.name + '_handler'))
        for button in self.f_playlist.buttons:
            button.bind(button.sequence, getattr(self, '_' + button.name + '_handler'))
        self.f_control.s_volume.bind('<B1-Motion>', self._set_volume)
        self.f_progress.s_progress.bind('<ButtonRelease-1>', self._skip)
        self.f_playlist.l_playlist.bind('<Double-Button-1>', self._play)
        self.f_progress.set_alarm(self._progress)

    def _update_play_icon(self, button):
        if mixer.is_playing():
            button.config(text=u'▶')
        else:
            button.config(text=u'▌▌')

    def _play_pause(self, button):
        self._update_play_icon(button)
        if mixer.is_playing():
            mixer.pause()
        else:
            mixer.play()

    def _play_pause_handler(self, event):
        self._play_pause(event.widget)

    def _stop_handler(self, event):
        if not mixer.is_stopped:
            self._play_pause(self.f_control.buttons[_ControlFrame.PLAY])
            mixer.stop()
            self.f_progress.set_progress(0)

    def _play_next(self, button):
        self.f_control.buttons[_ControlFrame.PLAY].config(text=u'▌▌')
        list_box = self.f_playlist.l_playlist
        list_box.highlight_next(mixer.curr_track_index)
        self.f_progress.set_progress(0)
        mixer.play_next()
        self.f_progress.set_max_progress(mixer.get_song_duration())

    def _play_next_handler(self, event):
        self._play_next(event.widget)

    def _show_hide_handler(self, event):
        if event.widget.checked is None:
            raise InvalidWidgetStateException('Expected boolean value for ' +
                                              str(event.widget))
        if event.widget.checked:
            self.f_playlist.l_playlist.grid_remove()
            self.f_playlist.yscroll.grid_remove()
            self.f_playlist.buttons[_PlaylistFrame.ADD].grid_remove()
            event.widget.checked = False
        else:
            self.f_playlist.l_playlist.grid(row=0, column=0, columnspan=2)
            self.f_playlist.yscroll.grid(row=0, column=2, sticky=Tk.N+Tk.S)
            self.f_playlist.buttons[_PlaylistFrame.ADD].grid(row=1, column=1)
            event.widget.checked = True

    def _play(self, event):
        mixer.stop()
        mixer.play(self.f_playlist.l_playlist.get(Tk.ACTIVE))
        self.f_control.buttons[_ControlFrame.PLAY].config(text=u'▌▌')
        f_progress = self.f_progress
        f_progress.set_progress(0)
        f_progress.set_max_progress(mixer.get_song_duration())

    def _add_handler(self, event):
        self.filename = os.path.basename(tkFileDialog.askopenfilename())
        self.f_playlist.l_playlist.add_track(self.filename)
        mixer.add(self.filename)

    def _set_volume(self, event):
        mixer.set_volume(float(event.widget.get()) / 100)

    def _progress(self):
        new_value = mixer.get_pos() / 1000
        if new_value != -1:
            self.f_progress.set_progress(new_value)
        else:
            self._play_next([_ControlFrame.NEXT])
        self.f_progress.set_alarm(self._progress)

    def _skip(self, event):
        value = self.f_progress.get_progress()
        mixer.skip(value)

    def open_file(self):
        self.filename = tkFileDialog.askopenfilename()
        mixer.stop()
        mixer.init([self.filename])
        self.f_playlist.l_playlist.clear()
        self.f_playlist.l_playlist.add_track(os.path.basename(self.filename))
        self.f_playlist.l_playlist.highlight_next(mixer.curr_track_index)
        mixer.set_volume(float(self.f_control.s_volume.get()) / 100)
        self._update_play_icon(self.f_control.buttons[_ControlFrame.PLAY])
        mixer.play()

class _PlaylistFrame(Tk.Frame):
    _button_data = [('show_hide', u'≡', False, True),
                   ('add', u'+', None, False)]
    _button_names = 'SHOW_HIDE ADD'

    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.yscroll = Tk.Scrollbar(root)
        self.buttons = [widgets.PlayerButton(self, text=text,\
                        name=name, checked=checked, visible=visible) \
                        for name, text, checked, visible in self._button_data]
        for index, button in enumerate(self.buttons):
            if button.visible:
                button.grid(row=1, column=index)
        self._create_playlist()
        self.yscroll.config(command=self.l_playlist.yview)

    def _create_playlist(self):
        self.l_playlist = widgets.PlayList(self, yscrollcommand=self.yscroll.set)
        for track in mixer.track_list:
            self.l_playlist.add_track(os.path.basename(track.get_path()))
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
                button.grid(row=0, column=index, padx=2)
        self.s_volume = widgets.VolumeSlider(self)
        self.s_volume.grid(row=0, column=4, ipady=8)
        self.s_volume.set(50)

for index, field in enumerate(_ControlFrame._button_names.split(' ')):
    setattr(_ControlFrame, field, index)

class _ProgressFrame(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.s_progress = widgets.PlayerSlider(self, to=mixer.get_song_duration())
        self.s_progress.grid(row=0, column=0, ipady=10)

    def set_alarm(self, callback):
        self.s_progress.after(1000, callback)

    def get_progress(self):
        return self.s_progress.get()

    def set_progress(self, value):
        self.s_progress.set(value)

    def set_max_progress(self, value):
        self.s_progress.config(to=mixer.get_song_duration())
