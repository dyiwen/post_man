#! /usr/bin/env python
# encoding: utf-8

import sys
import suds
from suds.xsd.doctor import Import,ImportDoctor

reload(sys)
sys.setdefaultencoding('utf8')

imp = Import('http://www.w3.org/2001/XMLSchema',
            location='http://www.w3.org/2001/XMLSchema.xsd')
imp.filter.add("http://WebXml.com.cn/")
d = ImportDoctor(imp)

try:
    web_url = 'http://www.webxml.com.cn/WebServices/WeatherWebService.asmx?wsdl'
    client = suds.client.Client(web_url, doctor=d)

except:
    print 'url is error'

def get_all_methods(client): #查询本webservice所有的方法
    return [method for method in client.wsdl.services[0].ports[0].methods]

def get_method_args(client,method_name): #查询本webservice所有方法调用的参数
    method = client.wsdl.services[0].ports[0].methods[method_name]
    input_params = method.binding.input
    return input_params.param_defs(method)

interfaces = get_all_methods(client)
print 'There are interfaces what we got :\n',interfaces
print '-------------------------------------------------------------------------------------------'

def get_all_method_args(): #查询接口所有方法调用的参数
    for method_name in interfaces:
        print get_method_args(client, method_name)

cli_ser = client.service
get_all_method_args()

def ProvinceAre():#查询天气预报支持的所有省份
    #print cli_ser.getSupportProvince()
    P_are = cli_ser.getSupportProvince()
    for province in P_are:
        print province[1]
        print type(province[1])
        return province[1]
ProvinceAre()