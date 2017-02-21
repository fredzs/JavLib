from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class DBItem(Base):
    # 表的名字:
    __tablename__ = 'items'

    # 表的结构:
    item_code = Column(String(20), primary_key=True)
    item_key = Column(String(10))
    item_title = Column(String(255))
    item_date = Column(Date())
    item_rank = Column(Float())
    item_duration = Column(Integer())
    item_link = Column(String(20))
    item_actor = Column(String(255))

