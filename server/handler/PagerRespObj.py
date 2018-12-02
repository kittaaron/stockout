__author__ = 'kittaaron'
import json
import decimal


class PagerRespObj(json.JSONEncoder):
    code = 0
    msg = ''
    total_row = 0
    total_page = 0
    data = None

    def __init__(self, code, msg, data, total_row, total_page):
        self.code = code
        self.msg = msg
        self.data = data
        self.total_row = total_row
        self.total_page = total_page

    def return_ok(self):
        return PagerRespObj(0, '', self.data, self.total_row, self.total_page)

    def reprJSON(self):
        return dict(data=self.data, code=self.code, msg=self.msg, total_row=self.total_row, total_page=self.total_page)


class RespObjEncoder(json.JSONEncoder):
    def default(self, data):
        if hasattr(data, 'reprJSON'):
            return data.reprJSON()
        elif isinstance(data, decimal.Decimal):
            return float(data)
        else:
            return json.JSONEncoder.default(self, data)