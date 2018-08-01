__author__ = 'kittaaron'
import json
import decimal


class RespObj(json.JSONEncoder):
    code = 0
    msg = ''
    obj = None

    def __init__(self, code, msg, obj):
        self.code = code
        self.msg = msg
        self.obj = obj

    @staticmethod
    def return_ok(obj):
        return RespObj(0, '', obj)

    def reprJSON(self):
        return dict(obj=self.obj, code=self.code, msg=self.msg)


class RespObjEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)

        else:
            return json.JSONEncoder.default(self, obj)