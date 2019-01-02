#! /usr/bin/env python
# encoding: utf-8

# from xml.etree.ElementTree import Element,ElementTree,tostring

# e=Element('message')
# #e.set('name','abc')
# #e.text="123"
# #print tostring(e)
# e2=Element("header") 
# e3=Element("Open")
# e3.text=None
# e2.append(e3)
# print tostring(e2)
# e.append(e2)
# e.text=None
# print tostring(e)
# #et=ElementTree(e)
# #print tostring(et)
# #et.write("test.xml")

from xml.etree import ElementTree as ET

def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def build_xml_result():
	root = ET.Element('Message')
	header_ = ET.SubElement(root,'header')
	channel_ = ET.SubElement(header_,'channelID')
	channel_.text = "CHANNEL.SERVICE.S_DICT_BASE"
	ver_ = ET.SubElement(header_,'ver')
	ver_.text = "100"
	sourceSystemID_ = ET.SubElement(header_,'sourceSystemID')
	sourceSystemID_.text = "01_FC"
	serialNumber_ = ET.SubElement(header_,'serialNumber')
	serialNumber_.text = "APP.YYGH-2017011314233324510001"
	status_ = ET.SubElement(header_,'status')
	code_ = ET.SubElement(status_,'code')
	code_.text = None
	exptMsg_ = ET.SubElement(status_,'exptMsg')
	exptMsg_.text = None
	timestamp_ =ET.SubElement(header_,'timestamp')
	timestamp_.text = "201701131423332451"
	ext_ = ET.SubElement(header_,'ext')
	ext_.text = None
	body_ = ET.SubElement(root,'body')
	request_ = ET.SubElement(body_,'request')
	startTime_ = ET.SubElement(request_,'startTime')
	startTime_.text = "2018-04-16 00:00:00"
	endTime_ = ET.SubElement(request_,'endTime')
	endTime_.text = "2018-04-17 00:00:00"
	pageNo_ = ET.SubElement(request_,'pageNo')
	pageNo_.text = "1"
	pageSize_ = ET.SubElement(request_,'pageSize')
	pageSize_.text = "100"
	pageCount_ = ET.SubElement(request_,'pageCount')
	pageCount_.text = "1"
	total_ = ET.SubElement(request_,'total')
	total_.text = "1"
	dictTypeCode_ = ET.SubElement(request_,'dictTypeCode')
	dictTypeCode_.text = "SEX"
	incrementFlag_ =ET.SubElement(request_,'incrementFlag')
	incrementFlag_.text = "2"
	indent(root)
	print ET.tostring(root)
	tree = ET.ElementTree(root)
	xml = tree.write('request.xml')
	with open('request.xml','r') as req:
		request_data = req.read()
	print request_data
	return request_data

if __name__ == '__main__':
	build_xml_result()