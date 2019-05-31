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
import dateutil


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


class ProductCategory0ListHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        category0_def_list = get_category0_def_list()

        self.write(super().return_json(category0_def_list))


class ProductCategory1ListHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, category0_id):
        if not category0_id:
            self.write(super().return_json([]))
            return
        category0_def_list = get_category1_def_list(category0_id=category0_id)

        self.write(super().return_json(category0_def_list))


class SaveProductPriceHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def post(self, *args, **kwargs):
        c0 = self.get_body_argument('c0', '')
        c1 = self.get_body_argument('c1', '')
        date = self.get_body_argument('date', '')
        price = self.get_body_argument('price', '')
        if not c0 or not c1 or not date or not price:
            logging.warning("参数错误: c0: %s, c1: %s, date: %s, price: %s", c0, c1, date, price)
            self.write(super().return_error('参数不能为空'))
            return
        date = dateutil.parser.parse(date).strftime("%Y-%m-%d")
        logging.info("c0: %s, c1: %s, date: %s, price: %s", c0, c1, date, price)
        save_product_price(c0, c1, date, price)
        self.write(super().return_json('ok'))


class BatchSaveProductPriceHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def post(self, *args, **kwargs):
        c0 = self.get_body_argument('c0', '')
        date = self.get_body_argument('date', '')
        joinedNames = self.get_body_argument('joinedNames', '')
        joinedPrices = self.get_body_argument('joinedPrices', '')

        logging.info("joinedName: %s, joinedPrice: %s", joinedNames, joinedPrices)
        names = joinedNames.split(",")
        prices = joinedPrices.split(",")
        if len(names) != len(prices):
            logging.info("参数不正确")
            self.write(super().return_error('参数不正确'))
            return

        batch_save_product_price(c0, date, names, prices)
        self.write(super().return_json('ok'))


if __name__ == "__main__":
    pass
