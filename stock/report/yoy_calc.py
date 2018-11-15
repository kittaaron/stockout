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


def get_pre_yearreport_date(date_str):
    year = int(date_str[0:4]) - 1
    return str(year) + "-" + "12-31"


def get_pre_same_season_date(date_str):
    year = int(date_str[0:4]) - 1
    month_date = date_str[4:]
    return str(year) + month_date


def analyze():
    latest_date = get_latest_record_date()
    logging.info("latest_date: %s", latest_date)


def get_multiple():
    month = datetime.datetime.now().month
    if 1 <= month <= 4:
        return 1
    elif 5 <= month <= 8:
        return 4
    elif 9 <= month <= 10:
        return 2
    elif 11 <= month:
        return 4 / 3


def calc_yoy(code, name, stock):
    logging.info("handle %s %s", code, name)
    zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.code == code)).order_by(desc(Zycwzb.date)).all()

    if zycwzbs is None:
        logging.info("%s no zycwzb")
        return

    zycwzb_dict = {}
    for zycwzb in zycwzbs:
        zycwzb_dict[zycwzb.date] = zycwzb

    for zycwzb in zycwzbs:
        pre_same_season_date = get_pre_same_season_date(zycwzb.date)
        if pre_same_season_date not in zycwzb_dict:
            continue
        pre_zycwzb = zycwzb_dict[pre_same_season_date]
        if pre_zycwzb is None:
            continue
        if zycwzb.net_profit is not None and pre_zycwzb.net_profit is not None and pre_zycwzb.net_profit != 0:
            zycwzb.net_yoy = round(zycwzb.net_profit / pre_zycwzb.net_profit, 2)
        if zycwzb.por is not None and pre_zycwzb.por is not None and pre_zycwzb.por != 0:
            zycwzb.por_yoy = round(zycwzb.por / pre_zycwzb.por, 2)
        if zycwzb.pop is not None and pre_zycwzb.pop is not None and pre_zycwzb.pop != 0:
            zycwzb.pop_yoy = round(zycwzb.pop / pre_zycwzb.pop, 2)
        save(zycwzb)


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    #stocks = session.query(StockInfo).filter(StockInfo.code == '002236').all()
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        calc_yoy(code, name, row)
