import logging
import requests

from Entity.Config import Config
from Utility.Utility import Utility


class NetworkService(object):
    proxies = dict(http='socks5://127.0.0.1:1080', https='socks5://127.0.0.1:1080')
    headers1 = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, sdch",
        'Accept-Language': "zh-CN,zh;q=0.8,pt;q=0.6,en;q=0.4,th;q=0.2",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        'Referer': "http://www.javl10.com/cn/",
        'Upgrade-Insecure-Requests': "1",
        'Connection': "keep-alive",
        'Host': "www.javl10.com"
    }

    headers2 = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, sdch",
        'Accept-Language': "zh-CN,zh;q=0.8,pt;q=0.6,en;q=0.4,th;q=0.2",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        'Referer': "http://www.j12lib.com/cn/",
        'Upgrade-Insecure-Requests': "1",
        'Connection': "keep-alive",
        'Host': "www.j12lib.com"
    }

    headers3 = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, sdch",
        'Accept-Language': "zh-CN,zh;q=0.8,pt;q=0.6,en;q=0.4,th;q=0.2",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        'Referer': "http://www.jav11b.com/cn/",
        'Upgrade-Insecure-Requests': "1",
        'Connection': "keep-alive",
        'Host': "www.jav11b.com"
    }

    @staticmethod
    def get_search_html(code):
        num = Utility.find_num(code)
        if num % 3 == 0:
            server = Config.get_config_field()["search_url1"]
            headers = NetworkService.headers1
        elif num % 3 == 1:
            server = Config.get_config_field()["search_url2"]
            headers = NetworkService.headers2
        else:
            server = Config.get_config_field()["search_url3"]
            headers = NetworkService.headers3
        item_url = server + code
        logging.info("开始处理" + code + ": " + item_url)
        item_html = requests.get(item_url, headers=headers, proxies=NetworkService.proxies)
        return item_html

    @staticmethod
    def get_base_html(i_href, code):
        num = Utility.find_num(code)
        if num % 3 == 0:
            server = Config.get_config_field()["base_url1"] + i_href[i_href.find('?'):]
            headers = NetworkService.headers1
        elif num % 3 == 1:
            server = Config.get_config_field()["base_url2"] + i_href[i_href.find('?'):]
            headers = NetworkService.headers2
        else:
            server = Config.get_config_field()["base_url3"] + i_href[i_href.find('?'):]
            headers = NetworkService.headers3
        item_url = server
        logging.info("开始处理" + code + ": " + item_url)
        item_html = requests.get(item_url, headers=headers, proxies=NetworkService.proxies)
        return item_html
