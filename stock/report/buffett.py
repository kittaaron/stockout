from typing import Any, Union

import tushare as ts
import logging
import config.logginconfig
from model.report.ReportData import ReportData
from sqlalchemy import *
import datetime
import math
from model.StockInfo import StockInfo
from model.report.Zycwzb import Zycwzb
from model.Buffett import Buffett
from utils.db_utils import *


def get_latest_record_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if 1 <= month <= 4:
        year -= 1
        return str(year) + "-" + "12-31"
    elif 5 <= month <= 8:
        return str(year) + "-" + "03-31"
    elif 9 <= month <= 10:
        return str(year) + "-" + "06-30"
    elif 11 <= month:
        return str(year) + "-" + "09-30"
    else:
        return None


def calc_buffet_result(code, name, stock):
    date = get_latest_record_date()
    logging.info("handle %s %s %s", code, name, date)
    zycwzb = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == date)).first()

    if zycwzb is None:
        logging.info("%s %s 信息没有取到", code, name)
        return

    flow_assets = zycwzb.flow_assets
    total_debts = zycwzb.total_debts
    flow_debts = zycwzb.flow_debts

    mktcap = stock.mktcap

    if mktcap is None:
        logging.info("%s %s 市值没有取到.", code, name)
        return

    logging.info("%s %s 流动资产:%s 总负债:%s 流动负债: %s, 总市值:%s", code, name, flow_assets, total_debts, flow_debts, mktcap)
    old_safe = session.query(Buffett).filter(and_(Buffett.code == code)).first()
    if old_safe is None:
        old_safe = Buffett(code = code, name = name)
    old_safe.flow_sub_total = round((flow_assets - total_debts) / mktcap, 2)
    old_safe.flow_sub_flow = round((flow_assets - flow_debts) / mktcap, 2)

    save(old_safe)


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        calc_buffet_result(code, name, row)
