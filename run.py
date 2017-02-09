#!/usr/bin/python3

import argparse
import terminal_player
from openmedia.player.player import Player
from openmedia.gui.playerapp import PlayerApp


def main(no_gui=True, args=[]):
    player = Player(args)
    if no_gui:
        terminal_player.run(player, args)
    else:
        PlayerApp()
    player.player_thread.keep_running = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play audio files.')
    parser.add_argument('--no-gui',
                        help='run the player without a graphical user'
                             ' interface',
                        action='store_true')
    parser.add_argument('-t', '--track-list',
                        help='the list of tracks to play',
                        default=[], nargs='+')
    args = parser.parse_args()
    main(no_gui=args.no_gui, args=args.track_list)
