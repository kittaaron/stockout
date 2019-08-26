import tornado.ioloop
from tornado.web import *
from server.handler import *
from server.handler import RespObj
from server.handler.BaseHandler import BaseHandler
from stock.dd import dd
from stock import basic
import config.logginconfig
import logging
from stock.report.fhsg import *

"""
分红送股handler
"""

class FHSGHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        date_str = self.get_argument('date_str', '')
        page = int(self.get_argument('page', 0))
        page_size = int(self.get_argument('page_size', 1000))
        if len(date_str) <= 0:
            self.write(super().return_json({}))
            return
        logging.info("date_str:%s, page: %s, page_size: %s", date_str, page, page_size)
        fhsgs = get_ordered_fhrate(date_str, page, page_size)
        logging.info("数量:%s", len(fhsgs))
        self.write(super().return_json(fhsgs))


if __name__ == "__main__":
    pass