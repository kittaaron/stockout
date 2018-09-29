__author__ = 'kittaaron'
# 龙虎榜

import tushare as ts
import config.logginconfig
import logging
from utils.db_utils import *
import datetime


def get_lhb():
    today = datetime.date.today()
    #delta = datetime.timedelta(days=0)
    #ndays_before = today - delta

    date_str = today.strftime('%Y-%m-%d')
    logging.info("date: %s", date_str)
    df = ts.top_list(date_str)
    df.to_sql('lhb', engine, if_exists='append', index=False, index_label='code')


if __name__ == '__main__':
    get_lhb()