import tornado.ioloop
from tornado.web import *
from server.handler import *
from server.handler import RespObj
from server.handler.BaseHandler import BaseHandler
from stock.dd import dd
from stock import basic
import config.logginconfig
import logging
from stock.marketdata.marketdata import *
from stock.industry.product_price_hist_handler import *


class ProductPriceHistHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        category0 = "维生素"
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=730)
        end_date_str = today.strftime('%Y-%m-%d')
        start_date_str = start_date.strftime('%Y-%m-%d')
        grouped_datas = get_grouped_category1(category0, start_date_str, end_date_str)

        self.write(super().return_json(grouped_datas))


if __name__ == "__main__":
    pass
