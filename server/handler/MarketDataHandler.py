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


class SHMarketDataHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        start_date = "2006-01-01"
        end_date = datetime.date.today().strftime('%Y-%m-%d')
        market_datas = get_sh_market_data("sh", 12, start_date, end_date)

        self.write(super().return_json(market_datas))


class SZMarketDataHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        start_date = "2005-01-03"
        end_date = datetime.date.today().strftime('%Y-%m-%d')
        zbtype = zbmcs.index("股票平均市盈率") + 1
        market_datas = get_sz_market_data(zbtype, start_date, end_date)

        self.write(super().return_json(market_datas))


class SteelPriceHistHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        start_date = "2005-01-03"
        end_date = datetime.date.today().strftime('%Y-%m-%d')
        type = 1
        market_datas = get_steel_price_hist(type, start_date, end_date)

        self.write(super().return_json(market_datas))


if __name__ == "__main__":
    pass
