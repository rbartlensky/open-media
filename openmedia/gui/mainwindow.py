# -*- coding: utf-8 -*-

from curses import wrapper
from openmedia.player.player import Player
from openmedia.observable.observable import Observer
import time


def main(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr('Implement me')
        stdscr.refresh()
        time.sleep(1)


def run():
    wrapper(main)
