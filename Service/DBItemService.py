import logging

from mysql.connector import IntegrityError
from sqlalchemy import func

from Entity.Statistic import Statistic
from Factory.DBFactory import DBFactory
from ORM.DBItem import DBItem


class DBItemService(object):
    @staticmethod
    def copy_to_db(item):
        db_item = DBItem()
        db_item.item_code = item.get_code
        db_item.item_key = item.get_key
        db_item.item_title = item.get_title
        db_item.item_date = item.get_date
        db_item.item_duration = item.get_duration
        db_item.item_rank = item.get_rank
        db_item.item_link = item.get_link
        db_item.item_actor = item.get_actor
        return db_item

    @staticmethod
    def db_save(item):
        db_session = DBFactory.get_db_session()
        db_item = DBItemService.copy_to_db(item)
        db_session.add(db_item)
        Statistic.db_item_success()
        logging.info(item.get_code + "已写入数据库缓存")
        return

    @staticmethod
    def db_commit(item_key):
        db_session = DBFactory.get_db_session()
        try:
            db_session.flush()
            db_session.commit()
            logging.info(item_key + "已提交数据库'items'")
        except IntegrityError as e:
            db_session.rollback()
            Statistic.db_item_failed()
            logging.error("记录重复")
            logging.error(e)
        except Exception as e:
            Statistic.db_item_failed()
            logging.error("数据库写入失败！")
            logging.error(e)

    @staticmethod
    def db_find_max_date(item_key):
        db_session = DBFactory().get_db_session()
        query = db_session.query(DBItem.item_date)
        result = query.order_by(DBItem.item_code.desc()).filter(DBItem.item_key == item_key).limit(1).first()
        return result.item_date

    @staticmethod
    def db_find_min_code(item_key):
        db_session = DBFactory().get_db_session()
        query = db_session.query(DBItem.item_code)
        result = query.order_by(DBItem.item_code.asc()).filter(DBItem.item_key == item_key).limit(1).first()
        if result is not None:
            return result.item_code
        else:
            return item_key + '-001'

    @staticmethod
    def db_find_max_code(item_key):
        db_session = DBFactory().get_db_session()
        query = db_session.query(DBItem.item_code).order_by(DBItem.item_code.desc())\
            .filter(DBItem.item_key == item_key)\
            .limit(1)
        result = query.first()
        if result is not None:
            return result.item_code
        else:
            return item_key + '-000'

    @staticmethod
    def db_find_attribute(item_code, attribute):
        db_session = DBFactory().get_db_session()
        query = db_session.query(attribute).filter(DBItem.item_code == item_code)
        logging.info(query)
        result = query.first()
        return result[0]

    @staticmethod
    def db_find_key_total(item_key):
        db_session = DBFactory().get_db_session()
        query = db_session.query(func.count('*'))
        result = query.filter(DBItem.item_key == item_key).first()
        return result[0]

    @staticmethod
    def db_if_code_exist(item_code):
        db_session = DBFactory().get_db_session()
        query = db_session.query(func.count('*'))
        result = query.filter(DBItem.item_code == item_code).first()
        return result[0]

# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
# item = session.query(DBItem).filter(DBItem.item_key == 'ABA').all()
# 打印类型和对象的name属性:
# print('type:', type(DBItem))
# for i in item:
    # print('name:', i.item_title)
# 关闭Session:
# session.close()
