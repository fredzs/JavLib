import re
from bs4 import BeautifulSoup


class Item(object):
    def __init__(self, key, num):
        self.__key = key
        self.__num = num
        self.__title = str()
        self.__img_src = str()
        self.__date = str()
        self.__rank = float()
        self.__link = str()
        self.__duration = int()
        self.__actor = str()
        self.__soup = BeautifulSoup()

    def set_title(self, title):
        self.__title = title

    def set_img_src(self, img_src):
        self.__img_src = img_src

    def set_soup(self, soup):
        self.__soup = soup

    def set_date(self, date):
        self.__date = date

    def set_rank(self, rank):
        if not rank == '':
            self.__rank = float(rank)
        else:
            self.__rank = float(0)

    def set_link(self, link):
        self.__link = link

    def set_duration(self, duration):
        self.__duration = duration

    def set_actor(self, actor):
        self.__actor = actor

    @property
    def get_code(self):
        return self.__key + '-' + str("%03d" % self.__num)

    @property
    def get_key(self):
        return self.__key

    @property
    def get_num(self):
        return int(self.__num)

    @property
    def get_title(self):
        return self.__title

    @property
    def get_img_src(self):
        return self.__img_src

    @property
    def get_date(self):
        return self.__date

    @property
    def get_rank(self):
        return self.__rank

    @property
    def get_link(self):
        return self.__link

    @property
    def get_duration(self):
        return self.__duration

    @property
    def get_link(self):
        return self.__link

    @property
    def get_actor(self):
        return self.__actor

    @property
    def get_soup(self):
        return self.__soup

    def tidy_title(self):
        if len(self.__title) >= 100:
            self.set_title(self.__title[0:100])
        self.__title = self.__title.replace("*", "").replace(":", "").replace("/", "")

        pattern1 = re.compile(r'^([a-zA-Z][0-9a-zA-Z]{1,4}-)([0-9]{2,5})(.*)')
        match1 = pattern1.match(self.__title)
        if match1 and len(match1.group(2)) < 3:
            self.__title = match1.group(1) + str("%03d" % int(match1.group(2))) + match1.group(3)

        pattern2 = re.compile(r'^([a-zA-Z][0-9a-zA-Z]{1,4}-)0([0-9]{1,4})(.*)')
        match2 = pattern2.match(self.__title)
        if match2 and len(match2.group(2)) > 2:
            self.__title = match2.group(1) + match2.group(2) + match2.group(3)

    def match(self, html_code):
        condition = self.__key + '-[0]*' + str(self.__num) + '$'
        pattern = re.compile(condition)
        match = pattern.match(html_code)
        if match:
            return True
        else:
            return False
