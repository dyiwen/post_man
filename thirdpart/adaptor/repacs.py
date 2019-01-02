# coding=utf-8
import requests

from app import config


class Repacs(object):
    """
    repacs的wrapper
    """
    class PredictType:
        CT_LUNG_NODE = 'ct_lung'
        CT_CHEST_FRACTURE = 'ct_chest_fracture'

    def __get(self, path, *args, **kws):
        """
        GET方法包装
        """
        url = "http://%s:%s%s" % (
            config['REPACS']['ip'], config['REPACS']['port'], path)
        resp = requests.get(url, *args, **kws)
        if resp.status_code != 200:
            return None
        else:
            return resp.json()

    def study(self, _id):
        return self.__get('/studies/' + str(_id))

    def predict(self, series_id, _type):
        return self.__get('/series/%s/predict/%s' % (series_id, _type))


repacs = Repacs()
