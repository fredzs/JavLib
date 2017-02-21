import os
from Utility.Utility import Utility


class KeyService(object):
    @staticmethod
    def find_start(keyset):
        l = os.listdir(keyset.get_key_path())
        l.sort()
        if len(l) > 0:
            start = int(Utility.find_num(l[-1])) + 1
        else:
            start = 1
        keyset.__start = start
