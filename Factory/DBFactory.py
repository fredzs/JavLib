import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBFactory(object):
    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://root:Fred1234@localhost:3306/jav')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建session对象:
    db_session = DBSession()

    @staticmethod
    def get_db_session():
        return DBFactory.db_session

    @staticmethod
    def close_session():
        DBFactory.db_session.close()
        logging.info("关闭数据库连接。")
