# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
import re
import json
import string
from scrapy import cmdline
import demjson
import time
import random
from urllib import request
from utils.db_utils import *
from model.StockInfo import StockInfo
import os
import datetime
from model.HKStock import HKStock
from sqlalchemy import and_

"""
爬取港交所股票数据
"""

save_dir = "/Users/kittaaron/Downloads/report/"

def build_url(hkse_url, page, pagesize):
    req_num = str(random.randint(1, 9999))
    param = ""
    param += "callback=callback_" + str(random.randint(1, 9999999999))
    param += "&host=/hk/service/hkrank.php"
    param += "&page=" + str(page)
    param += "&query=CATEGORY:MAIN;TYPE:1;EXCHANGE_RATE:_exists_true"
    param += "&fields=no,SYMBOL,NAME,PRICE,PERCENT,UPDOWN,OPEN,YESTCLOSE,HIGH,LOW,VOLUME,TURNOVER,EXCHANGE_RATE,ZF,PE,MARKET_CAPITAL,EPS,FINANCEDATA.NET_PROFIT,FINANCEDATA.TOTALTURNOVER_"
    param += "&PERCENT=PERCENT"
    param += "&order=desc"
    param += "&count=" + str(pagesize)
    param += "&type=query"
    param += "&req=" + str(req_num)

    url = hkse_url + param
    return url


def build_stockinfo(oldstock, dataI):
    oldstock.price = dataI['PRICE'] if 'PRICE' in dataI else None
    oldstock.eps = dataI['EPS'] if 'EPS' in dataI else None
    oldstock.pe = dataI['PE'] if 'PE' in dataI else None
    oldstock.fixedpe = round(oldstock.price / oldstock.eps, 2) if oldstock.eps != 0 else oldstock.pe
    oldstock.percent = dataI['PERCENT'] if 'PERCENT' in dataI else None
    oldstock.turnover = dataI['TURNOVER'] if 'TURNOVER' in dataI else None
    oldstock.high = dataI['HIGH'] if 'HIGH' in dataI else None
    oldstock.open = dataI['OPEN'] if 'OPEN' in dataI else None
    oldstock.volume = dataI['VOLUME'] if 'VOLUME' in dataI else None
    oldstock.low = dataI['LOW'] if 'LOW' in dataI else None
    oldstock.mkt_cap = dataI['MARKET_CAPITAL'] if 'MARKET_CAPITAL' in dataI else None
    oldstock.exchange_rate = dataI['EXCHANGE_RATE'] if 'EXCHANGE_RATE' in dataI else None
    oldstock.total_turnover = dataI['FINANCEDATA']['TOTALTURNOVER_'] if 'FINANCEDATA' in dataI and 'TOTALTURNOVER_' in dataI['FINANCEDATA'] else None
    oldstock.net_profit = dataI['FINANCEDATA']['NET_PROFIT'] if 'FINANCEDATA' in dataI and 'NET_PROFIT' in dataI['FINANCEDATA'] else None
    oldstock.updown = dataI['UPDOWN'] if 'UPDOWN' in dataI else None
    oldstock.yestclose = dataI['YESTCLOSE'] if 'YESTCLOSE' in dataI else None
    oldstock.zf = dataI['ZF'] if 'ZF' in dataI else None


total_page = 0


class HKSESpider(scrapy.Spider):
    name = "hkse"

    def start_requests(self):
        page = 0
        pagesize = 24
        while True:
            hkse_url = "http://quotes.money.163.com/hk/service/hkrank.php?"
            req_url = build_url(hkse_url, page, pagesize)

            self.log('req_url: %s' % req_url)

            payload_header = {
                'Accept': "*/*",
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/json',
                'Host': 'quotes.money.163.com',
                #"Origin": 'http://www.szse.cn',
                'Referer': 'http://quotes.money.163.com/old/',
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            }
            yield scrapy.Request(url=req_url, headers=payload_header,
                          errback=self.err_callback,
                                 callback=self.parse)
            time.sleep(random.randint(1, 5))
            page += 1
            self.log("page: %s total_page: %s" % (page, total_page))
            if 0 < total_page <= page:
                break
        self.log("程序结束.")


    def parse(self, response):
        url = response.url
        content = response.body.decode('utf8')
        extract_contents = re.findall("callback_.*\((.*)\)", content)
        if len(extract_contents) <= 0:
            self.log("extract error. content: %s" % content)
            return

        json_content = demjson.decode(extract_contents[0])
        data_date = json_content['time'][:10]
        list = json_content['list']

        global total_page
        if total_page == 0:
            total_page = json_content['pagecount']

        self.log("当前页数: %s 总条数: %s, 总页数: %s" % (json_content['page'], json_content['total'], json_content['pagecount']))
        for dataI in list:
            code = dataI['SYMBOL']
            name = dataI['NAME']
            self.log("获取到数据 %s, %s 市值: %s, 净利润: %s, eps: %s pe: %s" % (code, name, dataI['MARKET_CAPITAL'], dataI['FINANCEDATA']['NET_PROFIT'], dataI['EPS'], dataI['PE']))

            oldstock = session.query(HKStock).filter(and_(HKStock.code == code,
                                                                 HKStock.date == data_date)).first()
            if oldstock is None:
                oldstock = HKStock(code=code, name=name, date=data_date)
            build_stockinfo(oldstock, dataI)
            save(oldstock)
            self.log("保存 %s 成功" % oldstock)

    def err_callback(self, response):
        self.log("response: %s" % response.value.response.body.decode('utf8'))


if __name__ == '__main__':
    cmdline.execute("scrapy crawl hkse".split())
