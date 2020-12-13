#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File      : orm_learn.py
@Time      : 2020/12/13 16:55:34
@Author    : Goal
@Release   : 1.0
@Desc      : SQLAlchemy 创建表、实现增删改查.
@Reference : https://github.com/boyshen/Python005-01/tree/main/week03.
"""


import random
import datetime
from configparser import ConfigParser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, CHAR, BigInteger, TIMESTAMP, Date
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


# 定义表:
class UserTable(Base):
    """
    # 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
    """
    __tablename__ = 'user'
    uid = Column(BigInteger(), primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer())
    birthday = Column(Date())
    gender = Column(CHAR(10))
    education = Column(String(50))
    create_time = Column(TIMESTAMP(3), default=get_time())
    update_time = Column(TIMESTAMP(3), onupdate=get_time(), default=get_time())

    def __repr__(self):
        return "<User(uid:{}, " \
               "name:{}, " \
               "age:{}, " \
               "birthday:{}, " \
               "gender:{}, " \
               "education:{}, " \
               "create_time:{}, " \
               "update_time:{})>".format(self.uid,
                                         self.name,
                                         self.age,
                                         self.birthday,
                                         self.gender,
                                         self.education,
                                         self.create_time,
                                         self.update_time)



# 定义操作类:
class User(object):
    WOMAN = "woman"
    MAN = 'man'

    def __init__(self, user, password, host, port, database, echo=False):
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__database = database
        self.__echo = echo

        self.mysql_url = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(self.__user,
                                                                                 self.__password,
                                                                                 self.__host,
                                                                                 self.__port,
                                                                                 self.__database)
        self.__init_engine()

    def __init_engine(self):
        self.engine = create_engine(self.mysql_url, echo=self.__echo, encoding='UTF-8')
        Base.metadata.create_all(self.engine)
        self.session_class = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session_class()

    def add(self, name, age, birthday, gender, education):
        """
        :param name: (str) 姓名
        :param age: (int) 年龄
        :param birthday: (str) 格式例如："1993-02-23"
        :param gender: (str) 性别
        :param education: (str) 学历
        :return: (bool)
        """
        session = self.get_session()
        user_info = UserTable(name=name, age=age, birthday=birthday, gender=gender, education=education)
        try:
            session.add(user_info)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(e)
            print("Add User Failed: {}".format(user_info))
            return False

    def query_all_info(self):
        """
        查询所有用户信息
        :return: (tuple)
        """
        session = self.get_session()
        try:
            res = (result for result in session.query(UserTable))
            session.commit()
            return res
        except Exception as e:
            print(e)
            return ()

    def condition_query(self, birthday):
        """
        指定出生日期做条件查询
        :param birthday: (str)
        :return: (tuple)
        """
        session = self.session_class()
        try:
            res = (result for result in session.query(UserTable).filter(UserTable.birthday > birthday))
            session.commit()
            return res
        except Exception as e:
            print(e)
            return ()

    def all_numbers_by_gender(self):
        """
        根据性别统计用户数量
        :return: (tuple)
        """
        session = self.session_class()
        try:
            res = (result for result in session.query(UserTable.gender, func.count(UserTable.gender)).group_by(UserTable.gender))
            session.commit()
            return res
        except Exception as e:
            print(e)
            return ()

    def all_numbers_by_education(self, is_desc=False):
        """
        根据学历统计用户数量
        :param is_desc: (bool) 是否返回降序
        :return: (tuple)
        """
        session = self.session_class()
        try:
            query = session.query(UserTable.education, func.count(UserTable.education)).group_by(UserTable.education)
            if is_desc:
                query = query.order_by(desc(func.count(UserTable.education)))
            else:
                query = query.order_by(func.count(UserTable.education))

            res = (result for result in query)
            session.commit()
            return res
        except Exception as e:
            print(e)
            return ()


def test_add(num):
    test_name = ('张三', '李四', '王五', '赵六')
    test_age = (27, 28, 29, 30)
    test_gender = (User.WOMAN, User.MAN)
    test_birthday = ("1993-02-23", "1992-01-28", "1991-10-21", "1990-08-04")
    test_education = ('本科', '专科', '博士', '研究生')

    config = read_config(CONFIG, 'mysql')
    user = User(user=config['user'], password=config['password'], host=config['host'], port=config['port'], database=config['database'])
    for i in range(num):
        index = random.randint(0, len(test_name) - 1)
        gender_index = random.randint(0, len(test_gender) - 1)
        user.add(name=test_name[index],
                 age=test_age[index],
                 birthday=test_birthday[index],
                 gender=test_gender[gender_index],
                 education=test_education[index])


def test_query():
    config = read_config(CONFIG, 'mysql')
    user = User(user=config['user'], password=config['password'], host=config['host'], port=config['port'], database=config['database'])

    for result in user.query_all_info():
        print(result)


def test_all_numbers_by_gender():
    config = read_config(CONFIG, 'mysql')
    user = User(user=config['user'], password=config['password'], host=config['host'], port=config['port'], database=config['database'])

    for result in user.all_numbers_by_gender():
        print(result)


def test_all_numbers_by_education():
    config = read_config(CONFIG, 'mysql')
    user = User(user=config['user'], password=config['password'], host=config['host'], port=config['port'], database=config['database'])

    for result in user.all_numbers_by_education(True):
        print(result)

    for result in user.all_numbers_by_education(False):
        print(result)


def test_condition_query():
    config = read_config(CONFIG, 'mysql')
    user = User(user=config['user'], password=config['password'], host=config['host'], port=config['port'], database=config['database'])

    for result in user.condition_query('1992.01-02'):
        print(result)


if __name__ == '__main__':
    test_add(30)
    test_query()
    test_all_numbers_by_gender()
    test_all_numbers_by_education()
    test_condition_query()


