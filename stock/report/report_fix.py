# encoding:utf-8

from stock.report.report_handler import *
import sys

"""
    临时文件,逗号连接的入参股票代码，把已经下载好的财务报表数据，插入到数据库
"""


def handle_all():
    stocks = getSession().query(StockInfo).all()
    for stock in stocks:
        handle_one(stock)


def handle_one(stock):
    code = stock.code
    name = stock.name
    handle_zcfzb(code, name)


if __name__ == '__main__':
    handle_all()
    logging.info("处理完成")
    exit(0)
    codes = []
    if len(sys.argv) == 2:
        codes = sys.argv[1].split(",")
    logging.info("%s", codes)
    for code in codes:
        stock = getSession().query(StockInfo).filter(StockInfo.code == code).first()
        if stock is None:
            continue
        handle_one(stock)
        #handle_cwbbzy(code, name)
