# -*- coding: utf-8 -*-

import scrapy
import re
from scrapy import cmdline
import demjson
import time
import random
from utils.db_utils import *
import datetime
from sqlalchemy import and_
from model.market.MarketDataSH import MarketData
from utils.db_utils import *
from sqlalchemy import *

"""
爬取上交所股票财报
"""

save_dir = "/Users/kittaaron/Downloads/report/"
market = "sh"


def build_old_market_data(old_market_data, dataI):
    old_market_data.exchangeRate = float(dataI['exchangeRate'])  # A股换手率
    old_market_data.istVol = float(dataI['istVol'])
    #old_market_data.marketValue = float(dataI['marketValue'])  # A股总市值(亿元)
    old_market_data.marketValue = float(dataI['marketValue1'])  # A股总市值精确值(亿元)
    #old_market_data.negotiableValue = float(dataI['negotiableValue'])  # 流通市值(亿元)
    old_market_data.negotiableValue = float(dataI['negotiableValue1'])  # 流通市值精确值(亿元)
    old_market_data.productType = int(dataI['productType'])  #
    #old_market_data.profitRate = float(dataI['profitRate'])  # 平均市盈率
    old_market_data.profitRate = float(dataI['profitRate1'])  # 平均市盈率精确值
    #old_market_data.date = str(dataI['searchDate'])
    #old_market_data.trdAmt = float(dataI['trdAmt'])  # 成交金额(亿元)
    old_market_data.trdAmt = float(dataI['trdAmt1'])  # 成交金额精确值(亿元)
    #old_market_data.trdTm = float(dataI['trdTm'])  # 成交笔数(万笔)
    old_market_data.trdTm = float(dataI['trdTm1'])  # 成交笔数精确值(万笔)
    #old_market_data.trdVol = float(dataI['trdVol'])  # 成交量(万股)
    old_market_data.trdVol = float(dataI['trdVol1'])  # 成交量精确值(万股)


class SseMarketData(scrapy.Spider):
    name = "sse_market_data"

    def start_requests(self):

        # sse_url = 'http://www.sse.com.cn/js/common/stocks/new/%s.js'
        sse_market_data_url = "http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do"

        today = datetime.date.today()
        #today = datetime.datetime.strptime('2010-09-01', '%Y-%m-%d').date()

        already_max_date = session.query(MarketData.market, func.max(MarketData.date)).filter(MarketData.market == "sh").group_by(
            MarketData.market).first()
        start_date = (datetime.datetime.strptime(already_max_date[1], '%Y-%m-%d') + datetime.timedelta(days=1)).date() if already_max_date is not None else datetime.datetime.strptime('1999-02-01', '%Y-%m-%d').date()
        #start_date = datetime.datetime.strptime('1999-02-01', '%Y-%m-%d').date()
        end_date = today
        self.log("start_date: %s, end_date: %s" % (start_date, end_date))

        while end_date >= start_date:
            param = ""
            param += "jsonCallBack=jsonpCallback" + str(random.randint(1, 99999))
            param += "&searchDate=" + end_date.strftime('%Y-%m-%d')
            param += "&prodType=gp"
            ms = str(round(time.time() * 1000 - random.randint(1, 1800)))
            param += "&_=" + ms

            url = sse_market_data_url + "?" + param
            self.log('url: %s' % url)
            end_date -= datetime.timedelta(days=1)
            time.sleep(random.random())
            payload_header = {
                'Accept': "*/*",
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Host': 'query.sse.com.cn',
                # "Origin": 'http://www.szse.cn',
                'Referer': 'http://www.sse.com.cn/market/stockdata/overview/day/',
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            }
            yield scrapy.Request(url=url, headers=payload_header,
                                 errback=self.err_callback,
                                 callback=self.parse)

    def parse(self, response):
        url = response.url
        content = response.body.decode('utf8')
        extract_contents = re.findall("jsonpCallback.*\((.*)\)", content)
        if len(extract_contents) <= 0:
            self.log("extract error. content: %s" % content)
            return

        json_content = demjson.decode(extract_contents[0])

        if 'result' not in json_content:
            self.log("no result return. content: %s" % json_content)
            return
        result = json_content['result']
        stockAData = result[0]
        stockBData = result[1]
        stockSHData = result[2]
        for dataI in result:
            searchDate = dataI['searchDate']
            productType = dataI['productType']  #

            if not searchDate or not productType or not dataI['exchangeRate'] or not dataI['marketValue'] or \
                    not dataI['profitRate'] or not dataI['trdAmt']:
                self.log("wrong data. %s" % dataI)
                continue

            old_market_data = session.query(MarketData).filter(and_(MarketData.date == searchDate,
                                                                    MarketData.productType == dataI['productType'],
                                                                    MarketData.market == market)).first()
            if old_market_data is None:
                old_market_data = MarketData(market=market, date=searchDate)
            build_old_market_data(old_market_data, dataI)
            save(old_market_data)
            self.log("保存 %s 成功" % old_market_data)

    def err_callback(self, response):
        self.log("response: %s" % response.value.response.body.decode('utf8'))


if __name__ == '__main__':
    cmdline.execute("scrapy crawl sse_market_data".split())
    # spider = SseSpider()
    # spider.start_requests()
