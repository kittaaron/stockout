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
from model.report.AnnouncePub import AnnouncePub
from sqlalchemy import and_

save_dir = "/Users/kittaaron/Downloads/report/"


class SseSpider(scrapy.Spider):
    name = "sse"

    def start_requests(self):

        #sse_url = 'http://www.sse.com.cn/js/common/stocks/new/%s.js'
        sse_url = "http://query.sse.com.cn/security/stock/queryCompanyStatementNew.do"

        stocks = session.query(StockInfo).all()
        #stocks = session.query(StockInfo).filter(StockInfo.code=="601933").all()
        end_date = datetime.date.today().strftime('%Y-%m-%d')
        start_date = str(datetime.datetime.now().year - 1) + "-01-01"

        for row in stocks:
            if row is None:
                continue

            stockcode = row.code
            if not stockcode.startswith("60"):
                self.log("not 60 code %s" % stockcode)
                continue

            param = ""
            param += "jsonCallBack=jsonpCallback" + str(random.randint(1, 99999))
            param += "&isPagination=true"
            param += "&productId=" + stockcode
            param += "&isNew=1"
            param += "&reportType2=DQBG"
            param += "&reportType=ALL"
            param += "&beginDate=" + start_date
            param += "&endDate=" + end_date
            param += "&pageHelp.pageSize=25"
            param += "&pageHelp.pageCount=50"
            param += "&pageHelp.pageNo=1"
            param += "&pageHelp.beginPage=1"
            param += "&pageHelp.cacheSize=1"
            param += "&pageHelp.endPage=5"
            ms = str(round(time.time() * 1000 - random.randint(1, 1800)))
            param += "&_=" + ms

            url = sse_url + "?" + param

            self.log('url: %s' % url)
            time.sleep(random.randint(1, 2))
            payload_header = {
                'Accept': "application/json, text/javascript, */*; q=0.01",
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
                'Host': 'www.sse.com.cn',
                #"Origin": 'http://www.szse.cn',
                'Referer': 'http://www.sse.com.cn/assortment/stock/list/info/announcement/index.shtml?productId=' + stockcode,
                'X-Request-Type': 'ajax',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
            }
            yield scrapy.Request(url=url, headers=payload_header,
                          errback=self.err_callback,
                                 callback=self.parse)

    def parse(self, response):
        url = response.url
        content = response.body.decode('utf8')
        #print(content)
        extract_contents = re.findall("jsonpCallback.*\((.*)\)", content)
        if len(extract_contents) <= 0:
            self.log("extract error. content: %s" % content)
            return

        json_content = demjson.decode(extract_contents[0])

        if 'pageHelp' not in json_content or 'data' not in json_content['pageHelp']:
            self.log("no data return: %s" % json_content)
            return

        for dataI in json_content['pageHelp']['data']:
            bulletin_file_url = dataI['URL']
            bulletin_title = dataI['title']
            code = dataI['security_Code']
            bulletin_year = dataI['bulletin_Year']
            pub_date = dataI['SSEDate']
            bulletin_type = dataI['bulletin_Type']

            file_suffix = bulletin_file_url[bulletin_file_url.rfind("."):]

            if '度报告' in bulletin_title:
                announce_record = session.query(AnnouncePub).filter(and_(AnnouncePub.code == code,
                                                                AnnouncePub.bulletin_year == bulletin_year,
                                                                AnnouncePub.title == bulletin_title)).first()
                if announce_record is None:
                    announce_record = AnnouncePub(code=code)
                announce_record.title = bulletin_title
                announce_record.pub_date = pub_date
                announce_record.file_url = "http://static.sse.com.cn" + bulletin_file_url
                announce_record.bulletin_type = bulletin_type
                announce_record.bulletin_year = bulletin_year
                save(announce_record)
                self.log('文件名: %s bulletin_file_url %s' % (bulletin_title, bulletin_file_url))

                save_path = save_dir + code + "/" + bulletin_title + file_suffix

                if os.path.exists(save_path):
                    self.log("已下载: %s" % save_path)
                    continue
                self.log("开始下载: %s" % save_path)
                #time.sleep(random.randint(1, 10))

                request.urlretrieve("http://static.sse.com.cn" + bulletin_file_url, save_path)
            else:
                self.log('(不下载)其他文档 -- title: %s bulletin_file_url %s' % (bulletin_title, bulletin_file_url))
            '''
            if bulletin_file_url.find("_z.pdf") >= 0 or \
                    bulletin_file_url.find("_n.pdf") >= 0 or \
                    bulletin_file_url.find("_1.pdf") >= 0 or \
                    bulletin_file_url.find("_3.pdf") >= 0:
                self.log('title: %s bulletin_file_url %s' % (bulletin_title, bulletin_file_url))
            else:
                self.log('其他文档 -- title: %s bulletin_file_url %s' % (bulletin_title, bulletin_file_url))
            '''

    def err_callback(self, response):

        self.log("response: %s" % response.value.response.body.decode('utf8'))

if __name__ == '__main__':
    cmdline.execute("scrapy crawl sse".split())
    #spider = SseSpider()
    #spider.start_requests()
