__author__ = 'kittaaron'
import json


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


class RespObjEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, RespObj):
            return float(o)
        super(RespObjEncoder, self).default(o)