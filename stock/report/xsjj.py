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


def save_list(datas, autocommit=True):
    session.add_all(datas)
    if autocommit:
        session.commit()


def get_xsjj_by_code_time(code, start_date, end_date):
    xsjj_datas = session.query(xsjj_model).filter(and_(xsjj_model.code == code, xsjj_model.date >= start_date, xsjj_model.date <= end_date)).all()
    return xsjj_datas


def dump_xsjj(year, month):
    df = ts.xsg_data(year=year, month=month)
    if df is None:
        return

    list = []
    for index, row in df.iterrows():
        xsjj_data = xsjj_model(code=row['code'], name=row['name'], date=row['date'])
        xsjj_data.count = row['count']
        xsjj_data.ratio = float(row['ratio'])
        list.append(xsjj_data)
    save_list(list)


if __name__ == '__main__':
    now = datetime.date.today()
    endtime = datetime.date.today() + relativedelta(months=+5)
    starttime = endtime
    endtime = datetime.date.today() + relativedelta(months=+20)
    while starttime <= endtime:
        year = starttime.year
        month = starttime.month
        dump_xsjj(year, month)
        logging.info("%s %s 数据dump完成", year, month)
        starttime += relativedelta(months=+1)
