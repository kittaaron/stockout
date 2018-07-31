import tornado.ioloop
from tornado.web import *
from server.handler import *
from server.handler import RespObj
from server.handler.BaseHandler import BaseHandler
from stock import basic


class StockInfoHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, code):
        stock = basic.get_by_code(code)
        self.write(super().return_json(stock))


if __name__ == "__main__":
    pass
