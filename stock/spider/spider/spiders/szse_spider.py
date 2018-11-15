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
import os

"""
爬取深交所股票财报
"""

save_dir = "/Users/kittaaron/Downloads/report/"


class SzseSpider(scrapy.Spider):
    name = "szse"

    def start_requests(self):
        #stocks = session.query(StockInfo).all()
        stocks = session.query(StockInfo).filter(StockInfo.code=="000333").all()

        for row in stocks:
            if row is None:
                continue
            stockcode = row.code
            if not stockcode.startswith("00") and not stockcode.startswith("30"):
                self.log("not sz szse. code: %s" % stockcode)
                continue

            '''
            这是爬取没有分类的文档信息
            sse_url = 'http://www.szse.cn/api/search/secInfoList?random=' + str(random.random())

            yield scrapy.FormRequest(
                url=szse_url,
                formdata={
                    'channelCode': ["listedNotice_disc"],  # 这里不能给bool类型的True，requests模块中可以
                    'currentPage': '1',  # 这里不能给int类型的1，requests模块中可以
                    'pageSize': '20'
                },
                callback=self.parse
            )
            '''

            """
                爬取公告
            """
            szse_url = "http://www.szse.cn/api/disc/announcement/annList?random=" + str(random.random())

            payload_header= {
                'Accept': "application/json, text/javascript, */*; q=0.01",
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
                'Host': 'www.szse.cn',
                "Origin": 'http://www.szse.cn',
                'Referer': 'http://www.szse.cn/disclosure/listed/notice/index.html?stock=' + stockcode,
                'X-Request-Type': 'ajax',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
            }
            payload_data= {
                "channelCode": ["fixed_disc"],
                "pageNum": 1,
                "pageSize": 10,
                "stock": [stockcode]
            }
            time.sleep(random.randint(1, 10))
            yield Request(url=szse_url,
                          headers=payload_header,
                          body=json.dumps(payload_data),
                          #meta={'payloadFlag': True, 'payloadData': payloadData, 'headers': payloadHeader},
                          callback=self.parse,
                          errback=self.err_callback,
                          method='POST'
                          )

    def parse(self, response):
        url = response.url
        jsonreqbody = demjson.decode(response.request.body.decode('utf8'))
        respbody = response.body.decode('utf8')
        code = '0'
        if 'stock' in jsonreqbody and len(jsonreqbody['stock']) > 0:
            code = jsonreqbody['stock'][0]
        if code == '0':
            self.log("wrong code, reqbody: %s" % jsonreqbody)
            return

        self.log("code: %s, url: %s, body: %s" % (code, url, respbody))
        json_body = demjson.decode(respbody)
        if json_body is not None and 'data' in json_body:
            reports = json_body['data']
            for reportI in reports:
                title = reportI['title']
                attachPath = reportI['attachPath']
                attachFormat = reportI['attachFormat']
                file_suffix = "." + attachFormat
                self.log('文件名: %s attachPath %s' % (title, attachPath))
                if '度报告' not in title:
                    continue

                docurl = "http://disc.static.szse.cn/download" + attachPath
                save_path = save_dir + code + "/" + title + file_suffix
                if os.path.exists(save_path):
                    self.log("已下载: %s" % save_path)
                    continue
                self.log("开始下载: %s" % save_path)

                request.urlretrieve(docurl, save_path)
        else:
            self.log("no report found")

    def err_callback(self, response):
        self.log("response: %s" % response.value.response.body.decode('utf8'))


if __name__ == '__main__':
    cmdline.execute("scrapy crawl szse".split())
    #spider = SseSpider()
    #spider.start_requests()
