#! /usr/bin/env python
#记录日志的类
import logging

class Logger:

    def __init__(self, path,clevel = logging.DEBUG,Flevel = logging.DEBUG):
        """
        :param path: 日志路径
        :param clevel: 控制台level
        :param Flevel: 日志文件level
        :return:
        """
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
        #设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        #设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


log_instance = Logger('app.log',logging.WARNING,logging.DEBUG).logger
if __name__ =='__main__':
    logtest = Logger('test.log',logging.WARNING,logging.DEBUG).logger
    logtest.debug('一个debug信息')
    logtest.info('一个info信息')
    logtest.warning('一个warning信息')
    logtest.error('一个error信息')
    logtest.critical('一个致命critical信息')
    log_instance.info("hello")
    exit(0)