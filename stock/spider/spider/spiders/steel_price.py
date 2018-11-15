# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
import re
import json
import string
from scrapy import cmdline, Request
import demjson
import time
import random
from urllib import request
from utils.db_utils import *
from model.StockInfo import StockInfo
from model.industry.SteelPrice import SteelPriceHist
import os
from sqlalchemy import and_

"""
爬取钢铁价格爬虫
"""


class SzseSpider(scrapy.Spider):
    name = "steel_price"

    def start_requests(self):
        """
            爬取钢铁数据价格：数据来源，我的钢铁网
        """
        mysteel_url = "https://data.mysteel.com/data/analysis/chartsData"

        payload_header = {
            'Accept': "*/*",
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'data.mysteel.com',
            "Origin": 'https://data.mysteel.com',
            'Referer': 'https://data.mysteel.com/data/analysis/detail-k5CmnVtNgE0jEiBkutr_4w==-1-6-.html',
            'X-Request-Type': 'ajax',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
        }
        payload_data= {
            "code": "k5CmnVtNgE0jEiBkutr_4w==",
            "dataType": "0"
        }
        yield scrapy.http.FormRequest(url=mysteel_url,
                      headers=payload_header,
                      formdata=payload_data,
                      #meta={'payloadFlag': True, 'payloadData': payloadData, 'headers': payloadHeader},
                      callback=self.parse,
                      errback=self.err_callback,
                      method='POST'
                      )

    def parse(self, response):
        url = response.url
        respbody = response.body.decode('utf8')
        json_resp = demjson.decode(respbody)
        if "status" not in json_resp or json_resp['status'] != "200":
            self.log("error resp. %s" % json_resp)
            return
        data = json_resp['data']
        date_arr = data['xAxis']
        series = data['series']
        data_len = len(date_arr)
        i = 0
        while i < data_len:
            dateI = date_arr[i]
            price = series[i]
            i += 1
            old_data = session.query(SteelPriceHist).filter(and_(SteelPriceHist.type == 1,
                                                                 SteelPriceHist.date == dateI,
                                                                 SteelPriceHist.price == price)).first()
            if old_data is None:
                old_data = SteelPriceHist(type=1, date=dateI, price=price)
            else:
                old_data.type = 1
                old_data.date = dateI
                old_data.price = price
            save(old_data)
            self.log("%s %s元/吨" % (dateI, price))

    def err_callback(self, response):
        self.log("response: %s" % response.value.response.body.decode('utf8'))


if __name__ == '__main__':
    cmdline.execute("scrapy crawl steel_price".split())
    #spider = SseSpider()
    #spider.start_requests()
