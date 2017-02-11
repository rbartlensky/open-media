from threading import Thread
from subprocess import call
import os
from openmedia.player.player import Player


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


def print_help():
    global help_open

    help_open = True
    call(['clear'])
    print("Type 'a' followed by a list of tracks to add them to the playlist")
    print("Type 'n' to play the next track")
    print("Type 'p' to play and 'P' to pause")
    print("Type 'q' to quit")
    print("Type 'r' to return to the main menu")


def start_player(args):
    global help_open

    playlist = args[:]
    input_char = None
    while True:
        if not help_open:
            print_playlist(playlist)
        else:
            print_help()
        input_char = input().strip()
        if input_char == 'h':
            print_help()
        elif input_char == 'n':
            Player.instance().play_next()
        elif input_char == 'p':
            Player.instance().play()
        elif input_char == 'P':
            Player.instance().pause()
        elif input_char == 'r':
            help_open = False
        elif len(input_char) and input_char[0] == 'a':
            tracks = input_char.split(' ')[1:]
            for track in tracks:
                Player.instance().add(track)
                playlist.append(track)
            print_playlist(playlist)
        elif input_char == 'q':
            Player.instance().stop()
            break
        else:
            print(("Unknown command '%s'" % input_char))


def run(player, args=[]):
    Player.instance().play()
    runner = Thread(target=start_player, args=(args,))
    runner.start()
    runner.join()
