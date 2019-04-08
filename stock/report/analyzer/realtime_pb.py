from typing import Any, Union

import tushare as ts
import logging
import config.logginconfig
from model.report.ReportData import ReportData
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from config import dbconfig
import math
import datetime
from dateutil.relativedelta import relativedelta
from model.HistData import HistData
from model.RealTimePB import RealTimePB
import math
from model.StockInfo import StockInfo
from model.report.Zycwzb import Zycwzb
from utils.db_utils import *


session = getSession()


def calc_pb(code, name, stock):
    logging.info("handle %s %s", code, name)
    report_max_date = session.query(func.max(Zycwzb.date)).filter(Zycwzb.code == code).first()
    if report_max_date is None:
        logging.warning("no report found")
        return

    filter_date = report_max_date[0]
    zycwzb = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == filter_date)).first()
    if zycwzb is None:
        logging.warning("%s %s no report found", code, name)
        return

    hist_data = session.query(HistData).filter(HistData.code == code).order_by(desc(HistData.date)).limit(1).first()
    if hist_data is None:
        logging.warning("%s %s no hist_data found", code, name)
        return

    old = session.query(RealTimePB).filter(RealTimePB.code == code).first()

    if old is None:
        old = RealTimePB(code=code, name=name)

    old.date = hist_data.date
    old.price = hist_data.close
    old.total_assets = zycwzb.total_assets
    old.flow_assets = zycwzb.flow_assets
    old.total_debts = zycwzb.total_debts
    old.flow_debts = zycwzb.flow_debts
    old.net_assets = zycwzb.total_assets - zycwzb.total_debts
    old.sheq = zycwzb.sheq
    old.mktcap = stock.mktcap
    old.pb = round(old.mktcap / old.sheq, 2) if old.sheq > 0 else None
    old.liab_ratio = round(old.total_debts * 100 / old.total_assets, 2) if old.total_debts > 0 and old.total_assets > 0 else None
    old.non_current_liab_ratio = round((old.total_debts - old.flow_debts) * 100/ old.total_assets, 2) if old.total_debts is not None and old.total_assets > 0 and old.flow_debts is not None else None

    session.add(old)
    logging.info("%s %s pb save ok", code, name)


def get_stocks_map(stocks):
    ret = {}
    for stock in stocks:
        ret[stock.code] = stock
    return ret


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    #stocks = session.query(StockInfo).filter(StockInfo.code == '002943').all()
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        calc_pb(code, name, row)
