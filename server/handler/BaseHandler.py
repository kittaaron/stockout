import tornado.ioloop
from tornado.web import *
from server.handler import *
from server.handler.RespObj import RespObj, RespObjEncoder
from server.handler.PagerRespObj import PagerRespObj
import json


class BaseHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def return_json(self, obj):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        # return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True)
        return json.dumps(RespObj.return_ok(obj), cls=RespObjEncoder)

    def return_pager_resp(self, list, total_row, total_page):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return json.dumps(PagerRespObj(code=0, msg='', data=list, total_row=total_row, total_page=total_page).return_ok(), cls=RespObjEncoder)


if __name__ == "__main__":
    pass
