# encoding:utf-8

from stock.report.report_handler import *
import sys

"""
    临时文件,逗号连接的入参股票代码，把已经下载好的财务报表数据，插入到数据库
"""

if __name__ == '__main__':
    codes = []
    if len(sys.argv) == 2:
        codes = sys.argv[1].split(",")
    logging.info("%s", codes)
    for code in codes:
        stock = getSession().query(StockInfo).filter(StockInfo.code == code).first()
        if stock is None:
            continue
        name = stock.name
        # handle_zycwzb(code, name)
        # handle_zcfzb(code, name)
        handle_cwbbzy(code, name)
