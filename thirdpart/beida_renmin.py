# coding=utf-8
"""
北大人民医院
"""
import json

import requests
from pydispatch import dispatcher

from adaptor import config, Event
from adaptor.repacs import repacs
from util.logger_ import get_logger
from util.threading_ import async

logger = get_logger('beida_renmin',
                    config['SERVER']['log_dir'] + '/beidarenmin.log',
                    level='DEBUG',
                    maxBytes=10 << 20)
get_logger('beida_renmin')

BDRM_NOTIFY_URL = 'http://127.0.0.1:20189/'


@async
def notify(msg, **kws):
    print msg
    logger.info('received: %s', msg)
    task_id = msg.get('taskId', '')
    status = msg.get('status', '')
    if status != 'ok':
        logger.info("task %s status is %s" % (task_id, status))
        return
    mtype = msg.get('type')
    if mtype != 'predict/ct_lung':
        logger.debug('not ct_lung task. passed.')
        return
    series = msg.get('target', {}).get('series')
    if not series:
        logger.warn('no series found for task %s. passed', task_id)
        return
    study_id = series[0]['studyId']
    series_id = series[0]['seriesId']
    predicted_result = repacs.predict(series_id,
                                      repacs.PredictType.CT_LUNG_NODE)
    logger.info(predicted_result)
    if not predicted_result:
        logger.warn('no predict result found for task %s. passed', task_id)
        return
    study_info = repacs.study(study_id)
    if not study_info:
        logger.warn('no study found for task %s. passed', task_id)
        return
    accession_num = study_info['accessionNumber']
    study_iuid = study_info['studyInstanceUID']
    boxes = predicted_result[0]['boxes']
    summary = "发现%s个结节" % len(boxes)

    server_conf = config['SERVER']
    result_viewer_url = "http://%s:%s/viewer/%s" % (server_conf['ip'],
                                                    3000, study_iuid)
    logger.info('sending bdrm notify" %s', json.dumps({
        "accession_num": accession_num,
        "result_viewer_url": result_viewer_url,
        "status": status,
        "summary": summary
    }))
    requests.post(BDRM_NOTIFY_URL,
                  json={
                      "accession_num": accession_num,
                      "result_viewer_url": result_viewer_url,
                      "status": status,
                      "summary": summary
                  })


# msg = {
#     "event": "task.create",
#     "payload": {
#         "taskId": 825,
#         "type": "predict/ct_lung",
#         "priority": 200,
#         "status": "ok",
#         "acquiredAt": "2018-08-09T11:17:56.000Z",
#         "workerId": "CT0",
#         "updatedAt": "2018-08-09T11:19:41.000Z",
#         "createdAt": "2018-08-09T11:09:21.000Z",
#         "target": {
#             "relId": 3089,
#             "relType": "default",
#             "series": [
#                 {
#                     "bodyPartExamined": None,
#                     "createdAt": "2018-08-08T10:45:56.000Z",
#                     "modality": "CT",
#                     "seriesDate": "20171228",
#                     "seriesDescription": "Recon 3:",
#                     "seriesId": 3724,
#                     "seriesInstanceUID": "1.2.840.113619.2.55.3.2831183620.19.1513932123.49.4",
#                     "seriesTime": "095508",
#                     "studyId": 2616,
#                     "updatedAt": "2018-08-09T11:09:20.000Z"
#                 }
#             ]
#         }
#     }
# }


dispatcher.connect(notify, signal=Event.TASK_UPDATE)
