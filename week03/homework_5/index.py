#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      : index.py
@Time      : 2020/12/13 16:02:17
@Author    : Goal
@Release   : 1.0
@Desc      : 用于创建有索引、无索引的俩张表，同时导入测试数据.
@Reference : https://github.com/boyshen/Python005-01/tree/main/week03.
'''

import random
import pymysql
import datetime
from tqdm import tqdm
from configparser import ConfigParser

CONFIG = './config.ini'


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


# 读取 ini 格式的配置文件
def read_config(config, section):
    parser = ConfigParser()
    parser.read(config)

    if parser.has_section(section):
        items = parser.items(section)
    else:
        raise "Exception: {} File Not Found section:{}".format(config, section)
    return dict(items)


class User(object):
    WOMAN = 'woman'
    MAN = 'man'

    def __init__(self, host, port, user, password, database):
        self.table = 'user'
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database
        self.charset = 'utf8mb4'

        self.__init_connection__()
        self.create_table_has_index()
        self.create_table_no_index()

    def __init_connection__(self):
        self.connection = pymysql.connect(host=self.__host,
                                          port=self.__port,
                                          user=self.__user,
                                          password=self.__password,
                                          db=self.__database,
                                          charset=self.charset,
                                          cursorclass=pymysql.cursors.DictCursor)

    def create_table_has_index(self):
        try:
            with self.connection.cursor() as cursor:
                sql = "CREATE TABLE IF NOT EXISTS user_has_index(" \
                      "`uid` BIGINT(20) NOT NULL AUTO_INCREMENT," \
                      "`name` VARCHAR(50) NOT NULL," \
                      "PRIMARY KEY(`uid`)," \
                      "KEY (`name`)" \
                      ")"
                cursor.execute(sql)
        except Exception as e:
            raise e

    def create_table_no_index(self):
        try:
            with self.connection.cursor() as cursor:
                sql = "CREATE TABLE IF NOT EXISTS user_no_index(" \
                      "`uid` BIGINT(20) NOT NULL AUTO_INCREMENT," \
                      "`name` VARCHAR(50) NOT NULL," \
                      "PRIMARY KEY(`uid`)" \
                      ")"
                cursor.execute(sql)
        except Exception as e:
            raise e

    def insert(self, name):
        try:
            with self.connection.cursor() as cursor:
                # sql = "INSERT INTO `user` " \
                #       "(`name`, `age`, `birthday`, `gender`, `education`, `create_time`, `update_time`) " \
                #       "VALUES (%s, %s, %s, %s, %s, %s, %s)"

                sql = "INSERT INTO `user_no_index` (`name`) VALUES (%(name)s)"
                args = {'name': name}
                cursor.execute(sql, args)

                sql = "INSERT INTO `user_has_index` (`name`) VALUES (%(name)s)"
                cursor.execute(sql, args)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    def close(self):
        self.connection.close()


def t_insert(num):
    last_name = ('Nabila', 'Mora', 'Radinka', 'Tabitha', 'Vivienne', 'Abejundio', 'Bakari', 'Caius', 'Edan', 'Haines')
    fast_name = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'w')

    config = read_config(CONFIG, 'mysql')
    print(config)
    user = User(user=config['user'], password=config['password'], host=config['host'], port=int(config['port']),
                database=config['database'])
    try:
        for _ in tqdm(range(num)):
            i = random.randint(0, len(last_name) - 1)
            j = random.randint(0, len(fast_name) - 1)
            _name = last_name[i] + '_' + fast_name[j]
            user.insert(name=_name)
    except Exception as e:
        raise e
    finally:
        user.close()


if __name__ == '__main__':
    t_insert(30000)
