__author__ = 'kittaaron'
# 融资融券

import tushare as ts
import config.logginconfig
import logging
from utils.db_utils import *
import datetime


def dump_rzrq():
    today = datetime.date.today()
    delta = datetime.timedelta(days=360)
    ndays_before = today - delta
    print("%s, %s", today, ndays_before)
    df = ts.sz_margins(start=ndays_before.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
    df.to_sql('rzrq_total', engine, if_exists='append', index=False, index_label='opDate')


if __name__ == '__main__':
    dump_rzrq()
