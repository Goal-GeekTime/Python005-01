#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File      : hk_redis_count.py
@Time      : 2020/12/26 23:42:30
@Author    : Goal
@Release   : 2.0
@Desc      : 使用 Python+redis 实现高并发的计数器功能
@Reference : https://github.com/boyshen/Python005-01/tree/main/week05
"""


import redis
import random
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


class RedisCount(object):

    def __init__(self, host, port, password, db):
        self._host = host
        self._port = port
        self._password = password
        self._db = db
        self.video = 'video'

        self.client = redis.Redis(host=self._host, port=self._port, password=self._password)

    def add_video(self, video_id):
        """
        添加视频信息到 redis
        :param video_id: (int or str)
        :return: (bool)
        """
        result = False

        # 类型转换
        if isinstance(video_id, int):
            video_id = str(video_id)

        # 查看哈希表 key 中，给定域 field 是否存在。
        if self.client.hexists(self.video, video_id):
            print("video: {} Already Exists".format(video_id))
            # 存在记录，暂时不清空
            return result
            
            # 存在即情况
            # print("Clear existing keys: {}".format(video_id))
            # self.client.hdel(self.video, video_id)

        try:
            self.client.hset(self.video, video_id, '0')
        except Exception as e:
            raise e
        else:
            result = True
        finally:
            return result

    def counter(self, video_id):
        """
        视频计数
        :param video_id: (str)
        :return: (int)
        """
        value = 0
        if isinstance(video_id, int):
            video_id = str(video_id)

        try:
            if self.client.hexists(self.video, video_id):
                self.client.hincrby(self.video, video_id, amount=1)
                value = int(self.client.hget(self.video, video_id))
        except Exception as e:
            raise e
        finally:
            return value

    def close(self):
        self.client.close()


def main(config):
    videos = [ x for x in range(1001, 1006) ]
    redis_count = RedisCount(host=config['host'], port=config['port'], password=config['password'], db=config['db'] )

    try:
        for video in videos:
            redis_count.add_video(video)

        for i in range(10):
            index = random.randrange(0, len(videos))
            video = videos[index]
            result = redis_count.counter(video)
            print("video({}), count:{}".format(video, result))

    except Exception as e:
        raise e
    finally:
        redis_count.close()


# main
if __name__ == '__main__':
    config = read_config(CONFIG, 'redis_default')
    main(config)
