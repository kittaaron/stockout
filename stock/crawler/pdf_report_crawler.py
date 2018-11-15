#encoding:utf-8

from urllib import request
import os
import re
import logging
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import config.logginconfig
from dateutil.relativedelta import relativedelta
from model.StockInfo import StockInfo
import time
import datetime
import random
from utils.db_utils import *

save_dir = "/Users/kittaaron/Downloads/report/"
# 上交所pdf报告
####            http://static.sse.com.cn/disclosure/listedinfo/announcement/c/2018-04-28/600755_2017_n.pdf
sse_pdf_addr = "http://static.sse.com.cn/disclosure/listedinfo/announcement/c/{date}/{code}_{year}_{flag}.pdf"


def download_pdf(code):
    """
    下载pdf
    :param url:
    :param code:
    """
    date = datetime.date.today()
    date_str = date.strftime('%Y-%m-%d')
    delta = datetime.timedelta(days=1)
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    flag = "3" if current_month >= 10 else ("z" if 6 <= current_month <= 8 else "1")

    download_url = sse_pdf_addr.format(code=code, date=date_str, year=current_year, flag = flag)

    logging.info("download_url: %s", download_url)

    pos = download_url.rfind("/")
    save_filename = download_url[:pos]
    save_path = save_dir + code + "/" + save_filename
    request.urlretrieve(download_url, save_path)
    logging.info("save ok: %s", save_path)


if __name__ == '__main__':
    #stocks = session.query(StockInfo).all()
    stocks = session.query(StockInfo).filter(StockInfo.code == '600060').all()
    for row in stocks:
        if row is None:
            continue
        try:
            # 股票代码
            code = row.code
            download_pdf(code)
            time.sleep(1)
            #time.sleep(5)
        except Exception as e:
            logging.warning("%s %s exception when downloading. %s", row.code, row.name, e)
            time.sleep(random.randint(1, 3))