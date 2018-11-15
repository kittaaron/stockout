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
from model.ExtraZB import ExtraZB
from decimal import Decimal
from utils.db_utils import *


def save(data, autocommit=True):
    session.add(data)
    if autocommit:
        session.commit()


def build_extraZB(extraZB, zcfzb, zycwzb):
    tca = zcfzb.tca
    inventories = zcfzb.inventories
    ats = zcfzb.ats
    acid_asset = tca - inventories - ats
    total_current_liabi = zcfzb.total_current_liabi

    liquidity_ratio = (tca / total_current_liabi).quantize(Decimal('0.00'))
    extraZB.liquidity_ratio = liquidity_ratio
    extraZB.acid_ratio = round(acid_asset / total_current_liabi, 2)
    if zycwzb is not None:
        extraZB.por_yoy = zycwzb.por_yoy
        extraZB.pop_yoy = zycwzb.pop_yoy
        extraZB.net_yoy = zycwzb.net_yoy


def to_dict(zycwzbs):
    dict = {}
    for zycwzb in zycwzbs:
        dict[zycwzb.date] = zycwzb
    return dict


def calc_cznl(code, name, stock):
    """
    偿债能力
    :param code:
    :param name:
    :param stock:
    :return:
    """
    # 如果code_date已经录入，则已经插入过，不继续插入
    zcfzbs = session.query(Zcfzb).filter(and_(Zcfzb.code == code)).all()
    zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.code == code)).all()
    zycwzbs_dict = to_dict(zycwzbs)
    for zcfzb in zcfzbs:
        date = zcfzb.date
        tca = zcfzb.tca
        total_current_liabi = zcfzb.total_current_liabi

        if total_current_liabi == 0 or tca == 0:
            logging.warning("%s %s 流动负债 %s 流动资产 %s", code, name, total_current_liabi, tca)
            continue

        zycwzb = zycwzbs_dict[date] if date in zycwzbs_dict else None
        #liquidity_ratio = round(tca / total_current_liabi, 2)
        extraZB = session.query(ExtraZB).filter(and_(ExtraZB.code == code, ExtraZB.date == date)).first()
        if extraZB is None:
            extraZB = ExtraZB(code=code, name=name, date=date)
        build_extraZB(extraZB, zcfzb, zycwzb)
        save(extraZB)
        logging.info("%s %s 处理完成", code, name)


if __name__ == '__main__':
    stocks = session.query(StockInfo).filter(StockInfo.code == '002236').all()
    #stocks = session.query(StockInfo).all()
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        calc_cznl(code, name, row)
