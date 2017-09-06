from threading import Thread
from subprocess import call
from openmedia.player.player import Player
from curses import wrapper
from curses.textpad import Textbox
import curses
import os


help_open = False


def print_playlist(args):
    if args:
        if not Player.instance().current_track:
            Player.instance().play()
        call(['clear'])
        print('Type "h" for help.\nYour playlist is:')
        for arg in args:
            filename = os.path.basename(arg)
            track_path = Player.instance().current_track.file_path
            if filename == os.path.basename(track_path):
                print(('{:<8}{:}'.format('*', filename)))
            else:
                print(('{:<8}{:}'.format('', filename)))
        if Player.instance().is_playing():
            print('Playing')
        elif Player.instance().is_paused:
            print('Paused')
        else:
            print('Stopped')
    else:
        print_help()


def print_help(stdscr):
    global help_open

    help_open = True
    stdscr.clear()
    stdscr.addstr(0,0,
                  "Type 'a' followed by a list of tracks to add them to the playlist")
    stdscr.addstr(1, 0, "Type 'n' to play the next track")
    stdscr.addstr(2, 0, "Type 'p' to play and 'P' to pause")
    stdscr.addstr(3, 0, "Type 'q' to quit")
    stdscr.addstr(4, 0, "Type 'r' to return to the main menu")


def _validate_tracks(ch):
    # user hits return
    if ch == 10:
        return 7
    return ch


def start_player(stdscr, args):
    global help_open

    Player.instance().play()
    playlist = args[:]
    while True:
        input_char = stdscr.getkey()
        if input_char == 'l':
            print_playlist(playlist)
        elif input_char == 'h':
            print_help(stdscr)
        elif input_char == 'n':
            Player.instance().play_next()
        elif input_char == 'p':
            Player.instance().play()
        elif input_char == 'P':
            Player.instance().pause()
        elif input_char == 'r':
            help_open = False
        elif input_char == 'a':
            box = Textbox(stdscr)
            box.edit(_validate_tracks)
            text_input = box.gather()
            tracks = text_input.split(' ')[1:]
            for track in tracks:
                Player.instance().add(track)
                playlist.append(track)
            print_playlist(playlist)
        elif input_char == 'q':
            Player.instance().stop()
            break
        else:
            strscr.addstr("Unknown command '%s'" % input_char)


def run(player, args=[]):
    wrapper(start_player, args)
