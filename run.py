import sys, time
from openmedia.player import mixer
from openmedia.gui.playerapp import PlayerApp

def main(args):
    mix = mixer.Mixer(args[1:])
    player = PlayerApp(mix)

if __name__ == "__main__":
    print sys.argv
    if len(sys.argv) < 2:
        print '[ERROR] Need one or more files to play\n'\
                 'Usage: ./run.py file1 [file_list]'
    else:
        main(sys.argv)
