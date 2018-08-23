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

engine = create_engine(dbconfig.getConfig('database', 'connURL'))
Session = sessionmaker(bind=engine)
session = Session()


def save(data, autocommit=True):
    session.add(data)
    if autocommit:
        session.commit()


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


def get_pre_yearreport_date(date_str):
    year = int(date_str[0:4]) - 1
    return str(year) + "-" + "12-31"


def analyze():
    latest_date = get_latest_record_date()
    logging.info("latest_date: %s", latest_date)


def get_multiple(date):
    month = datetime.datetime.now().month

    date_no_year = date[(len(date) - 5):]
    if date_no_year == '03-31':
        return 4
    if date_no_year == '06-30':
        return 2
    if date_no_year == '09-30':
        return 4/3
    if date_no_year == '12-31':
        return 1


    #if 1 <= month <= 4:
        #return 1
    #elif 5 <= month <= 8:
        #return 4
    #elif 9 <= month <= 10:
        #return 2
    #elif 11 <= month:
        #return 4 / 3


def calc_pe_eps(code, name, stock):
    logging.info("handle %s %s", code, name)
    date1 = get_latest_record_date()
    date2 = get_pre_yearreport_date(date1)
    date3 = get_pre_yearreport_date(date2)
    date4 = get_pre_yearreport_date(date3)
    #zycwzb1 = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == date1)).first()
    zycwzb1 = session.query(Zycwzb).filter(and_(Zycwzb.code == code)).order_by(desc(Zycwzb.date)).limit(1).first()
    date1 = zycwzb1.date
    zycwzb2 = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == date2)).first()
    zycwzb3 = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == date3)).first()
    zycwzb4 = session.query(Zycwzb).filter(and_(Zycwzb.code == code, Zycwzb.date == date4)).first()
    old = session.query(RealTimePEEPS).filter(RealTimePEEPS.code == code).first()

    ## 股数
    totals = stock.totals * 10000

    multiple = get_multiple(date1)
    if old is None:
        old = RealTimePEEPS(code=code, name=name)
    if zycwzb1 is not None:
        old.eps1 = float(zycwzb1.eps)
        old.latest_report_date = zycwzb1.date
    if zycwzb1 is not None: old.koufei_eps = float(round(zycwzb1.npad / totals, 2))
    if zycwzb2 is not None: old.eps2 = float(zycwzb2.eps)
    if zycwzb3 is not None: old.eps3 = float(zycwzb3.eps)
    if zycwzb4 is not None: old.eps4 = float(zycwzb4.eps)

    hist = session.query(HistData).filter(HistData.code == code).order_by(desc(HistData.date)).limit(1).first()
    if hist is None:
        return
    koufei_pe = round(float(hist.close) / (old.koufei_eps * multiple), 0) if old.koufei_eps != 0 and old.koufei_eps is not None else -999
    pe1 = round(float(hist.close) / (old.eps1 * multiple), 0) if old.eps1 != 0 and old.eps1 is not None else -999
    pe2 = round(float(hist.close) / old.eps2, 0) if old.eps2 != 0 and old.eps2 is not None else -999
    pe3 = round(float(hist.close) / old.eps3, 0) if old.eps3 != 0 and old.eps3 is not None else -999
    pe4 = round(float(hist.close) / old.eps4, 0) if old.eps4 != 0 and old.eps4 is not None else -999
    old.koufei_pe = koufei_pe
    old.pe1 = pe1
    old.pe2 = pe2
    old.pe3 = pe3
    old.pe4 = pe4
    old.date = hist.date
    old.price = hist.close
    save(old)


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    #stocks = session.query(StockInfo).filter(StockInfo.code == '600230').all()
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        calc_pe_eps(code, name, row)
