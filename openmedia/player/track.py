from mutagen.mp3 import MP3, MPEGInfo

class Track(object):

    def __init__(self, file_path):
        self.__file_path = file_path
        self.duration = MP3(file_path).info.length

    def get_path(self):
        return self.__file_path
