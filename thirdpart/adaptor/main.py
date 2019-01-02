# coding=utf-8
from time import sleep

import requests
from twisted.internet import reactor

from app import app, config
from util.threading_ import asyncd

msg_listener_key = 'msg_listener'


@asyncd
def register_msg_listener():
    """
    向repacs的webhook注册服务
    :return:
    """
    sleep(3)
    repacs_config = config['REPACS']
    server_config = config['SERVER']
    requests.post('http://%s:%s/%s' % (
        repacs_config['ip'], repacs_config['port'],
        repacs_config['webhook_url']),
                  json={
                      "key": msg_listener_key,
                      "events": ['task.update'],
                      "callback": "http://%s:%s%s" % (
                          server_config['ip'], server_config['port'], '/txmsg')
                  })


def unregister_msg_listener():
    """
    解除repacs中的webhook的注册
    """
    repacs_config = config['REPACS']
    requests.delete('http://%s:%s/%s/%s' % (
        repacs_config['ip'], repacs_config['port'],
        repacs_config['webhook_url'], msg_listener_key))


# 启用 Viewer
__import__('adaptor.views')
# 启用自定义服务
__import__('thirdpart.' + config['THIRDPART']['name'])

# 注册服务
register_msg_listener()

# 当应用退出解除注册
reactor.addSystemEventTrigger('before', 'shutdown', unregister_msg_listener)

# twisted 资源
resource = app.resource
