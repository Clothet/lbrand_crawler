# -*- coding: utf-8 -*-
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
import datetime as dt


class MyFormatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s


class LoggerHelper:

    def __init__(self):
        pass

    @classmethod
    def init_logger(self, logger_name, to_console=True, debug_thread=False, log_fullname='', size=0):
        if logger_name not in Logger.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            if debug_thread:
                format_str = '[%(asctime)s]: TID-%(thread)d %(name)s %(levelname)s L%(lineno)s %(message)s'
            else:
                # if to_console :
                console_format_str = '[%(asctime)s]: %(name)s %(levelname)s L%(lineno)s %(message)s'
                # else:
                msg_format_str = '%(message)s'

            if to_console:
                formatter = logging.Formatter(
                    console_format_str, datefmt='%Y-%m-%d %H:%M:%S')
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                console_handler.setLevel(logging.DEBUG)
                logger.addHandler(console_handler)

            if log_fullname:
                formatter = logging.Formatter(
                    msg_format_str, datefmt='%Y-%m-%d %H:%M:%S')
                handler = RotatingFileHandler('{0}'.format(
                    log_fullname), mode='a', maxBytes=size, backupCount=30)
                handler.setFormatter(formatter)
                handler.setLevel(logging.DEBUG)
                logger.addHandler(handler)
            """
            # handler error
            handler = RotatingFileHandler('/tmp/ktv_error.log', mode='a', maxBytes=1024000, backupCount=5)
            datefmt = "%Y-%m-%d %H:%M:%S"
            format_str = "[%(asctime)s]: %(name)s %(levelname)s L%(lineno)s %(message)s"
            formatter = logging.Formatter(format_str, datefmt)
            handler.setFormatter(formatter)
            handler.setLevel(logging.ERROR)
            logger.addHandler(handler)
            """
        logger = logging.getLogger(logger_name)
        return logger

if __name__ == '__main__':
    logger = LoggerHelper().init_logger('helper')
    logger.error("test-error")
    logger.info("test-info")
    logger.warn("test-warn")
