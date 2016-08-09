class Track(object):

    def __init__(self, file_path):
        self.__file_path = file_path

    def get_path(self):
        return self.__file_path
