# encoding: utf-8
"""
@author: jinlin.xiao
@file: config.py
@time: 2019/4/19 11:30 AM
@desc:
 配置需要初始化的logger以及level

"""
import logging

HOST = "0.0.0.0"
PORT = 9801

LoggerInitConfig = {
    # name: {config1: val, config2: val}
    # must config app
    'app': {
        'level': logging.DEBUG,
        'format': '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
    },
    'test_a': {
        'level': logging.DEBUG,
        'format': '%(asctime)s [%(levelname)s] %(message)s'
    },
    'test_p': {
        'level': logging.INFO,
        'format': '%(asctime)s [%(levelname)s] %(message)s'
    }
}

if __name__ == "__main__":
    for key, val in LoggerInitConfig.iteritems():
        print(key)
        print(val)
