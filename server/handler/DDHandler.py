import tornado.ioloop
from tornado.web import *
from server.handler import *
from server.handler import RespObj
from server.handler.BaseHandler import BaseHandler
from stock.dd import dd
from stock import basic
import config.logginconfig
import logging


class DDHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, code):
        default_date_str = datetime.date.today().strftime('%Y-%m-%d')
        start_date = self.get_argument('start_date', default_date_str, strip=True)
        end_date = self.get_argument('end_date', default_date_str, strip=True)
        dd_sts = dd.get_ddsts_by_code_date(code, start_date, end_date)
        logging.info("数量:%s", len(dd_sts))
        self.write(super().return_json(dd_sts))


if __name__ == "__main__":
    pass
