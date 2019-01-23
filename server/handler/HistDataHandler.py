import tornado.ioloop
from tornado.web import *
from server.handler import *
from server.handler import RespObj
from server.handler.BaseHandler import BaseHandler
from stock.task import hist_data
import config.logginconfig
import logging


class PriceListHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, code):
        default_date_str = datetime.date.today().strftime('%Y-%m-%d')
        default_start = (datetime.date.today() - datetime.timedelta(days=3650)).strftime('%Y-%m-%d')
        start_date = self.get_argument('start_date', default_start, strip=True)
        end_date = self.get_argument('end_date', default_date_str, strip=True)
        logging.info("start_date: %s, end_date: %s", start_date, end_date)
        price_list = hist_data.get_price_list(code, start_date, end_date)
        self.write(super().return_json(price_list))


if __name__ == "__main__":
    pass
