#!/usr/bin/env python3
import logging
import os
import warnings
from time import sleep

import requests

from Entity.Config import Config
from Entity.Item import *
from Entity.Key import KeySet
from Entity.Statistic import Statistic
from Entity.Status import Status
from Factory.DBFactory import DBFactory
from Factory.LogFactory import LogFactory
from Service.ConfigService import ConfigService
from Service.DBItemService import DBItemService
from Service.DBKeyService import DBKeyService
from Service.ItemService import ItemService
from Service.NetworkService import NetworkService
from Service.StatisticsService import StatisticsService
from Utility.Utility import Utility

########################################################################################################
warnings.filterwarnings("ignore")
ConfigService().init()
DBFactory()
Statistic()
LogFactory().init()
retry = int()
########################################################################################################


def search_by_code(item, image, dst_dir):
    result = Status.ERROR
    sleep(1)
    db = DBItemService.db_if_code_exist(item.get_code)
    try:
        code = item.get_code
        item_html = NetworkService.get_search_html(code)
        soup = BeautifulSoup(item_html.text, "html.parser")

        div_videos = soup.find_all("div", class_='videos')
        if len(div_videos) > 0:  # 结果不唯一时有videos
            div_video = div_videos[0].find_all("div", class_="video")
            if len(div_video) > 0:  # 多个结果时有video
                for video in div_video:
                    html_code = video.a.div.text
                    if item.match(html_code):
                        i_href = video.a.get('href')
                        logging.info("存在多个结果，重定向中。。。")
                        item_html = NetworkService.get_base_html(i_href, code)
                        soup = BeautifulSoup(item_html.text, "html.parser")
                        result = Status.SUCCESS
                        break
            if not result == Status.SUCCESS:  # 无结果时无video
                logging.warning(code + "不存在，跳过")
                result = Status.CODE_NOT_EXIST
                global retry
                retry += 1
        else:  # 直接找到item
            logging.info("直接找到")
            result = Status.SUCCESS
        if Status.SUCCESS == result:
            retry = 0
            item.set_soup(soup)
            path = Utility.get_download_path(dst_dir, item.get_key)
            if os.path.exists(path + soup.find("div", id='video_title').a.string + ".jpg"):
                logging.info(item.get_code + "已存在，跳过图片下载")
                result = Status.DUPLICATE
    except requests.exceptions.RequestException as e:
        logging.error("请求发生错误" + item.get_code)
        logging.error(e)
        result = Status.REQUEST_FAILED
    except Exception as e:
        logging.error(e)
    finally:
        handle_status(item, result, db, image, dst_dir)


def search_codes():
    logging.info('----------开始按Code搜索----------')
    for i, code in enumerate(Config.get_code_list()):
        if code != "":
            download_path = Config.get_config_field()["download_dir"] + Utility.find_key(code) + '/'
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            global retry
            retry = 0
            item = Item(Utility.find_key(code), Utility.find_num(code))
            if retry > int(Config.get_config_field()["retry_times"]):
                break
            search_by_code(item, True, "download")
            if i % 20 == 19:
                DBItemService.db_commit(item.get_key)
    logging.info('按Code搜索结束。')


def search_keys():
    logging.info('----------开始按Key搜索----------')
    for keyset in Config.get_key_list():
        if not os.path.exists(keyset.get_key_path):
            os.makedirs(keyset.get_key_path)
        global retry
        retry = 0
        for cur_num in range(keyset.get_start, keyset.get_end):
            item = Item(keyset.get_key, cur_num)
            if retry > int(Config.get_config_field()["retry_times"]):
                logging.info("番号处理完毕" + keyset.get_key)
                break
            search_by_code(item, True, 'download')
            if cur_num % 20 == 0:
                DBItemService.db_commit(item.get_key)
        DBItemService.db_commit(keyset.get_key)
        Utility.delete_extra_file(keyset.get_key, 'download')
    logging.info('----------按Key搜索结束----------')


def download_failed():
    logging.info('----------重新处理失败的Code----------')
    todo_list = list()
    failed_list = list()
    with open('failed_list.txt', 'r') as f:
        for line in f:
            todo_list.append(line.strip('\n'))
            failed_list.append(line.strip('\n'))

    i = 0
    for code in todo_list:
        try:
            item = Item(Utility.find_key(code), Utility.find_num(code))
            keyset = KeySet(item.get_key)
            keyset.set_download_path(Config.get_config_field()["download_dir"])
            search_by_code(item, True, 'download')
            if os.path.exists(keyset.get_key_path + item.get_title + ".jpg"):
                failed_list.pop(i)
            else:
                i += 1
        except Exception as e:
            logging.error(e)
        finally:
            DBItemService.db_commit(item.get_key)
            with open('failed_list.txt', 'w') as file:
                for line in failed_list:
                    file.writelines('{0}\n'.format(line))
    logging.info('处理失败的Code结束。')


def db_add():
    logging.info('开始向数据库中导入。')
    base_dir = Config.get_config_field()['arrange_dir']
    for key in os.listdir(base_dir):
        key_dir = base_dir + key
        global retry
        retry = 0
        if os.path.exists(key_dir):
            for i, file in enumerate(filter(lambda x: x.endswith(".jpg"), os.listdir(key_dir))):
                item = Item(Utility.find_key(file), Utility.find_num(file))
                if retry > int(Config.get_config_field()["retry_times"]):
                    logging.info("番号处理完毕" + key)
                    break
                search_by_code(item, False, 'download')
                if i % 5 == 4:
                    DBItemService.db_commit(item.get_key)
        DBItemService.db_commit(key)
    logging.info('----------向数据库中导入结束----------')


def db_update():
    logging.info('----------开始整理----------')
    base_dir = Config.get_config_field()['arrange_dir']
    for key in os.listdir(base_dir):
        db_key = DBKeyService.copy_to_db(key)
        DBKeyService.db_save(db_key)
        DBKeyService.db_commit(db_key.key_)
    logging.info('----------整理结束----------')


def key_check_new():
    logging.info('----------开始更新----------')
    base_dir = Config.get_config_field()['updating_dir']
    updating_list = os.listdir(base_dir)
    # start_index = updating_list.index('NTRD') + 1
    for key in updating_list:
        try:
            start = Utility.find_num(DBItemService.db_find_max_code(key)) + 1
            global retry
            retry = 0
            for cur_num in range(start, 1000):
                item = Item(key, cur_num)
                if retry > int(Config.get_config_field()["retry_times"]):
                    logging.info("番号处理完毕" + key)
                    break
                search_by_code(item, True, 'updating')
                if cur_num % 20 == 0:
                    DBItemService.db_commit(item.get_key)
        except Exception as e:
            logging.error(e)
        finally:
            DBItemService.db_commit(key)

            db_key = DBKeyService.copy_to_db(key)
            DBKeyService.db_update(db_key)
            DBKeyService.db_commit(db_key.key_)

            Utility.delete_extra_file(key, 'updating')
    logging.info('----------更新结束----------')


def handle_status(item, status, db, image, dst_dir):
    key_path = Utility.get_download_path(dst_dir, item.get_key)

    if Status.CODE_NOT_EXIST == status:
        with open(key_path + item.get_code + '.txt', 'w') as f:
            f.writelines('{0}\n'.format(item.get_code))
        return

    if Status.REQUEST_FAILED == status:
        with open('failed_list.txt', 'a') as f:
            f.writelines('{0}\n'.format(item.get_code))
        return

    if ItemService.parse_html(item):
        if db == 0:
            DBItemService.db_save(item)
        else:
            logging.info(item.get_code + "已存在于数据库中，跳过写入。")
        if Status.SUCCESS == status and image:
            status = ItemService.save_image(item, dst_dir)
        if Status.SAVE_FAILED == status:
            with open('failed_list.txt', 'a') as f:
                f.writelines('{0}\n'.format(item.get_code))
        if Status.DUPLICATE == status:
            pass
    else:
        status = Status.PARSE_ERROR
        with open('failed_list.txt', 'a') as f:
            f.writelines('{0}\n'.format(item.get_code))
    return status


if "__main__" == __name__:
    logging.info('----------程序开始执行----------')
    # search_codes()
    search_keys()
    # key_check_new()
    #db_update()
    # db_add()
    download_failed()
    logging.info('----------程序执行结束----------')
    StatisticsService.print_statistics()
    DBFactory.close_session()
