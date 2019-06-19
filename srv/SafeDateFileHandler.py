# encoding: utf-8
"""
@author: jinlin.xiao
@file: SafeDateFileHandler.py
@time: 2019/4/19 11:21 AM
@desc:
按天切换文件的log handler
"""
from logging import FileHandler
# from logging.handlers import TimedRotatingFileHandler
import time
import os
try:
    import codecs
except ImportError:
    codecs = None


class SafeDateFileHandler(FileHandler):

    def __init__(self, filename, mode='a', encoding=None, delay=0):
        """
        Use the specified filename for streamed logging
        """
        if codecs is None:
            encoding = None
        self.filename = filename
        self.log_dir = 'log'    # make dir 'log' in current path
        self.__mk_log_dir()
        # set delay=1 for filename not add date
        FileHandler.__init__(self, filename, mode, encoding, delay=1)
        # FileHandler.__init__ has set delay=1,here must reset delay
        self.delay = delay
        self.mode = mode
        self.encoding = encoding
        self.suffix = "%Y%m%d"     # support %Y%m%d%H%M%S
        self.suffix_time = ""

    def __mk_log_dir(self):
        # path with dir
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)

    def __get_custom_base_name(self):
        """
        get custom baseFileName
        :return: baseFileName
        """
        # if self.suffix_time is None, return %s_.log
        return os.path.join(self.log_dir, "%s_%s.log" % (self.filename, self.suffix_time))

    def __set_base_name(self):
        """
        reset self.suffix_time, and set self.baseFileName
        """
        # add new suffix
        current_time_tuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, current_time_tuple)
        self.baseFilename = self.__get_custom_base_name()

    def emit(self, record):
        """
        Emit a record.
        Always check time
        :param record:
        """
        try:
            if self.check_base_filename():
                self.build_base_filename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_base_filename(self):
        """
        Determine if builder should occur.
        record is not used, as we are just comparing times, 
        but it is needed so the method signatures are the same
        """
        time_tuple = time.localtime()
        # date changed or file not exist
        check_file_name = self.__get_custom_base_name()
        if self.suffix_time != time.strftime(self.suffix, time_tuple) or not os.path.exists(check_file_name):
            return True
        else:
            return False

    def build_base_filename(self):
        """
        do builder; in this case, 
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        -- 20190103
        -- not remove, just reset self.baseFileName
        -- close add flush and lock control like self.close()
        """
        # 1.close
        self.acquire()
        try:
            if self.stream:
                try:
                    self.flush()
                finally:
                    stream = self.stream
                    self.stream = None
                    if hasattr(stream, "close"):
                        stream.close()
        finally:
            self.release()
        # 2.reset self.baseFilename
        self.__set_base_name()
        # 3. set self.stream , here support no delay
        if not self.delay:
            self.stream = self._open()


# global variable
sys_logger, app_logger = None, None
