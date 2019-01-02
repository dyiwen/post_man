# coding=utf-8
import codecs
import logging
from logging.handlers import RotatingFileHandler


def get_logger(name, path=None, level=logging.INFO, maxBytes=0, backupCount=0,
               buffering=1):
    """
    获取logger
    :param name: str 名称
    :param path: str 路径
    :param level: logging.LEVEL 日志级别
    :param maxBytes: int 日志最大大小
    :param backupCount: int 日志最大备份数量
    :return: logging.Logger 日志对象
    """
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    if path:
        handler = BufferedRotatingFileHandler(path, maxBytes=maxBytes,
                                              backupCount=backupCount,
                                              buffering=buffering)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    if logger.level == logging.NOTSET or logger.level > level:
        logger.setLevel(level)
    return logger


class BufferedRotatingFileHandler(RotatingFileHandler):
    """
    带有缓冲的轮换文件日志写入Handler
    只有第一次写入的时候直接flush, 以表明日志生效
    """

    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0,
                 encoding=None, delay=0, buffering=1):
        self.buffering = buffering
        self._first_flush = False
        super(BufferedRotatingFileHandler, self).__init__(filename, mode,
                                                          maxBytes,
                                                          backupCount,
                                                          encoding, delay)

    def _open(self):
        """
        Open the current base file with the (original) mode and encoding.
        Return the resulting stream.
        """
        if self.encoding is None:
            stream = open(self.baseFilename, self.mode, self.buffering)
        else:
            stream = codecs.open(self.baseFilename, self.mode, self.encoding,
                                 self.buffering)
        return stream

    def emit(self, record):
        """
        Emit a record.

        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.
        """
        if self.stream is None:
            self.stream = self._open()
        try:
            if self.shouldRollover(record):
                self.doRollover()
            msg = self.format(record)
            stream = self.stream
            fs = "%s\n"
            try:
                if (isinstance(msg, unicode) and
                        getattr(stream, 'encoding', None)):
                    ufs = u'%s\n'
                    try:
                        stream.write(ufs % msg)
                    except UnicodeEncodeError:
                        # Printing to terminals sometimes fails. For example,
                        # with an encoding of 'cp1251', the above write will
                        # work if written to a stream opened or wrapped by
                        # the codecs module, but fail when writing to a
                        # terminal even when the codepage is set to cp1251.
                        # An extra encoding step seems to be needed.
                        stream.write((ufs % msg).encode(stream.encoding))
                else:
                    stream.write(fs % msg)
            except UnicodeError:
                stream.write(fs % msg.encode("UTF-8"))
            if not self._first_flush:
                self.flush()
                self._first_flush = True
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
