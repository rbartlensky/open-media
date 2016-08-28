import sys
from lib.player import mixer

def main(args):
    mixer = Mixer(args[1:])
    mixer.run()

if __name__ == "__main__":
    print sys.argv
    if len(sys.argv) < 2:
        print '[ERROR] Need one or more files to play\n'\
                 'Usage: ./run.py file1 [file_list]'
    else:
        main(sys.argv)
