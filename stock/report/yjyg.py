__author__ = 'kittaaron'
# 业绩预告

import tushare as ts
import config.logginconfig
import logging
from utils.db_utils import *


def get_yjyg():
    df = ts.forecast_data(2018, 2)
    df.to_sql('yjyg', engine, if_exists='replace', index=False, index_label='code')


if __name__ == '__main__':
    get_yjyg()