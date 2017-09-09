# -*- coding: utf-8 -*-

from .playlistbox import PlaylistBox
from openmedia.observable.observable import Observer
from openmedia.player.player import Player
from .tools.iconhelp import get_button_image
from .tools.iconhelp import get_name
from ..player import player
from . import WINDOW_WIDTH, WINDOW_HEIGHT


class StatusWindow(Observer):

    def __init__(self):
        Observer.__init__(self)
        Player.instance().add_observer(self)
