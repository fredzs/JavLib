from sqlalchemy import func

from Factory.DBFactory import DBFactory
from ORM.DBItem import DBItem
from ORM.DBKey import DBKey
from Service.DBItemService import DBItemService
from Service.DBKeyService import DBKeyService
from Utility.Utility import Utility


def func1():
    failed_list = list()
    with open('failed_list.txt', 'r') as f:
        for line in f:
            failed_list.append(line.strip('\n'))
    for i, code in enumerate(failed_list):
        if "BGN-0372" in code:
            failed_list.pop(i)
    with open('failed_list.txt', 'w') as f:
        for line in failed_list:
            f.writelines('{0}\n'.format(line))


def func2(key, attribute):
    db_session = DBFactory().get_db_session()
    # query_sql = 'SELECT item_date from items where item_key = :item_key order by item_code desc'
    # db_session.execute(query_sql, {'item_key': item_key})
    query = db_session.query(attribute).filter(DBKey.key_ == key)
    print(query)
    result = query.first()
    print(result[0])


def db_if_code_exist(item_code):
    db_session = DBFactory().get_db_session()
    query = db_session.query(func.count('*'))
    result = query.filter(DBItem.item_code == item_code).first()
    return result[0]

if "__main__" == __name__:
    # print(db_if_code_exist('AAJ'))
    func2('ABA', 'latest_date')

