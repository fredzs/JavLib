import logging
import os
import re
import shutil

from Entity.Config import Config


class Utility(object):
    @staticmethod
    def find_key(file_name):
        pattern = re.compile(r'^([a-zA-Z][0-9a-zA-Z]{1,4})-([0-9]{2,5})(.*)')
        match = pattern.match(file_name)
        if match:
            key = match.group(1)
        else:
            key = ""
        return key

    @staticmethod
    def find_code(file_name):
        pattern = re.compile(r'^([a-zA-Z][0-9a-zA-Z]{1,4}-[0-9]{2,5})(.*)')
        match = pattern.match(file_name)
        if match:
            code = match.group(1)
        else:
            code = ""
        return code

    @staticmethod
    def find_num(file_name):
        pattern = re.compile(r'^([a-zA-Z][0-9a-zA-Z]{1,4})-([0-9]{2,5})(.*)')
        match = pattern.match(file_name)
        if match:
            num = match.group(2)
        else:
            num = ""
        return int(num)

    @staticmethod
    def find_num_str(file_name):
        pattern = re.compile(r'^([a-zA-Z][0-9a-zA-Z]{1,4})-([0-9]{2,5})(.*)')
        match = pattern.match(file_name)
        if match:
            num = match.group(2)
        else:
            num = ""
        return num

    @staticmethod
    def count_file():
        output = open('data.txt', 'w')
        base_dir = Config.get_config_field()['updating_dir']
        for DIR in os.listdir(base_dir):
            key = list(filter(lambda x: x.endswith(".jpg"), os.listdir(base_dir + DIR)))
            text = DIR + ' ' + str(len(key)) + '\n'
            output.write(text)
        output.close()

    @staticmethod
    def delete_extra_file(key, dst_dir):
        path = Utility.get_download_path(dst_dir, key)
        l = os.listdir(path)
        count = len(l)
        if count > 0:
            for i in range(1, count):
                extra_pic = l[-i]
                if ".txt" == os.path.splitext(extra_pic)[1]:
                    try:
                        os.remove(path + extra_pic)
                    except Exception as e:
                        logging.error(e)
                else:
                    break

    @staticmethod
    def move_pics():
        base_dir = Config.get_config_field()["download_dir"]
        l = os.listdir(base_dir)
        for pic in l:
            key = Utility.find_key(pic)
            if not key == "":
                src_path = os.path.join(base_dir, pic)
                dst_path = os.path.join(base_dir, key)
                if not os.path.exists(dst_path):
                    os.mkdir(dst_path)
                shutil.move(src_path, dst_path)

    @staticmethod
    def var_to_str(attribute):
        name = [k for k, v in locals().items() if v is attribute][0]
        return name

    @staticmethod
    def get_download_path(dst_dir, key):
        if dst_dir == 'download':
            download_path = Config.get_config_field()["download_dir"] + key + "/"
        elif dst_dir == 'done':
            download_path = Config.get_config_field()["done_dir"] + key + "/"
        elif dst_dir == 'updating':
            download_path = Config.get_config_field()["updating_dir"] + key + "/"
        else:
            download_path = ''
        return download_path
