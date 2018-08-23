# encoding:utf-8

from stock.report.report_handler import *
import sys


if __name__ == '__main__':
    codes = []
    if len(sys.argv) == 2:
        codes = sys.argv[1].split(",")
    logging.info("%s", codes)
    for code in codes:
        stock = session.query(StockInfo).filter(StockInfo.code == code).first()
        if stock is None:
            continue
        name = stock.name
        # handle_zycwzb(code, name)
        # handle_zcfzb(code, name)
        handle_cwbbzy(code, name)
