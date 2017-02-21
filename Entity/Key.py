

class KeySet(object):
    def __init__(self, key):
        self.__key = key
        self.__start = int()
        self.__end = int()
        self.__download_path = str()

    def set_start(self, start):
        self.__start = start

    def set_end(self, end):
        self.__end = end

    def set_download_path(self, download_path):
        self.__download_path = download_path
        return self.__download_path

    @property
    def get_start(self):
        return self.__start

    @property
    def get_end(self):
        return self.__end

    @property
    def get_key(self):
        return self.__key

    @property
    def get_download_path(self):
        return self.__download_path

    @property
    def get_key_path(self):
        return self.__download_path
