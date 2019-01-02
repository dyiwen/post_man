# coding=utf-8
"""
毓璜顶/美迪康对接接口
"""
from pydispatch import dispatcher
from zeep import Client

from adaptor import config, Event, repacs
from util.logger_ import get_logger

logger = get_logger('yuhuangding',
                    config['SERVER']['log_dir'] + '/yuhuangding.log',
                    maxBytes=10 << 20)


def notify4create(msg, **kws):
    """
    task.create 事件回调
    :param msg: dict
    :return:
    """
    return notify(msg, 2)


dispatcher.connect(notify4create, signal=Event.TASK_CREATE)


def notify4update(msg, **kws):
    """
    task.update 事件回调
    :param msg: dict
    :return:
    """
    return notify(msg, 3)


dispatcher.connect(notify4update, signal=Event.TASK_UPDATE)


def notify(msg, status_code):
    # 解析参数 study_id
    logger.debug('received: %s', msg)
    payload = msg.get('payload', {})
    task_id = payload.get('taskId', '')
    status = payload.get('status', '')
    if status != 'ok':
        logger.info("task %s status is %s", task_id, status)
        return
    mtype = payload.get('type')
    if mtype != 'predict/ct_lung':
        logger.debug('not ct_lung task. passed.')
        return
    series = payload.get('target', {}).get('series')
    if not series:
        logger.error('no series found for task %s. passed', task_id)
        return
    study_id = series[0]['studyId']

    # 翻译study_id到accession_num
    study_info = repacs.study(study_id)
    if not study_info:
        logger.error('study info not found for %s', study_id)
    acc_no = study_info['accessionNumber']
    # 调用对方服务
    client = Client('resource/Medicon.wsdl')
    client.SetExamStatus(u'推想', acc_no, status_code)
