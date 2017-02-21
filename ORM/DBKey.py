from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class DBKey(Base):
    # 表的名字:
    __tablename__ = 'keys_info'

    # 表的结构:
    key_ = Column(String(10), primary_key=True)
    total = Column(Integer())
    num_length = Column(Integer())
    start_num = Column(Integer())
    end_num = Column(Integer())
    latest_code = Column(String(20))
    latest_date = Column(Date())
    category = Column(String(100))
    updating = Column(Integer())

