from audiotools import open, Filename

class Track(object):

    def __init__(self, file_path):
        self.__file_path = file_path
        self.track_file = open(file_path)
        self.duration = self.track_file.seconds_length()
        self.meta_data = self.track_file.get_metadata()

    def get_path(self):
        return self.__file_path

    
