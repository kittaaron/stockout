import tornado.ioloop
from tornado.web import *
from server.handler import *
from server.handler import RespObj
from server.handler.BaseHandler import BaseHandler
from stock.dd import dd
from stock import basic
import config.logginconfig
import logging


class DDTopHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, date_str):
        default_date_str = datetime.date.today().strftime('%Y-%m-%d')
        date_str = default_date_str if date_str is None else date_str

        order_by = self.get_argument('order_by', 'net', strip=True)
        dd_sts = dd.get_ddsts_by_date(date_str, order_by)
        logging.info("数量:%s", len(dd_sts))
        self.write(super().return_json(dd_sts))


if __name__ == "__main__":
    pass
