import tornado.ioloop
from tornado.web import *
from server.handler import *
from server.handler import RespObj
from server.handler.BaseHandler import BaseHandler
from stock import basic
from utils.pinyin_util import *


class SearchStockHandler(BaseHandler):
    def get(self, param):
        ## 参数可能是数字或者字符串
        if param.isdigit():
            ## 如果是数字
            stocks = basic.get_by_code_like(param)
        elif param.encode('UTF-8').isalpha():
            ## 如果是字母
            stocks = basic.get_by_abbr_like(param.lower())
        else:
            ## 中文查询
            names = [param]
            stocks = basic.get_by_names(names)
        retstocks = []
        for stock in stocks:
            retI = {}
            retI['code'] = stock.code
            retI['name'] = stock.name
            retstocks.append(retI)
        self.write(super().return_json(retstocks))


if __name__ == "__main__":
    print('SZHZ'.isdigit())
    print('SZHZ'.isalpha())
    print('000001'.isdigit())
    print('002000'.isalpha())
    print('ST保千'['ST保千'.index('T')+1:])
    print(lazy_pinyin('奥飞数据'))
    print(get_acronym('中弘股份'))
