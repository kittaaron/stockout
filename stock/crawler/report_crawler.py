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


engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()

save_dir = "/Users/kittaaron/Downloads/report/"
# 主要财务指标
zycwzb_url_tmp = "http://quotes.money.163.com/service/zycwzb_%s.html?type=report"
# 财务报表摘要
cwbbzy_url_tmp = "http://quotes.money.163.com/service/cwbbzy_%s.html"
# 资产负债表
zcfzb_url_tmp = "http://quotes.money.163.com/service/zcfzb_%s.html"
# 利润表
lrb_url_tmp = "http://quotes.money.163.com/service/lrb_%s.html"
# 现金流量表
xjllb_url_tmp = "http://quotes.money.163.com/service/xjllb_%s.html"


def download_all(code):
    if not os.path.exists(save_dir + code):
        os.mkdir(save_dir + code)

    download_one(zycwzb_url_tmp, code)
    download_one(cwbbzy_url_tmp, code)
    download_one(zcfzb_url_tmp, code)
    download_one(lrb_url_tmp, code)
    download_one(xjllb_url_tmp, code)
    logging.info("download ok %s", code)



def download_one(url, code):
    """
    下载主要财务指标
    :param url:
    :param code:
    :return:
    """
    matchs = re.findall(r"http://quotes.money.163.com/service/(.+?)_.*", url)
    filename = ''
    if matchs is not None:
        filename = matchs[0] + ".csv"
    if not filename.strip():
        print(code + " filename is error, url: " + url)
        return

    save_path = save_dir + code + "/" + filename
    request.urlretrieve(url.replace("%s", code), save_path)
    logging.info("save ok: %s", save_path)


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    #stocks = session.query(StockInfo).filter(StockInfo.code =='002943').all()
    for row in stocks:
        if row is None:
            continue
        try:
            # 股票代码
            code = row.code
            download_all(code)
            time.sleep(1)
        except Exception as e:
            logging.warning("%s %s exception when downloading.", row.code, row.name)
            time.sleep(5)