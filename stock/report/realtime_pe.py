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
import math
from utils.db_utils import *


def analyze():
    # 业绩主表数据
    rdf = ts.get_report_data(2018, 1)
    records = rdf.to_dict("records")
    for data in records:
        code = data['code']
        name = data['name']
        hist = session.query(HistData).filter(HistData.code == code).order_by(desc(HistData.date)).limit(1).first()
        if hist is None:
            continue
        if data['eps'] is None or str(data['eps']) == 'nan' or math.isnan(data['eps']):
            continue
        if data['eps'] == 0:
            continue
        realtime_pe = round(float(hist.close) / (data['eps'] * 4), 0)
        logging.info("%s %s pe %s eps %s 当前价: %s", code, name, realtime_pe, data['eps'], hist.close)
        old = session.query(RealTimePE).filter(RealTimePE.code == code).first()
        if old is None:
            old = RealTimePE(code=code, name=name)
        old.pe = realtime_pe
        old.eps = data['eps']
        old.price = hist.close
        old.date = hist.date
        old.pe2 = 0
        old.pe3 = 0
        old.eps2 = 0
        old.eps3 = 0
        save(old)

    # 业绩主表数据
    rdf2 = ts.get_report_data(2017, 4)
    records2 = rdf2.to_dict("records")
    for data in records2:
        code = data['code']
        name = data['name']
        hist = session.query(HistData).filter(HistData.code == code).order_by(desc(HistData.date)).limit(1).first()
        if hist is None:
            continue
        if data['eps'] is None or str(data['eps']) == 'nan' or math.isnan(data['eps']):
            continue
        if data['eps'] == 0:
            continue
        realtime_pe = round(float(hist.close) / data['eps'], 0)
        logging.info("%s %s pe %s eps %s 当前价: %s", code, name, realtime_pe, data['eps'], hist.close)
        old = session.query(RealTimePE).filter(RealTimePE.code == code).first()
        if old is None:
            old = RealTimePE(code=code, name=name)
            old.eps = data['eps']
            old.price = hist.close
            old.date = hist.date
            old.pe = 0
            old.eps = 0
            old.pe3 = 0
            old.eps3 = 0
        old.pe2 = realtime_pe
        old.eps2 = data['eps']
        save(old)


    # 业绩主表数据
    rdf3 = ts.get_report_data(2016, 4)
    records3 = rdf3.to_dict("records")
    for data in records3:
        code = data['code']
        name = data['name']
        hist = session.query(HistData).filter(HistData.code == code).order_by(desc(HistData.date)).limit(1).first()
        if hist is None:
            continue
        if data['eps'] is None or str(data['eps']) == 'nan' or math.isnan(data['eps']):
            continue
        if data['eps'] == 0:
            continue
        realtime_pe = round(float(hist.close) / data['eps'], 0)
        logging.info("%s %s pe %s eps %s 当前价: %s", code, name, realtime_pe, data['eps'], hist.close)
        old = session.query(RealTimePE).filter(RealTimePE.code == code).first()
        if old is None:
            old = RealTimePE(code=code, name=name)
            old.eps = data['eps']
            old.price = hist.close
            old.date = hist.date
            old.pe = 0
            old.eps = 0
            old.pe2 = 0
            old.eps2 = 0
        old.pe3 = realtime_pe
        old.eps3 = data['eps']
        save(old)


if __name__ == '__main__':
    analyze()