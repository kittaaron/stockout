__author__ = 'kittaaron'
import json
import decimal


class RespObj(json.JSONEncoder):
    code = 0
    msg = ''
    data = None

    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    @staticmethod
    def return_ok(data):
        return RespObj(0, '', data)

    def reprJSON(self):
        return dict(data=self.data, code=self.code, msg=self.msg)


class RespObjEncoder(json.JSONEncoder):
    def default(self, data):
        if hasattr(data, 'reprJSON'):
            return data.reprJSON()
        elif isinstance(data, decimal.Decimal):
            return float(data)
        else:
            return json.JSONEncoder.default(self, data)