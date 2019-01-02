# coding=utf-8
"""
易联众的对接调用
"""
from pydispatch import dispatcher

from adaptor import config, Event
from util.logger_ import get_logger

logger = get_logger('yilanzhong',
                    config['SERVER']['log_dir'] + '/yilanzhong.log',
                    maxBytes=10 << 20)


def notify(msg):
    print msg


dispatcher.connect(notify, signal=Event.TASK_CREATE)
