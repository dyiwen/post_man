# coding=utf-8
import json

from pydispatch import dispatcher
from twisted.internet.defer import succeed

from app import app


@app.route('/')
def debug(req):
    return 'DEBUG'


@app.route('/txmsg', methods=['POST'])
def repacs_msg_listener(request):
    """
    repacs 消息的回调接口
    :param request: klein的request对象
    :return: str 回复的消息内容
    """

    def process_msg(resp, msg):
        """
        异步的处理信息
        :param msg:
        :return:
        """
        # 这里的event与event.Event的属性是一一对应的关系
        task_event = msg['event']
        print msg
        dispatcher.send(task_event, msg=msg['payload'])

    try:
        msg = json.loads(request.content.read())
    except ValueError:
        request.setResponseCode(400)
        return 'repacs msg format not json.'
    rtn = succeed({'status': 1})
    rtn.addCallback(process_msg, msg)
    return rtn
