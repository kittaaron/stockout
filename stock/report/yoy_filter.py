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
from model.PorYoySts import PorYoySts
from model.report.Zcfzb import Zcfzb
from model.report.Cwbbzy import Cwbbzy
from model.report.Lrb import Lrb
from model.report.Xjllb import Xjllb
from utils.db_utils import *


"""
找出近几年主营业务收入连续增长的股票
"""

def yoy_filter(code, name, stock):
    logging.info("handle %s %s", code, name)
    zycwzbs = session.query(Zycwzb).filter(and_(Zycwzb.code == code)).order_by(desc(Zycwzb.date)).all()

    pre_por = 0
    por_grow_cnt = 0
    por_grow_10_cnt = 0
    por_grow_20_cnt = 0
    for zycwzb in zycwzbs:
        current_por = float(zycwzb.por)
        if pre_por == 0:
            pre_por = current_por
            continue
        grow = current_por - pre_por
        if grow > 0:
            por_grow_cnt += 1
        if current_por > pre_por * 1.1:
            por_grow_10_cnt += 1
        if current_por > pre_por * 1.2:
            por_grow_20_cnt += 1
    porYoySts = session.query(PorYoySts).filter(and_(PorYoySts.code == code)).first()
    if porYoySts is None:
        porYoySts = PorYoySts(code = code, name = name)
    porYoySts.por_grow_cnt = por_grow_cnt
    porYoySts.por_grow_10_cnt = por_grow_10_cnt
    porYoySts.por_grow_20_cnt = por_grow_20_cnt
    save(porYoySts)
    logging.info("%s %s %s %s", name, por_grow_cnt, por_grow_10_cnt, por_grow_20_cnt)


if __name__ == '__main__':
    stocks = session.query(StockInfo).all()
    for row in stocks:
        if row is None:
            continue
        code = row.code
        name = row.name
        yoy_filter(code, name, row)
