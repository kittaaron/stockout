# -*- coding: utf-8 -*-

import scrapy
from scrapy import cmdline
import demjson
import time
import random
from utils.db_utils import *
import datetime
from sqlalchemy import and_
from model.market.MarketDataSZ import MarketDataSZ
from model.market.MarketDataSZ import zbmcs
import locale
from sqlalchemy import *

"""
爬取上交所股票财报
"""

save_dir = "/Users/kittaaron/Downloads/report/"
market = "sz"
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def build_old_market_data(old_market_data, dataI, zbtype):
    old_market_data.brsz = locale.atof(dataI['brsz']) if dataI['brsz'] else None  #比上日增减
    old_market_data.bsrzj = locale.atof(dataI['bsrzj']) if dataI['bsrzj'] else None  #比上日增减
    old_market_data.fd = locale.atof(dataI['fd']) if dataI['fd'] else None #幅度
    old_market_data.bnzg = locale.atof(dataI['bnzg']) if dataI['bnzg'] else None  #本年最高
    old_market_data.zgzrq = dataI['zgzrq'] if dataI['zgzrq'] else None #最高值日期


def getzbtype(zbmc):
    for i, zbmcI in enumerate(zbmcs):
        if zbmcI in zbmc:
            return i+1
    return 0
    pass


class SseMarketData(scrapy.Spider):
    name = "szse_market_data"

    def start_requests(self):
        sse_market_data_url = "http://www.szse.cn/api/report/ShowReport/data"

        today = datetime.date.today()
        #today = datetime.datetime.strptime('2010-09-01', '%Y-%m-%d').date()
        #start_date = datetime.datetime.strptime('2005-01-03', '%Y-%m-%d').date()

        already_max_date = session.query(func.max(MarketDataSZ.date)).first()
        start_date = (datetime.datetime.strptime(already_max_date[0], '%Y-%m-%d') + datetime.timedelta(days=1)).date() if already_max_date is not None else datetime.datetime.strptime('2005-01-03', '%Y-%m-%d').date()
        end_date = today

        self.log("start_date: %s, end_date: %s" % (start_date, end_date))

        while end_date >= start_date:
            param = ""
            param += "SHOWTYPE=JSON"
            param += "&CATALOGID=1803"
            param += "&txtQueryDate=" + end_date.strftime('%Y-%m-%d')
            # tab1、tab2、tab3、tab4分别为深圳市场，深圳主板，中小板企业，创业板 4种类型的值
            param += "&TABKEY=tab1"

            param += "&random=" + str(random.random())

            url = sse_market_data_url + "?" + param
            self.log('url: %s' % url)
            end_date -= datetime.timedelta(days=1)
            time.sleep(random.random())
            payload_header = {
                'Accept': "application/json, text/javascript, */*; q=0.01",
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Host': 'www.szse.cn',
                # "Origin": 'http://www.szse.cn',
                'Referer': 'http://www.szse.cn/market/stock/indicator/index.html',
                'X-Request-Type': 'ajax',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            }
            yield scrapy.Request(url=url, headers=payload_header,
                                 errback=self.err_callback,
                                 callback=self.parse,
                                 meta = {"date": end_date.strftime('%Y-%m-%d')}
                                 )

    def parse(self, response):
        url = response.url
        meta = response.meta
        date = meta['date']
        respbody = response.body.decode('utf8')
        json_body = demjson.decode(respbody)
        if json_body is None or len(json_body) <= 0:
            self.log("crawler return error. %s" % json_body)
            return
        wrapperdata = json_body[0]
        if wrapperdata['error'] is not None:
            self.log("crawler return error. %s" % json_body)
            return
        data = wrapperdata['data']
        if not data:
            self.log("no data %s" % date)
            return

        for dataI in data:
            self.log("dataI: %s" % dataI)
            zbmc = dataI['zbmc']  #指标名称
            zbtype = getzbtype(zbmc)
            brsz = dataI['brsz']  #本日数值

            old_market_data = session.query(MarketDataSZ).filter(and_(MarketDataSZ.date == date,
                                                                      MarketDataSZ.zbtype == zbtype)).first()
            if old_market_data is None:
                old_market_data = MarketDataSZ(date=date, zbtype=zbtype)
            build_old_market_data(old_market_data, dataI, zbtype)
            save(old_market_data)
            self.log("保存 %s 成功" % old_market_data)

    def err_callback(self, response):
        self.log("response: %s" % response.value.response.body.decode('utf8'))


if __name__ == '__main__':
    cmdline.execute("scrapy crawl szse_market_data".split())
    # spider = SseSpider()
    # spider.start_requests()
