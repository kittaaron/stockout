__author__ = 'kittaaron'
# 限售解禁

import tushare as ts
import config.logginconfig
import logging
from utils.db_utils import *
import datetime
from model.report.xsjj_model import xsjj_model
from decimal import *
from dateutil.relativedelta import relativedelta
from sqlalchemy import *
import time

"""
限售解禁数据
"""


session = getSession()


def get_xsjj_by_code_time(code, start_date, end_date):
    xsjj_datas = session.query(xsjj_model).filter(
        and_(xsjj_model.code == code, xsjj_model.date >= start_date, xsjj_model.date <= end_date)).all()
    return xsjj_datas


def get_xsjj_by_range(page, page_size, start_date, end_date):
    page = 0 if not page else page
    pageSize = 200 if not page_size else page_size
    offset = page * pageSize
    xsjj_datas = session.query(xsjj_model).filter(
        and_(xsjj_model.date >= start_date, xsjj_model.date <= end_date, xsjj_model.ratio >= 5)).limit(pageSize).offset(offset).all()
    return xsjj_datas


def get_xsjj_totals_by_range(start_date, end_date):
    cnt = session.query(func.count(xsjj_model.id)).filter(and_(xsjj_model.date >= start_date, xsjj_model.date <= end_date)).scalar()
    return cnt


def get_xsjj_by_code_date(code, date):
    xsjj_datas = session.query(xsjj_model).filter(
        and_(xsjj_model.code == code, xsjj_model.date == date)).all()
    return xsjj_datas


def dump_xsjj(year, month):
    logging.info("开始获取数据 %s %s", year, month)
    df = ts.xsg_data(year=year, month=month)
    logging.info("获取数据完成 %s %s", year, month)
    if df is None:
        return

    list = []

    for index, row in df.iterrows():
        code = row['code']
        name = row['name']
        date = row['date']
        xsjj_data = get_xsjj_by_code_date(code, date)
        if xsjj_data is not None:
            logging.info("%s %s %s 数据已dump", code, name, date)
        xsjj_data = xsjj_model(code=code, name=name, date=date)
        xsjj_data.count = row['count']
        xsjj_data.ratio = float(row['ratio'])
        list.append(xsjj_data)
    session.add_all(list)


if __name__ == '__main__':
    now = datetime.date.today()
    endtime = datetime.date.today() + relativedelta(months=-5)
    starttime = endtime
    endtime = datetime.date.today() + relativedelta(months=+20)
    while starttime <= endtime:
        year = starttime.year
        month = starttime.month
        dump_xsjj(year, month)
        logging.info("%s %s 数据dump完成", year, month)
        starttime += relativedelta(months=+1)
        time.sleep(3)
