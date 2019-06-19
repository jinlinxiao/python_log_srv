# encoding: utf-8
"""
@author: jinlin.xiao
@file: use_client_sample.py
@time: 2019/4/19 2:30 PM
@desc:
A sample of use UDPLogApi to send log to log srv

"""
from api import LogApi

# 所有的日志都在srv的log目录下

# 默认日志写在 app_YYYYMMDD.log 文件中， %(name)s 输出为 app
LogApi.debug("test debug")
LogApi.info("test info")
LogApi.error("test error")
LogApi.warn("test warn")

# 重置name，app.sub沿用logging原生逻辑，logger属于app，日志写在 app_YYYYMMDD.log 文件中， %(name)s 输出为 app.sub
test_app = LogApi.LogClient(name='app.sub')
test_app.debug("test debug test_app.sub")
test_app.info("test info test_app.sub")
test_app.error("test error test_app.sub")
test_app.warn("test warn test_app.sub")

# name=test_a，那么日志文件对应为 test_a_YYYYMMDD.log
test_app = LogApi.LogClient(name='test_a')
test_app.debug("test debug test_a")
test_app.info("test info test_a")
test_app.error("test error test_a")
test_app.warn("test warn test_a")

# test_p的日志级别为 INFO，所以debug日志不会出现在 test_p_YYYYMMDD.log 中
# 设置 console=True，会同时在控制台print日志内容
test_app = LogApi.LogClient(name='test_p', console=True)
test_app.debug("test debug test_p console")
test_app.info("test info test_p console")
test_app.debug("test debug test_p console second")
test_app.error("test error test_p console")
test_app.warn("test warn test_p console")
test_app.debug("test debug test_p console third")

# 设置 send_srv=False，不会给log server send log
test_app = LogApi.LogClient(name='test_c', console=True, send_srv=False)
test_app.debug("test debug test_c console")
test_app.info("test info test_c console")
test_app.debug("test debug test_c console second")
test_app.error("test error test_c console")
test_app.warn("test warn test_c console")
test_app.debug("test debug test_c console third")

# if name not set in server
# use app to write log
test_app = LogApi.LogClient(name='test_no_set', console=True, send_srv=True)
test_app.debug("test debug test_no_set console")
test_app.info("test info test_no_set console")
test_app.debug("test debug test_no_set console second")
test_app.error("test error test_no_set console")
test_app.warn("test warn test_no_set console")
test_app.debug("test debug test_no_set console third")
