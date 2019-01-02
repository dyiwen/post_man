# coding=utf-8
# coding=utf-8
"""
易联众的对接调用
"""
from pydispatch import dispatcher

from adaptor import config, Event
from util.logger_ import get_logger
from traceback import format_exc
import os,json
from xml.etree import ElementTree as ET

logger = get_logger('yilanzhong',
                    config['SERVER']['log_dir'] + '/yilanzhong.log',
                    maxBytes=10 << 20)
#------------------------------------------------------------------------
def out(s):
    print s
    logger.info(s)

def debug(s):
    print s
    logger.debug(s)

def warn(s):
    print s
    logger.warning(s)
    logger.warning(format_exc())

def error(s):
    print s
    logger.error(s)
    logger.error(format_exc())
#-------------------------------------------------------------------------
def notify(msg):
    #print msg
    payload = msg.get('payload')
    taskId = payload.get('taskId')
    pre_type = payload.get('type')
    status = payload.get('status')
    channel = payload.get('workerId')
    if status != 'ok':
        out('The predict {} is {}!'.format(taskId,status))
        return
    if pre_type != 'predict/ct_lung':
        logger.debug('not ct_lung task. passed.')
        return
    series = payload.get('target').get('series')
    study_id = series[0]['studyId']
    study_info = repacs.study(study_id)
    accession_num = study_info['accessionNumber']
    study_iuid = study_info['studyInstanceUID']
    if not series:
        error('no series found from task {}. passed : {}'.format(task_id,accession_num))
        return
    if not study_info:
        error('study info not found for %s', study_id)
    #-------------------------------------------------------------------------------------
    seriesInstanceUID = msg['payload']['target']['series'][0]['seriesInstanceUID']
    if status == 'ok':
        xml_status = 1
        desc = '成功'
    else:
        xml_status = 0
        desc = '异常'
    sysname = '推想科技'
    #-------------------------------------------------------------------------------------
    def build_xml_result():
        root = ET.Element('DiagResult')
        Sysname = ET.SubElement(root,'SystemName')
        Sysname.text = sysname 
        StudyUid = ET.SubElement(root,'StudyInstanceUID')
        StudyUid.text = seriesInstanceUID
        pred_status = ET.SubElement(root,'the-status-of-predict')
        Status = ET.SubElement(root,'Status')
        Status.text = str(xml_status)
        result_web = ET.SubElement(root,'the-url-of-result')
        XML_URL = ET.SubElement(root,'URL')
        XML_URL.text = 'localhost:port'
        tree = ET.ElementTree(root)
        xml = tree.write('request.xml')
        with open('request.xml','r') as req:
            request_data = req.read()
        return request_data
    def build_xml_response():
        root = ET.Element('response')
        sub_code = ET.SubElement(root,'code')
        sub_code.text = str(xml_status)
        sub_desc = ET.SubElement(root,'desc')
        sub_desc.text = desc
        tree = ET.ElementTree(root)
        xml = tree.write('response.xml')
        with open('response.xml','r') as req:
            response_data = req.read()
        return response_data
    target_URL = 'http://127.0.0.1:20189/'
    headers = {'Content-type':'text/xml'}
    requests.post(target_URL, data = build_xml_result(), headers = headers)
    os.remove('request.xml')
    out(str(build_xml_result()))


dispatcher.connect(notify, signal=Event.TASK_CREATE)
