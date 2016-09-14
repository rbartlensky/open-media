import sys, time
from openmedia.player import mixer
from openmedia.gui.playerapp import PlayerApp

def main(args):
    mixer.init(args[1:])
    player = PlayerApp()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print '[ERROR] Need one or more files to play\n'\
                 'Usage: ./run.py file1 [file_list]'
    else:
        main(sys.argv)
