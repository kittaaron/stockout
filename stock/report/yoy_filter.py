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
from model.RealTimePE import RealTimePE
from model.RealTimePEEPS import RealTimePEEPS
import math
from model.StockInfo import StockInfo
from model.report.Zycwzb import Zycwzb
from model.report.Zcfzb import Zcfzb
from model.report.Cwbbzy import Cwbbzy
from model.report.Lrb import Lrb
from model.report.Xjllb import Xjllb


"""
找出近几年主营业务收入、利润连续增长的股票
"""

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def save(data, autocommit=True):
    session.add(data)
    if autocommit:
        session.commit()


def yoy_filter(code, name, stock):
    logging.info("handle %s %s", code, name)
    zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.code == code)).order_by(desc(Zycwzb.date)).all()

    if zycwzbs is None:
        logging.info("%s no zycwzb")
        return

    today = datetime.date.today()
    total_delta = datetime.timedelta(days=500)
    three_years_ago = today - total_delta
    three_years_ago = three_years_ago.strftime('%Y-%m-%d')

    zycwzb_dict = {}
    for zycwzb in zycwzbs:
        zycwzb_dict[zycwzb.date] = zycwzb

    all_por_yoy_ok = True
    for zycwzb in zycwzbs:
        if zycwzb.por_yoy is None:
            continue
        report_date = zycwzb.date
        if report_date <= three_years_ago:
            continue
        if zycwzb.por_yoy <= 1.00:
            all_por_yoy_ok = False
            break
    if all_por_yoy_ok is True:
        logging.info("%s %s por_yoy ok.", code, name)


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        yoy_filter(code, name, row)
