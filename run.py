import sys, argparse
from openmedia.player import mixer
from openmedia.gui.playerapp import PlayerApp

def main(args):
    mixer.init(args)
    player = PlayerApp()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play audio files.')
    parser.add_argument('--no-gui',
                        help='run the player without a graphical user interface',
                        action='store_true')
    parser.add_argument('-t', '--track-list',
                        help='the list of tracks to play',
                        default=[], nargs='+')
    args = parser.parse_args()
    if args.no_gui:
        pass
    else:
        main(args.track_list)
