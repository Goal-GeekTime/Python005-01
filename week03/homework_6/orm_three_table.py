#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File      : orm_three_table.py
@Time      : 2020/12/13 17:45:20
@Author    : Goal
@Release   : 1.0
@Desc      : 
@Reference : 
"""

import datetime
from configparser import ConfigParser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, CHAR, BigInteger, TIMESTAMP, Date, ForeignKey
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

CONFIG = './config.ini'

Base = declarative_base()


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


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
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return "<id:%s name:%s>" %(self.id, self.name)

class UserAsset(Base):
    """
    # 资产表: id、用户id、总资产
    """
    __tablename__ = 'assets'
    id = Column(BigInteger(), primary_key=True)
    user_id = Column(Integer,ForeignKey("accounts.uid"))
    total_asset = Column(BigInteger())

    account = relationship("UserTable", backref="asset")

    # def __repr__(self):
    #     return "<id:%s name:%s>" %(self.id, self.account_alias.name, )

    def __repr__(self):
        return "<id:%s >" %(self.id )

# class UserAudit(Base):
# """
# # 审计表: id、转账 id，被转账 id，转账金额、字段创建时间
# """
# __tablename__ = 'audit'
# id = Column(BigInteger(), primary_key=True)
# tran_id = Column(Integer,ForeignKey("account.id") ,comment='转账id') 
# des_id = Column(Integer,ForeignKey("account.id") ,comment='被转账转账id') 
# create_time = Column(TIMESTAMP(3), default=get_time())


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


config = read_config(CONFIG, 'mysql')
print(config)
# dburl = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format( user=config['user'], password=config['password'], host=config['host'], port=config['port'], database=config['database'] )

dburl = "mysql+pymysql://{}:{}@{}:{}/{}".format( config['user'], config['password'], config['host'], config['port'], config['database'])


engine = create_engine(dburl, encoding='utf-8', echo=False)
Base.metadata.create_all(engine)    
