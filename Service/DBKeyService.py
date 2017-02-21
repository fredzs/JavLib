import logging

from mysql.connector import IntegrityError
from sqlalchemy import func

from Entity.Statistic import Statistic
from Factory.DBFactory import DBFactory
from ORM.DBKey import DBKey
from Service.DBItemService import DBItemService
from Utility.Utility import Utility


class DBKeyService(object):
    @staticmethod
    def copy_to_db(key):
        db_key = DBKey()
        db_key.key_ = key
        db_key.total = DBItemService.db_find_key_total(key)
        latest_code = DBItemService.db_find_max_code(key)
        db_key.latest_code = latest_code
        db_key.num_length = len(Utility.find_num_str(db_key.latest_code))
        db_key.start_num = Utility.find_num(DBItemService.db_find_min_code(key))
        db_key.end_num = Utility.find_num(DBItemService.db_find_max_code(key))
        db_key.latest_date = DBItemService.db_find_max_date(key)
        db_key.category = '1'
        db_key.updating = 0
        return db_key

    @staticmethod
    def db_save(db_key):
        db_session = DBFactory.get_db_session()
        db_session.add(db_key)
        Statistic.db_key_success()
        logging.info(db_key.key_ + "已写入数据库缓存")
        return

    @staticmethod
    def db_update(db_key):
        db_session = DBFactory.get_db_session()
        db_session.merge(db_key)
        Statistic.db_key_success()
        logging.info(db_key.key_ + "已写入数据库缓存")
        return

    @staticmethod
    def db_commit(db_key):
        db_session = DBFactory.get_db_session()
        try:
            db_session.flush()
            db_session.commit()
            logging.info(db_key + "已提交数据库'keys_info'")
        except IntegrityError as e:
            db_session.rollback()
            Statistic.db_key_failed()
            logging.error("记录重复")
            logging.error(e)
        except Exception as e:
            Statistic.db_key_failed()
            logging.error("数据库写入失败！")
            logging.error(e)

    @staticmethod
    def db_find_attribute(key, attribute):
        db_session = DBFactory().get_db_session()
        query = db_session.query(attribute).filter(DBKey.key_ == key)
        result = query.first()
        return result[0]

    @staticmethod
    def db_if_key_exist(key):
        db_session = DBFactory().get_db_session()
        query = db_session.query(func.count('*'))
        result = query.filter(DBKey.key_ == key).first()
        return result[0]
