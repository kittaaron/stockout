__author__ = 'kittaaron'
# 每日龙虎榜列表

import tushare as ts
import config.logginconfig
import logging
from utils.db_utils import *
import datetime


def get_top_list():
    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    ndays_before = today - delta
    date_str = ndays_before.strftime('%Y-%m-%d');
    logging.info("date: %s", date_str)
    df = ts.top_list(date_str)
    df.to_sql('top_list', engine, if_exists='append', index=False, index_label='code')


if __name__ == '__main__':
    get_top_list()