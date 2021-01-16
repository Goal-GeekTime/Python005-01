#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File      : timer.py
@Time      : 2021/01/16 17:13:22
@Author    : Goal
@Release   : 1.0
@Desc      : 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
@Reference : 
"""

import time
from functools import wraps

sltime = 2

def getLogTime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

def timer(func):
    @wraps(func)
    def in_dec(*args, **kwargs):
        start = int(time.time())
        print(f"开始运行函数: {func.__name__}, 时间: {getLogTime()}")
        func(*args, **kwargs)
        print("The consuming time is: %ds" % (int(time.time() - start)))
    return in_dec

@timer                                    # 装饰器函数已经执行
def funsleep(time1):
    time.sleep(time1)

@timer
def test(num):
    for i in range(num):
        print("run count: {}".format(i))
        time.sleep(1)

# main
if __name__ == "__main__":
    try:
        sltime = int(input("Please input a time:"))
    except Exception:
        print("\033[31;1m输入非整数，自动赋值 :{}s. \033[0m".format(sltime))
    funsleep(sltime)

    print("")
    test(3)