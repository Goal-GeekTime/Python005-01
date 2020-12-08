#!/usr/bin/env python
# coding=utf-8

"""
    # README
    编写一个函数, 当函数被调用时，将调用的时间记录在日志中, 日志文件的保存位置建议为：/var/log/python- 当前日期 /xxxx.log
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

BaseDir = os.path.dirname(os.path.abspath(__file__))

# return the function name.
def p():
    import sys
    return sys._getframe(1).f_code.co_name

# Configure logging
def set_log(log_base_path = './log/', LoggingLevel = 'INFO'):
    logger = logging.getLogger()
    # File logging
    log_base_path=os.path.abspath(log_base_path)
    this_file_name = os.path.splitext(os.path.basename(__file__))[0]
    date_time = datetime.now().isoformat().replace(':', '-')[:10]
    log_path = os.path.join(log_base_path, 'python-'+date_time)
    print("log_path :", log_path)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file_name = os.path.join(log_path, this_file_name + '.log')
    print('Logging to file:', os.path.abspath(log_file_name))
    print('Logging level:', LoggingLevel)
    fileHandler = logging.FileHandler(filename=log_file_name, encoding='utf-8')
    fileHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s - %(message)s'))
    logger.addHandler(fileHandler)
    # Loggin Level
    logger.setLevel(logging.WARNING)
    if LoggingLevel == 'INFO':
        logger.setLevel(logging.INFO)
    elif LoggingLevel == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    return logger, log_file_name


# Get local file list, return the filesize list.
def get_local_file_list(logger,SrcDir=BaseDir, SrcFileIndex='*', str_key=False):
    __src_file_list = []

    logger.info(f' Function called：{p()}')
    try:
        if SrcFileIndex == "*":                 # '*' 遍历本地目录的所有文件
            for parent, dirnames, filenames in os.walk(SrcDir):
                for filename in filenames:      # 遍历输出文件信息
                    file_absPath = os.path.join(parent, filename)
                    file_relativePath = file_absPath[len(SrcDir) + 1:]
                    file_size = os.path.getsize(file_absPath)
                    key = Path(file_relativePath)
                    if str_key:
                        key = str(key)
                    __src_file_list.append({
                        "Key": key,
                        "Size": file_size
                    })
        else:
            join_path = os.path.join(SrcDir, SrcFileIndex)
            file_size = os.path.getsize(join_path)
            __src_file_list = [{
                "Key": SrcFileIndex,
                "Size": file_size
            }]
    except Exception as err:
        logger.error('Can not get source files. ERR: ' + str(err))
        input('PRESS ENTER TO QUIT')
        sys.exit(0)
    if not __src_file_list:
        logger.error('Source file empty.')
        input('PRESS ENTER TO QUIT')
        sys.exit(0)
    return __src_file_list


# main
if __name__ == '__main__':
    logger, log_file_name = set_log('/var/log')
    file_list = get_local_file_list(logger)

    print(' Get local file list '.center(50, '#'))
    for i in file_list:
        print(i)
