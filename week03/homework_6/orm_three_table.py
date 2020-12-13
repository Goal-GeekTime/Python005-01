#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File      : orm_three_table.py
@Time      : 2020/12/13 17:45:20
@Author    : Goal
@Release   : 1.0
@Desc      : 创建3张表：accounts| assets |audits, 并且实现一笔转账.
@Reference : 
"""

import sys
import datetime
from configparser import ConfigParser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, CHAR, BigInteger, TIMESTAMP, Date, ForeignKey
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.orm import relationship

CONFIG = './config.ini'

Base = declarative_base()


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

# 读取配置文件
def read_config(file, section):
    parser = ConfigParser()
    parser.read(file)
    if parser.has_section(section):
        items = parser.items(section)
    else:
        raise Exception("{} not found in the {} file".format(section, file))
    return dict(items)


# 定义表
class UserTable(Base):
    """
    # 用户表: id、用户名
    """
    __tablename__ = 'accounts'
    uid = Column(BigInteger(), primary_key=True)
    name = Column(String(32), nullable=False)

    def __repr__(self):
        return "<id :%s name :%s>" %(self.uid, self.name)

class UserAsset(Base):
    """
    # 资产表: id、用户id、总资产
    """
    __tablename__ = 'assets'
    id = Column(BigInteger(), primary_key=True)
    total_asset = Column(BigInteger(), nullable=False)
    user_id = Column(BigInteger, ForeignKey("accounts.uid")) 

    account = relationship("UserTable", backref="asset")

    def __repr__(self):
        return "<id:%s name:%s>" %(self.id, self.account.name)

class UserAudit(Base):
    """
    # 审计表: id、转账 id，被转账 id，转账金额、字段创建时间
    """
    __tablename__ = 'audits'
    id = Column(BigInteger(), primary_key=True)
    create_time = Column(TIMESTAMP(3), default=get_time())
    tran_id = Column(BigInteger,ForeignKey("accounts.uid") ,comment='转账id') 
    des_id = Column(BigInteger,ForeignKey("accounts.uid") ,comment='被转账转账id') 
    


# engine = create_engine("mysql+pymysql://root:bridge@192.168.80.10/ibcp", encoding='utf-8', echo=False)


# class User(object):
#     def __init__(self, user, password, host, port, database, echo=False):
#         self.__user = user
#         self.__password = password
#         self.__host = host
#         self.__port = port
#         self.__database = database
#         self.__echo = echo

#         self.mysql_url = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(self.__user,
#                                                                                  self.__password,
#                                                                                  self.__host,
#                                                                                  self.__port,
#                                                                                  self.__database)
#         self.__init_engine()

#     def __init_engine(self):
#         self.engine = create_engine(self.mysql_url, echo=self.__echo, encoding='UTF-8')
#         Base.metadata.create_all(self.engine)
#         self.session_class = sessionmaker(bind=self.engine)
    
#     def get_session(self):
#         return self.session_class()



# # main
# def main():
#     config = read_config(CONFIG, 'mysql')
#     user = User(user=config['user'], password=config['password'], host=config['host'], port=config['port'], database=config['database'])

# if __name__ == '__main__':
#     main()




# main: 创建表
config = read_config(CONFIG, 'mysql')
print(config)
# dburl = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format( user=config['user'], password=config['password'], host=config['host'], port=config['port'], database=config['database'] )

dburl = "mysql+pymysql://{}:{}@{}:{}/{}".format( config['user'], config['password'], config['host'], config['port'], config['database'])


engine = create_engine(dburl, encoding='utf-8', echo=False)
Base.metadata.create_all(engine)    




# 插入数据
# account1 = UserTable(name='A小李')
# account2 = UserTable(name='B小张')
# account3 = UserTable(name='C小王')


# assets1 = UserAsset('500', 1)
# assets2 = UserAsset('100', 2)
# assets3 = UserAsset('50', 3)

# Session_class = sessionmaker(bind=engine)
# Session = Session_class()

# Session.add_all([ account1,  account2, account3, assets1, assets2, assets3 ])
# Session.commit()



# 发起一笔转账
def transferaccounts(tran_id, des_id, tran_money):
    if not moneycount < 1 or moneycount > 20000:
        try:
            tran_count_money = session.query(UserAsset).filter_by(user_id=tran_id).first().total_asset
            if tran_count_money > tran_money:
                query = Session.query(UserAsset) 
                query = query.filter(user_id == tran_id)
                query.update({UserAsset.total_asset: tran_count_money-tran_money  })

                des_count_money = session.query(UserAsset).filter_by(user_id=des_id).first().total_asset
                query = Session.query(UserAsset) 
                query = query.filter(user_id == des_id)
                query.update({UserAsset.total_asset: des_count_money+tran_money })
                Session.commit()
        except Exception as e:
            print(f"转账异常. {e}") 
            Session.rollback()
    else:
        print("转账金额不低于1元，且不大于20000.")
        sys.exit(1)