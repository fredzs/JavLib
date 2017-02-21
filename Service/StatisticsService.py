import logging

from Entity.Statistic import Statistic


class StatisticsService(object):
    @staticmethod
    def print_statistics():
        logging.info('下载成功：' + str(Statistic.get_download_success()))
        logging.info('下载失败：' + str(Statistic.get_download_failed()))
        logging.info('Item数据库导入成功：' + str(Statistic.get_item_success()))
        logging.info('Item数据库导入失败：' + str(Statistic.get_item_failed()))
        logging.info('Key数据库导入成功：' + str(Statistic.get_key_success()))
        logging.info('Key数据库导入失败：' + str(Statistic.get_key_failed()))
