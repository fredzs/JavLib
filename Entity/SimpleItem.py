import re


class SimpleItem(object):
    def __init__(self, code):
        self.__code = code

    @property
    def get_key(self):
        key = ""
        pattern = re.compile(r'^([a-zA-Z][0-9a-zA-Z]{1,4})-([0-9]{2,5})')
        match = pattern.match(self.__code)
        if match:
            key = match.group(1)
        return key

    @property
    def get_num(self):
        key = ""
        pattern = re.compile(r'^([a-zA-Z][0-9a-zA-Z]{1,4})-([0-9]{2,5})')
        match = pattern.match(self.__code)
        if match:
            key = match.group(2)
        return key

    @property
    def get_code(self):
        return self.__code
