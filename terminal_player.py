from threading import Thread
from subprocess import call
import os
import openmedia.player.mixer as mixer

help_open = False

def print_playlist(args):
    if args:
        if not mixer.current_track:
            mixer.init(args)
            mixer.play()
        call(['clear'])
        print 'Type "h" for help.\nYour playlist is:'
        for arg in args:
            filename = os.path.basename(arg)
            if filename  == os.path.basename(mixer.current_track.file_path):
                print '{:<8}{:}'.format('*', filename)
            else:
                print '{:<8}{:}'.format('', filename)
        if mixer.is_playing():
            print 'Playing'
        elif mixer.is_paused:
            print 'Paused'
        else:
            print 'Stopped'
    else:
        print_help()

def print_help():
    global help_open

    help_open = True
    call(['clear'])
    print "Type 'a' followed by a list of tracks to add them to the playlist"
    print "Type 'n' to play the next track"
    print "Type 'p' to play and 'P' to pause"
    print "Type 'q' to quit"
    print "Type 'r' to return to the main menu"

def start_player(args):
    global help_open

    playlist = args[:]
    input_char = None
    while True:
        if not help_open:
            print_playlist(playlist)
        else:
            print_help()
        input_char = raw_input().strip()
        if input_char == 'h':
            print_help()
        elif input_char == 'n':
            mixer.play_next()
        elif input_char == 'p':
            mixer.play()
        elif input_char == 'P':
            mixer.pause()
        elif input_char == 'r':
            help_open = False
        elif input_char[0] == 'a':
            tracks = input_char.split(' ')[1:]
            for track in tracks:
                mixer.add(track)
                playlist.append(track)
            print_playlist(playlist)
        elif input_char == 'q':
            mixer.stop()
            break
        else:
            print "Unknown command '%s'" % input_char

def run(args=[]):
    mixer.play()
    runner = Thread(target=start_player, args=(args,))
    runner.start()
    runner.join()
