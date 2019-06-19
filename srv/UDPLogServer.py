# encoding: utf-8
"""
@author: jinlin.xiao
@file: UDPLogServer.py
@time: 2019/4/19 11:21 AM
@desc:
base:
python 2.7

srv 的 main文件，在这里启动一个udp server

#####
client 发送消息格式
Name.Level|Msg

#####
server 端
1、取 | 前面的字符串，然后以 . 分隔， 前面为 logger 的name；后面为log的level
2、根据name取对应的 logger，如果不存在config的keys中，则取 defualt
"""
# python 3 import
# import socketserver
# from socketserver import ThreadingUDPServer
#
import SocketServer
from SocketServer import ThreadingUDPServer
import threading
import logging
import time
import SafeDateFileHandler
from config import LoggerInitConfig, HOST, PORT


def init_logger(p_name, log_conf):
    handler = SafeDateFileHandler.SafeDateFileHandler(p_name)
    handler.setLevel(log_conf.get('level'))  # DEBUG recommend
    formatter = logging.Formatter(log_conf.get('format'))
    handler.setFormatter(formatter)
    now_init_logger = logging.getLogger(p_name)
    now_init_logger.setLevel(log_conf.get('level'))
    now_init_logger.addHandler(handler)


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        """
        write log
        :return:
        """
        log_data = data = self.request[0].strip()
        # socket = self.request[1]
        # current_thread = threading.current_thread()
        # logger.debug("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))

        # 默认的logger和level
        tmp_logger, level = logging.getLogger("app"), 'DEBUG'
        if len(data) > 0 and data.find('|') > 0:
            separator_idx = data.find('|')
            header_str = data[:separator_idx]
            tmp_idx = header_str.rfind('.')
            # support: app.DEBUG or app.sub.DEBUG
            # issue:如果格式正常但获取tmp_logger失败,解决方案：
            # 方案1、继续用默认的logger app ，并且在app后带上name  app.name 的方式将日志写在app文件中
            # 方案2、设置一个default，按照default 初始化一个logger，写在新的文件中
            # 方案2可能带来log文件泛滥，舍弃，采用方案1
            if tmp_idx > 0:  # 找到 . 意味着格式合理
                # 传入的找不到时，使用默认值
                logger_name = header_str[:tmp_idx]
                if logger_name.split('.')[0] in LoggerInitConfig.keys():
                    # 有config
                    tmp_logger = logging.getLogger(logger_name)
                else:
                    # 没有config 修改一下name，方便grep log
                    tmp_logger = logging.getLogger("app.%s" % logger_name)
                level = header_str[tmp_idx + 1:].upper()
                log_data = data[separator_idx + 1:]

        # 利用获取的logger，根据level写不同级别的日志
        if level == 'INFO':
            tmp_logger.info(log_data)
        elif level == 'WARN' or level == 'WARNING':
            tmp_logger.warning(log_data)
        elif level == 'ERROR':
            tmp_logger.error(log_data)
        elif level == 'CRIT' or level == 'CRITICAL':
            tmp_logger.critical(log_data)
        else:
            # 默认按 debug 级别写log
            tmp_logger.debug(log_data)
        # socket.sendto(data.upper(), self.client_address)


def main():
    server = ThreadingUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        logger = logging.getLogger("app")
        logger.info("Server started at {} port {}".format(HOST, PORT))
        # 一个死循环
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()


if __name__ == "__main__":
    # init loggers
    for key, conf in LoggerInitConfig.iteritems():
        init_logger(key, conf)
    # call main function
    main()
