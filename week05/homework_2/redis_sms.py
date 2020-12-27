#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File      : hk_redis_count.py
@Time      : 2020/12/26 23:42:30
@Author    : Goal
@Release   : 2.0
@Desc      : 在使用短信群发业务时，公司的短信接口限制接收短信的手机号，每分钟最多发送五次，请基于 Python 和 redis 实现如下的短信发送接口：
@Reference : https://github.com/boyshen/Python005-01/tree/main/week05
"""


import redis
import random
import string
from configparser import ConfigParser

CONFIG = './config.ini'


def read_config(file, section):
    parser = ConfigParser()
    parser.read(file)
    if parser.has_section(section):
        items = parser.items(section)
    else:
        raise Exception("{} not found in the {} file".format(section, file))
    return dict(items)


import redis
import random
import time


# 随机生成手机号码
def phone_num():
    all_phone_nums=set()
    num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187', '188',
    '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']

    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits,8))
    res = start+end+'\n'
    return res


class RedisMessage(object):
    def __init__(self, host, port, password, db, count=5, time_limit=1):
        """
        :param host: (str) Redis host
        :param port: (int) Redis 端口
        :param password: (str) Redis 密码
        :param count: (int) 限制次数
        :param time_limit: (int) 限制时间，单位分钟
        """
        self._host = host
        self._port = port
        self._password = password
        self._db = db
        self.count = count
        self.time_limit = time_limit

        self.message_count = 'message_count'
        self.message_time = 'message_time'

        self.client = redis.Redis(host=self._host, port=self._port, password=self._password)

    def send_sms(self, telephone_number, content, key=None):
        """
        发送消息
        :param telephone_number: (str)
        :param content: (str)
        :param key: (None)
        :return: (bool)
        """
        # 获取当前时间
        current_time = int(time.time())

        if self.client.hexists(self.message_count, telephone_number):
            msg_count = int(self.client.hget(self.message_count, telephone_number))
            msg_time = int(self.client.hget(self.message_time, telephone_number))

            # 获取时间间隔
            interval_time = current_time - msg_time

            # 在限制时间发送
            if interval_time <= self.time_limit * 60:
                # 检查发送的次数是否达到限制
                if msg_count < self.count:
                    self.client.hset(self.message_count, telephone_number, msg_count + 1)
                    flag = True
                else:
                    flag = False
            # 已经过了限制时间。可以重新发送
            else:
                # 更新重新发送的时间和次数
                self.client.hset(self.message_count, telephone_number, 1)
                self.client.hset(self.message_time, telephone_number, current_time)
                flag = True

        else:
            # 第一次发送
            self.client.hset(self.message_count, telephone_number, 1)
            self.client.hset(self.message_time, telephone_number, current_time)
            flag = True

        if flag:
            print("{} 发送成功！context: {}".format(telephone_number, content))
        else:
            print("{} 在 {} 分钟内发送次数超过 {} 次, 请等待 {} 分钟".format(telephone_number, self.time_limit, self.count,
                                                             self.time_limit))

        return flag

    def close(self):
        self.client.close()


def main(config):
    kwconf = dict( host=config['host'], port=config['port'], password=config['password'], db=config['db'], count=int(config['count']), time_limit=int(config['time_limit']) )
    redis_message = RedisMessage(**kwconf)
    telephone_numbers = [phone_num() for i in range(5) ]

    try:
        for i in range( int(kwconf['time_limit']) * 60 * 2):
            index = random.randrange(0, len(telephone_numbers))
            telephone_num = telephone_numbers[index]
            redis_message.send_sms(telephone_num, 'hello world')
            time.sleep(1)

            if (i + 1) % 60 == 0:
                print()
                print("{} minute later ...".format((i + 1) / 60))

    except Exception as e:
        raise e
    finally:
        redis_message.close()


if __name__ == '__main__':
    config = read_config(CONFIG, 'redis_default')
    # print(config)
    main(config)
