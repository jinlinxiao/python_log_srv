# encoding: utf-8
"""
@author: jinlin.xiao
@file: LogApiNoColorama.py
@time: 2019/4/19 11:45 AM
@desc:
"""

import socket

# 配置
HOST, PORT = "localhost", 9801  # 服务器侦听的IP和端口


class LogClient(object):

    SystemName = 'app'  # 当前系统的名称
    # 控制变量
    Console = False     # 是否在控制台打印日志，默认不开启
    SendServer = True  # 是否发往服务器端，默认开启

    SendBuf = 1024     # client单次发给server端的长度，msg太长时，会出现OSError

    def __init__(self, name=None, **kwargs):
        self.log_srv_address = (HOST, PORT)
        # 可以重置SystemName
        if name:
            self.SystemName = name
        if 'console' in kwargs:
            self.Console = kwargs.get('console', False)
        if 'send_srv' in kwargs:
            self.SendServer = kwargs.get('send_srv', True)

    def set_console(self, console):
        self.Console = console

    def set_send_server(self, send_server):
        self.SendServer = send_server

    def send_log(self, level, msg):
        """
        send log to log server
        :param level:
        :param msg:
        :return:
        """
        if self.Console:
            print_msg = "%s|%s" % (level, msg)
            print(print_msg)
        if self.SendServer:
            send_msg = "%s.%s|%s" % (self.SystemName, level, msg)
            sock_cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                total_send_len = len(send_msg)
                if total_send_len > self.SendBuf:
                    sended_msg_len = 0
                    send_times = 0   # 控制一次最多发送10次 self.SendBuf * 10
                    while sended_msg_len + self.SendBuf < total_send_len and send_times < 10:
                        try:
                            sock_cli.sendto(send_msg[sended_msg_len:sended_msg_len + self.SendBuf], (HOST, PORT))
                        finally:
                            sended_msg_len += self.SendBuf
                            send_times += 1
                else:
                    sock_cli.sendto(send_msg, (HOST, PORT))
                # no need call recvfrom function,there is no return from log server.
            except TypeError:  # python 3
                total_send_len = len(send_msg)
                if total_send_len > self.SendBuf:
                    sended_msg_len = 0
                    send_times = 0   # 控制一次最多发送10次 self.SendBuf * 10
                    while sended_msg_len + self.SendBuf < total_send_len and send_times < 10:
                        try:
                            this_send_msg = send_msg[sended_msg_len:sended_msg_len + self.SendBuf]
                            sock_cli.sendto(bytes(this_send_msg, encoding="utf8"), (HOST, PORT))
                        finally:
                            sended_msg_len += self.SendBuf
                            send_times += 1
                else:
                    sock_cli.sendto(bytes(send_msg, encoding="utf8"), (HOST, PORT))
            except Exception as err:
                print("sendto Exception: {0}".format(err))
            finally:
                sock_cli.close()

    def debug(self, msg):
        self.send_log('DEBUG', msg)

    def info(self, msg):
        self.send_log('INFO', msg)

    def warn(self, msg):
        self.send_log('WARNING', msg)

    def error(self, msg):
        self.send_log('ERROR', msg)

    def critical(self, msg):
        self.send_log('CRITICAL', msg)


log_cli = LogClient()


def debug(msg):
    log_cli.debug(msg)


def info(msg):
    log_cli.info(msg)


def warn(msg):
    log_cli.warn(msg)


def error(msg):
    log_cli.error(msg)


def critical(msg):
    log_cli.critical(msg)
